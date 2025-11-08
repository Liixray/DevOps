<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getQuestion, getQuestionsCount, postParticipation } from '@/services/questions'
import { getLeaderboard } from '@/services/leaderboard'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

const LEADERBOARD_ITEMS_PER_PAGE = ref(10)

const playerName = ref('')
const showQuiz = ref(false)

const question = ref(null)
const loading = ref(false)
const error = ref(null)
const apiError = ref(null) // erreurs réseau non-bloquantes

const currentQuestion = ref(0)
const totalQuestions = ref(0)
const answers = ref([]) // index sélectionné par question (null = non validé)
const selectedOption = ref(null)
const isFinished = ref(false)
const score = ref(0)
const allQuestions = ref([]) // Stocke toutes les questions récupérées

// Leaderboard
const leaderboard = ref([])
const leaderboardPage = ref(1)
const leaderboardTotalPages = ref(1)
const leaderboardLoading = ref(false)

// fetch question and store into allQuestions[position] (doesn't change currentQuestion/question unless asked)
async function fetchAndStoreQuestion(position) {
  try {
    const q = await getQuestion(position)
    allQuestions.value[position] = q
    return q
  } catch (e) {
    throw e
  }
}

async function fetchQuestion(position) {
  loading.value = true
  error.value = null
  try {
    const q = await fetchAndStoreQuestion(position)
    question.value = q
  } catch (e) {
    error.value = e.message || String(e)
    question.value = null
  } finally {
    loading.value = false
  }
}

async function fetchTotalQuestions() {
  try {
    const data = await getQuestionsCount()
    totalQuestions.value = data.size
    answers.value = Array(totalQuestions.value).fill(null)
    allQuestions.value = Array(totalQuestions.value).fill(null)
  } catch (e) {
    error.value = e.message || String(e)
    totalQuestions.value = 0
  }
}

/**
 * Récupère les données du leaderboard
 */
async function fetchLeaderboardData() {
  leaderboardLoading.value = true
  try {
    const response = await getLeaderboard(leaderboardPage.value, LEADERBOARD_ITEMS_PER_PAGE.value)
    console.log('Leaderboard data:', response)
    
    if (response.data) {
      leaderboard.value = response.data
      // Calculer le total d'entrées à partir du nombre de pages
      leaderboardTotalPages.value = response.totalPages || 1
    } else {
      leaderboard.value = []
      leaderboardTotalPages.value = 1
    }
    
    console.log('Leaderboard processed:', leaderboard.value)
    console.log('Total pages:', leaderboardTotalPages.value)
  } catch (e) {
    console.error('Erreur leaderboard:', e)
    leaderboard.value = []
    leaderboardTotalPages.value = 1
  } finally {
    leaderboardLoading.value = false
  }
}

/**
 * Change de page du leaderboard
 */
async function changeLeaderboardPage(direction) {
  if (direction === 'next' && leaderboardPage.value < leaderboardTotalPages.value) {
    leaderboardPage.value++
    await fetchLeaderboardData()
  } else if (direction === 'prev' && leaderboardPage.value > 1) {
    leaderboardPage.value--
    await fetchLeaderboardData()
  }
}

/**
 * Calcule l'index de classement pour l'affichage
 */
function getLeaderboardRank(index) {
  return (leaderboardPage.value - 1) * LEADERBOARD_ITEMS_PER_PAGE.value + index + 1
}

// Charger le nombre total de questions au montage
onMounted(async () => {
  await fetchTotalQuestions()
  await fetchLeaderboardData()
})

// Surveiller le changement de question pour charger la nouvelle question via l'API
watch(currentQuestion, async (newIndex) => {
  selectedOption.value = answers.value[newIndex]
  await fetchQuestion(newIndex)
})

/**
 * Surveiller le changement du nombre d’éléments par page pour recharger le leaderboard
 */
watch(LEADERBOARD_ITEMS_PER_PAGE, async () => {
  leaderboardPage.value = 1
  await fetchLeaderboardData()
})

/**
 * Récupère toutes les questions manquantes (utilisé avant la revue)
 */
async function fetchAllRemainingQuestions() {
  const missing = []
  for (let i = 0; i < totalQuestions.value; i++) {
    if (!allQuestions.value[i]) missing.push(i)
  }
  for (const idx of missing) {
    try {
      await fetchAndStoreQuestion(idx)
    } catch (e) {
      apiError.value = apiError.value || []
      apiError.value.push(`Failed to fetch question ${idx + 1}: ${e.message || e}`)
    }
  }
}

/**
 * Enregistre la participation
 */
async function saveParticipation() {
  const payload = {
    playerName: playerName.value,
    score: score.value,
    answers: answers.value.map((answerIdx, i) => {
      const q = allQuestions.value[i]
      return q?.possibleAnswers?.[answerIdx]?.id ?? null
    }),
    idVersions: allQuestions.value[0]?.idVersions || 1
  }
  try {
    await postParticipation(payload)
  } catch (e) {
    apiError.value = apiError.value || []
    apiError.value.push(`Failed to save participation: ${e.message || e}`)
  }
}

/**
 * Enregistre la réponse validée et passe à la question suivante ou fin
 */
async function nextQuestion() {
  // store selected into validated answers
  answers.value[currentQuestion.value] = selectedOption.value

  if (currentQuestion.value < totalQuestions.value - 1) {
    currentQuestion.value++
    return
  }
  // sinon, fin du quiz
  await fetchAllRemainingQuestions()
  calculateScore()
  await saveParticipation()
  isFinished.value = true
}

/**
 * Va à la question spécifiée si elle a déjà été répondue
 */
function goToQuestion(index) {
  if (answers.value[index] !== null && !isFinished.value) {
    currentQuestion.value = index
  }
}

/**
 * Démarre le quiz si un nom d'utilisateur a été saisi
 */
const router = useRouter()
async function startQuiz() {
  const name = playerName.value.trim()
  if (name !== '') {
    if (name.toLowerCase() === 'admin') {
      router.push('/admin/login')
      return
    }
    showQuiz.value = true
    currentQuestion.value = 0
    answers.value = Array(totalQuestions.value).fill(null)
    selectedOption.value = null
    isFinished.value = false
    score.value = 0
    await fetchQuestion(0)
  }
}

/**
 * Calcule le score final
 */
function calculateScore() {
  let total = 0
  for (let i = 0; i < totalQuestions.value; i++) {
    const q = allQuestions.value[i]
    const ansIdx = answers.value[i]
    if (q && q.possibleAnswers && ansIdx !== null && q.possibleAnswers[ansIdx]?.isCorrect) {
      total++
    }
  }
  score.value = total
}

/**
 * préparation des données pour la revue
 */
const reviewList = computed(() => {
  const list = []
  for (let i = 0; i < totalQuestions.value; i++) {
    const q = allQuestions.value[i]
    list.push({
      index: i,
      question: q ?? { text: 'Question manquante', possibleAnswers: [] },
      selectedIndex: answers.value[i]
    })
  }
  return list
})
</script>

<template>
  <section class="min-h-screen flex items-center justify-center bg-white p-4">
    <div class="w-full max-w-6xl mx-auto pb-24 md:pb-0">
      <!-- Intro avec classement -->
      <div v-if="!showQuiz" class="flex flex-col lg:flex-row gap-8 items-start justify-center py-12 px-4">
        <!-- Formulaire de démarrage -->
        <div class="flex flex-col items-center justify-center space-y-6 w-full lg:w-1/2 max-w-lg border border-gray-300 rounded-lg p-8 bg-white">
          <h1 class="text-3xl font-semibold text-center">Prêt pour le meilleur quiz ?</h1>
          <input
            v-model="playerName"
            type="text"
            placeholder="Nom d'utilisateur ..."
            class="rounded-lg px-6 py-3 bg-gray-100 text-xl placeholder-gray-400 focus:outline-none w-full"
          />
          <Button
            class="bg-gray-300 text-xl px-8 py-2 mt-2"
            :disabled="playerName.trim() === ''"
            @click="startQuiz"
          >
            C'est parti !
          </Button>
        </div>

        <!-- Séparateur vertical -->
        <div class="hidden lg:block w-px bg-gray-300 self-stretch min-h-[400px]"></div>

        <!-- Classement général -->
        <div class="w-full lg:w-1/2 max-w-lg border border-gray-300 rounded-lg bg-white">
          <div class="p-6 border-b border-gray-200 flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <h2 class="text-xl font-semibold text-center sm:text-left">Classement général</h2>
            <!-- Sélecteur dynamique du nombre d’entrées -->
            <div class="mt-4 sm:mt-0">
              <label class="text-sm text-gray-600 mr-2">Éléments par page :</label>
              <select
                v-model="LEADERBOARD_ITEMS_PER_PAGE"
                class="border border-gray-300 rounded px-2 py-1 text-sm"
              >
                <option :value="10">10</option>
                <option :value="20">20</option>
                <option :value="50">50</option>
              </select>
            </div>
          </div>
          <div class="p-6">
            <div v-if="leaderboardLoading" class="text-center py-8 text-gray-600">
              Chargement du classement...
            </div>
            <div v-else-if="leaderboard.length === 0" class="text-center py-8 text-gray-500">
              Aucune participation pour le moment. Soyez le premier !
            </div>
            <div v-else class="space-y-3">
              <div
                v-for="(participant, index) in leaderboard"
                :key="participant.id || index"
                class="flex items-center justify-between px-5 py-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
              >
                <div class="flex items-center gap-4">
                  <span class="text-2xl font-handwriting text-gray-600 min-w-[2.5rem] text-center">
                    {{ getLeaderboardRank(index) }}
                  </span>
                  <span class="text-lg">{{ participant.playerName || participant.name || 'Anonyme' }}</span>
                </div>
                <span class="font-medium text-gray-700">{{ participant.score }}/{{ totalQuestions || '?' }}</span>
              </div>
              
              <!-- Pagination -->
              <div v-if="leaderboardTotalPages > 1" class="flex justify-center items-center gap-4 pt-6 mt-4 border-t border-gray-200">
                <Button
                  @click="changeLeaderboardPage('prev')"
                  :disabled="leaderboardPage === 1"
                  class="px-4 py-2"
                >
                  ← Précédent
                </Button>
                <span class="text-sm text-gray-600">
                  Page {{ leaderboardPage }} / {{ leaderboardTotalPages }}
                </span>
                <Button
                  @click="changeLeaderboardPage('next')"
                  :disabled="leaderboardPage >= leaderboardTotalPages"
                  class="px-4 py-2"
                >
                  Suivant →
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quiz -->
      <div v-else-if="!isFinished" class="flex flex-col md:flex-row gap-6 items-start">
        <div class="flex-1 flex justify-center">
          <Card class="w-full max-w-3xl bg-gray-100">
            <CardHeader>
              <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                <div>
                  <div class="font-semibold">Question N°{{ currentQuestion + 1 }}</div>
                  <CardTitle class="text-2xl mt-1">{{ question?.title || '' }}</CardTitle>
                </div>
                <div class="hidden md:block text-sm text-gray-600">Question {{ currentQuestion + 1 }} / {{ totalQuestions }}</div>
              </div>
            </CardHeader>

            <CardContent>
              <div v-if="loading" class="text-center my-8">Chargement…</div>
              <div v-else-if="error" class="text-red-500 my-8">{{ error }}</div>
              <div v-else-if="question" class="mb-4">
                <img
                  v-if="question.image"
                  :src="question.image"
                  alt="illustration"
                  class="w-full max-h-90 object-cover rounded my-4"
                />
                <div class="mb-4 text-base leading-relaxed">{{ question.text }}</div>

                <RadioGroup v-model="selectedOption" class="space-y-4">
                  <div
                    v-for="(option, index) in question.possibleAnswers"
                    :key="option.id"
                    class="flex items-start space-x-4"
                  >
                    <RadioGroupItem
                      :value="index"
                      :id="'option-' + index"
                      class="mt-1 w-5 h-5 border-2 border-gray-300"
                    />
                    <label :for="'option-' + index" class="text-base cursor-pointer w-full">
                      {{ option.text }}
                    </label>
                  </div>
                </RadioGroup>
              </div>

              <div class="flex justify-center mt-6">
                <Button
                  :class="[selectedOption !== null ? 'bg-green-400' : 'bg-gray-300', 'text-xl px-8 py-2']"
                  :disabled="selectedOption === null"
                  @click="nextQuestion"
                >
                  Suivant <span class="ml-2 text-2xl">→</span>
                </Button>
              </div>

              <div v-if="apiError" class="mt-4 text-sm text-yellow-700">
                <div v-if="Array.isArray(apiError)">
                  <div v-for="(e,i) in apiError" :key="i">{{ e }}</div>
                </div>
                <div v-else>{{ apiError }}</div>
              </div>
            </CardContent>
          </Card>
        </div>

        <!-- Sidebar for md+ -->
        <aside class="hidden md:block w-72 shrink-0">
          <Card class="bg-gray-100 h-full">
            <CardHeader>
              <CardTitle class="text-lg">Questions</CardTitle>
            </CardHeader>
            <CardContent>
              <div class="space-y-3 max-h-[60vh] overflow-auto pr-2">
                <div
                  v-for="index in totalQuestions"
                  :key="index"
                  class="flex items-center justify-between px-4 py-3 rounded-lg transition-all"
                  :class="{
                    'bg-gray-200 text-gray-400 cursor-not-allowed': answers[index - 1] === null,
                    'bg-white hover:bg-blue-100 cursor-pointer': answers[index - 1] !== null
                  }"
                  @click="goToQuestion(index - 1)"
                >
                  <span>Question N°{{ index }}</span>
                  <span v-if="answers[index - 1] !== null" class="w-3 h-3 bg-green-700 rounded-full inline-block"></span>
                </div>
              </div>
            </CardContent>
          </Card>
        </aside>
        <!-- Bottom bar for mobile -->
        <div class="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t p-2">
          <div class="max-w-6xl mx-auto px-4">
            <div class="flex gap-2 overflow-x-auto pb-1">
              <button
                v-for="index in totalQuestions"
                :key="index"
                @click="goToQuestion(index - 1)"
                :disabled="answers[index - 1] === null"
                :class="[
                  'min-w-[56px] px-3 py-2 rounded-md text-sm whitespace-nowrap',
                  answers[index - 1] === null ? 'bg-gray-200 text-gray-400' : 'bg-white border'
                ]"
              >
                {{ index }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Results + Review -->
      <div v-else class="mt-8">
        <Card class="max-w-4xl w-full bg-gray-100 p-6 mx-auto">
          <CardHeader>
            <CardTitle class="text-2xl mb-2">Résultat du quiz</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="text-xl text-center mb-6">
              Vous avez <span class="font-bold text-green-700">{{ score }}</span> bonne(s) réponse(s) sur <span class="font-bold">{{ totalQuestions }}</span>.
            </div>

            <div class="space-y-6">
              <div v-for="item in reviewList" :key="item.index" class="p-4 bg-white rounded shadow-sm">
                <div class="flex items-start justify-between">
                  <div>
                    <div class="text-sm text-gray-500">Question N°{{ item.index + 1 }}</div>
                    <div class="font-medium mt-1">{{ item.question.title }}</div>
                    <img v-if="item.question.image" :src="item.question.image" class="mt-3 w-full max-h-60 object-cover rounded" />
                  </div>
                </div>

                <div class="mt-3 space-y-2">
                  <div
                    v-for="(opt, idx) in item.question.possibleAnswers"
                    :key="opt.id"
                    :class="[
                      'px-3 py-2 rounded',
                      // correct answer
                      opt.isCorrect ? 'bg-green-50 border-l-4 border-green-600 text-green-800' : '',
                      // user's wrong answer
                      (item.selectedIndex === idx && !opt.isCorrect) ? 'bg-red-50 border-l-4 border-red-600 text-red-800' : '',
                      // normal
                      (!opt.isCorrect && !(item.selectedIndex === idx && !opt.isCorrect)) ? 'bg-transparent' : ''
                    ]"
                  >
                    <div class="flex items-center justify-between">
                      <div>{{ opt.text }}</div>
                      <div class="text-sm text-gray-500">
                        <span v-if="opt.isCorrect">Bonne réponse</span>
                        <span v-else-if="item.selectedIndex === idx">Votre réponse</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="apiError" class="mt-4 text-sm text-yellow-700">
              <div v-if="Array.isArray(apiError)">
                <div v-for="(e,i) in apiError" :key="i">{{ e }}</div>
              </div>
              <div v-else>{{ apiError }}</div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </section>
</template>