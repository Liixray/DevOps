<script setup>
import Leaderboard from '@/components/ui/Leaderboard.vue'
import { getQuestionsCount } from '@/services/questions'
import { ref, onMounted } from 'vue'

const totalQuestions = ref(0)

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
onMounted(fetchTotalQuestions)
</script>

<template>
  <section class="min-h-screen flex items-center justify-center bg-white p-4">
    <div class="w-full max-w-3xl mx-auto py-12">
      <Leaderboard
        :total-questions="totalQuestions"
        title="Classement général"
        :initial-items-per-page="10"
        :items-per-page-options="[10, 20, 50]"
      />
    </div>
  </section>
</template>
