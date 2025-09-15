<script setup>
import { ref, watch } from 'vue'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'

const playerName = ref('')
const showQuiz = ref(false)

const questions = [
  {
    id: 1,
    text: "Lorem ipsum dolor sit amet consectetus est Lorem ipsum dolor sit amet consectetus est Lorem ipsum dolor sit amet consectetus est ?",
    image: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAAXNSR0IArs4c6QAAAHRJREFUGFcBaQCW/wGHA6L/7JzXAPriIQATvu4AP5TAAAFFTxT/x73EADr9uwDoc20AzULjAAGBXdX/DpyhAO1yMgACl40A0pirAAFsTTP/Zs5rAL+4sgC01XMAnxLMAAFaqY//tP3tAO88AQCwlyYAS4WkAN9MLqt2q2/jAAAAAElFTkSuQmCC",
    options: [
      "Petit texte.",
      "Un texte un peu plus long pour tester l'affichage.",
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin ac.",
      "Option très courte."
    ]
  },
  {
    id: 2,
    text: "Seconde question : lorem ipsum dolor sit amet ?",
    image: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAAXNSR0IArs4c6QAAAHRJREFUGFcBaQCW/wFFgkf/sM+MAFzjkQB1TbIA6pAUAAEaevb/AtlcAICLxwB+xLMA8xWyAAHMBMH/k1sAABBVjQAjxH4A+OUiAAFwJBD/M1/7APg1UgBtdicAc68PAAFr/5b/aUy+AK7pGgDlYV8AmqIVAPR5KgiQLIhgAAAAAElFTkSuQmCC",
    options: [
      "Réponse A",
      "Réponse B avec un texte plus long pour voir le rendu.",
      "Réponse C",
      "Encore une réponse avec beaucoup de texte pour tester le comportement du composant sur plusieurs lignes. Lorem ipsum dolor sit amet."
    ]
  },
  {
    id: 3,
    text: "Troisième question : lorem ipsum dolor sit amet ?",
    image: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAAXNSR0IArs4c6QAAAHRJREFUGFcBaQCW/wHtQnj/UydwAJeaJADFWEUAHDw3AAGX4OX/ec8xAN3F+gC0T7IAE1zSAAENAc7/kqDsAMP/xgD2zX0AxcvFAAHSVx//ribKAL/2DQBd2ywAsaXbAAFqyKX/LDjEAJeN0ABxWv0Awt6+AIHQL6w+Jg/nAAAAAElFTkSuQmCC",
    options: [
      "Réponse X",
      "Réponse Y",
      "Réponse Z",
      "Réponse W"
    ]
  },
  {
    id: 4,
    text: "Quatrième question : lorem ipsum dolor sit amet ?",
    image: "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAAXNSR0IArs4c6QAAAHRJREFUGFcBaQCW/wFoVnf/B4mwAFlfcABswHAAODk2AAGpFp//MwIaANWIIADW/T0A+OwtAAGitYH/HM5+AAP0ZwBPCGIA5Jm6AAEiZ3T/jVPnAI0NJABfFywAC4MMAAHPalX/QdakANGOzwAfomQAlqnIAPWtJxu+AkejAAAAAElFTkSuQmCC",
    options: [
      "Réponse 1",
      "Réponse 2",
      "Réponse 3",
      "Réponse 4"
    ]
  }
]

const currentQuestion = ref(0)
const answers = ref(Array(questions.length).fill(null))
const selectedOption = ref(null)

// Remet la sélection temporaire quand on change de question
watch(currentQuestion, (newIdx) => {
  selectedOption.value = answers.value[newIdx]
})

/**
 * Enregistre la réponse et passe à la question suivante
 */
function nextQuestion() {
  answers.value[currentQuestion.value] = selectedOption.value
  if (currentQuestion.value < questions.length - 1) {
    currentQuestion.value++
  }
}

/**
 * Va à la question spécifiée si elle a déjà été répondue
 */
function goToQuestion(idx) {
  if (answers.value[idx] !== null) {
    currentQuestion.value = idx
  }
}

/**
 * Démarre le quiz si un nom d'utilisateur a été saisi
 */
function startQuiz() {
  if (playerName.value.trim() !== '') {
    showQuiz.value = true
    currentQuestion.value = 0
    answers.value = Array(questions.length).fill(null)
    selectedOption.value = null
  }
}
</script>

<template>
  <section class="flex flex-col items-center justify-center min-h-screen bg-white">
    <div v-if="!showQuiz" class="flex flex-col items-center space-y-6">
      <h1 class="text-3xl font-semibold mb-4">Prêt pour le meilleur quiz de tout les temps ?</h1>
      <input
        v-model="playerName"
        type="text"
        placeholder="Nom d'utilisateur ..."
        class="rounded-lg px-6 py-3 bg-gray-100 text-xl placeholder-gray-400 focus:outline-none"
        style="min-width: 320px;"
      />
      <Button
        class="bg-gray-300 text-xl px-8 py-2 mt-2"
        :disabled="playerName.trim() === ''"
        @click="startQuiz"
      >
        C'est parti !
      </Button>
    </div>

    <div v-else class="w-full">
      <section class="flex flex-row p-12 space-x-8 items-start">
        <!-- Bloc réponse aux questions -->
        <Card class="flex-1 max-w-2xl bg-gray-100">
          <CardHeader>
            <CardTitle class="text-2xl mb-2">Lorem ipsum dolor (Theme du quiz)</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="mb-4">
              <div class="font-semibold mb-1">Question N°{{ currentQuestion + 1 }}</div>
              <img
                v-if="questions[currentQuestion].image"
                :src="questions[currentQuestion].image"
                alt="illustration"
                class="w-full max-h-64 object-cover rounded my-4"
              />
              <div class="mb-4">{{ questions[currentQuestion].text }}</div>
              <RadioGroup v-model="selectedOption" class="space-y-4">
                <div
                  v-for="(option, idx) in questions[currentQuestion].options"
                  :key="idx"
                  class="flex items-center space-x-4"
                >
                  <RadioGroupItem
                    :value="idx"
                    :id="'option-' + idx"
                    class="w-6 h-6 border-2 border-gray-300"
                  />
                  <label :for="'option-' + idx" class="text-base cursor-pointer w-full">
                    {{ option }}
                  </label>
                </div>
              </RadioGroup>
            </div>
            <div class="flex justify-center mt-8">
              <Button
                class="bg-gray-300 text-xl px-8 py-2"
                :disabled="selectedOption === null"
                @click="nextQuestion"
              >
                Suivant <span class="ml-2 text-2xl">→</span>
              </Button>
            </div>
          </CardContent>
        </Card>

        <!-- Bloc navigation questions -->
        <Card class="w-72 bg-gray-100">
          <CardHeader>
            <CardTitle class="text-lg">Questions</CardTitle>
          </CardHeader>
          <CardContent class="space-y-3">
            <div
              v-for="(q, idx) in questions"
              :key="q.id"
              class="flex items-center justify-between px-4 py-3 rounded-lg transition-all"
              :class="{
                'bg-gray-200 text-gray-400 cursor-not-allowed': answers[idx] === null,
                'bg-white hover:bg-blue-100 cursor-pointer': answers[idx] !== null
              }"
              @click="goToQuestion(idx)"
            >
              <span>Question N°{{ idx + 1 }}</span>
              <span v-if="answers[idx] !== null" class="w-3 h-3 bg-green-700 rounded-full inline-block"></span>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  </section>
</template>