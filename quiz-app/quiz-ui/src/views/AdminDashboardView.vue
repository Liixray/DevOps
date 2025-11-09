<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { validateAdminToken } from '@/services/auth'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { getQuestion, getQuestionsCount, updateQuestion, createQuestion, deleteQuestion } from '@/services/questions'
import QuestionModal from './QuestionModal.vue'

const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('admin_token')
  if (token) {
    const isValid = await validateAdminToken()
    if (!isValid) {
      router.push('/admin/login')
    }
  } else {
    router.push('/admin/login')
  }
})

async function handleDeleteQuestion(q) {
  if (!window.confirm('Voulez-vous vraiment supprimer cette question ?')) return
  loading.value = true
  error.value = ''
  try {
    await deleteQuestion(q.id)
    await fetchQuestions()
  } catch (e) {
    error.value = 'Erreur lors de la suppression : ' + e.message
  } finally {
    loading.value = false
  }
}

const questions = ref([])
const quizSize = ref(0)
const loading = ref(false)
const error = ref('')

const modalOpen = ref(false)
const modalEdit = ref(false)
const modalQuestion = ref(null)

async function fetchQuestions() {
  loading.value = true
  error.value = ''
  try {
    const info = await getQuestionsCount()
    quizSize.value = info.size
    const arr = []
    for (let i = 0; i < quizSize.value; i++) {
      arr.push(await getQuestion(i))
    }
    questions.value = arr
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchQuestions)

function handleAddQuestion() {
  modalEdit.value = false
  modalQuestion.value = null
  modalOpen.value = true
}

function handleEditQuestion(q) {
  modalEdit.value = true
  modalQuestion.value = q
  modalOpen.value = true
}

async function handleSaveQuestion(data) {
  try {
    if (modalEdit.value) {
      await updateQuestion(modalQuestion.value.id, data)
    } else {
      await createQuestion(data)
    }
    modalOpen.value = false
    await fetchQuestions()
  } catch (e) {
    error.value = 'Erreur lors de la sauvegarde : ' + e.message
  }
}

function handleCloseModal() {
  modalOpen.value = false
}

async function handleUpdatePosition(qIdx, newPos) {
  newPos = Number(newPos)
  const oldPos = questions.value[qIdx].position
  if (oldPos === newPos) return
  const swapIdx = questions.value.findIndex(q => q.position === newPos)
  if (swapIdx === -1) return
  const temp = questions.value[qIdx].position
  questions.value[qIdx].position = questions.value[swapIdx].position
  questions.value[swapIdx].position = temp
  try {
    await Promise.all([
      updateQuestion(questions.value[qIdx].id, { position: questions.value[qIdx].position }),
      updateQuestion(questions.value[swapIdx].id, { position: questions.value[swapIdx].position })
    ])
  } catch (e) {
    error.value = 'Erreur lors du changement de position : ' + e.message
  }
  questions.value.sort((a, b) => a.position - b.position)
}

function logout() {
  localStorage.removeItem('admin_token');
  router.push('/admin/login');
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold">Gestion des questions du quiz</h1>
      <Button class="bg-red-500 text-white hover:bg-red-600" @click="logout">Se déconnecter</Button>
    </div>
    <div v-if="loading" class="text-center my-8">Chargement…</div>
    <div v-else-if="error" class="text-red-500 my-8">{{ error }}</div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
      <QuestionModal
        :open="modalOpen"
        :question="modalEdit ? modalQuestion : null"
        :onClose="handleCloseModal"
        :onSave="handleSaveQuestion"
        :quizSize="quizSize"
      />
      <Card class="flex flex-col items-center justify-center cursor-pointer hover:bg-green-100 transition" @click="handleAddQuestion">
        <CardHeader class="flex items-center justify-center">
          <span class="text-5xl text-green-500">+</span>
        </CardHeader>
        <CardContent>
          <div class="text-center text-lg font-semibold">Ajouter une question</div>
        </CardContent>
      </Card>
      <Card v-for="(q, idx) in questions" :key="q.id" class="relative">
        <CardHeader class="flex justify-between items-center">
          <CardTitle class="text-lg">{{ q.title || 'Sans titre' }}</CardTitle>
          <select
            class="absolute top-4 right-4 bg-gray-200 rounded px-2 py-1 text-sm"
            :value="q.position"
            @change="handleUpdatePosition(idx, $event.target.value)"
          >
            <option v-for="pos in quizSize" :key="pos" :value="pos">{{ pos }}</option>
          </select>
        </CardHeader>
        <CardContent>
          <div class="mb-2 text-gray-700">{{ q.text }}</div>
          <ul class="mb-2">
            <li
              v-for="(a, i) in q.possibleAnswers"
              :key="a.id"
              class="flex items-center gap-2 px-3 py-2 rounded-lg"
              :class="a.isCorrect ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'"
            >
              <span class="text-xl mr-2">{{ ['①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩'][i] }}</span>
              <span class="font-medium">{{ a.text }}</span>
            </li>
          </ul>
          <img v-if="q.image && q.image !== 'falseb64imagecontent'" :src="q.image" alt="illustration" class="w-full max-h-32 object-cover rounded mb-2" />
        </CardContent>
        <CardFooter class="flex justify-end gap-2">
          <Button size="sm" class="bg-green-500 text-white hover:bg-green-600" @click="handleEditQuestion(q)">Modifier</Button>
          <Button size="sm" class="bg-red-500 text-white hover:bg-red-600" @click="() => handleDeleteQuestion(q)">Supprimer</Button>
        </CardFooter>
      </Card>
    </div>
  </div>
</template>
