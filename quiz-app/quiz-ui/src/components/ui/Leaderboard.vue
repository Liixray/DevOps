<script setup>
import { ref, onMounted, watch } from 'vue'
import { getLeaderboard } from '@/services/leaderboard'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'

const props = defineProps({
  totalQuestions: { type: Number, required: true },
  title: { type: String, default: 'Classement général' },
  initialItemsPerPage: { type: Number, default: 10 },
  itemsPerPageOptions: { type: Array, default: () => [10, 20, 50] }
})

const itemsPerPage = ref(props.initialItemsPerPage)
const leaderboard = ref([])
const page = ref(1)
const totalPages = ref(1)
const loading = ref(false)

async function fetchLeaderboardData() {
  loading.value = true
  try {
    const response = await getLeaderboard(page.value, itemsPerPage.value)
    if (response?.data) {
      leaderboard.value = response.data
      totalPages.value = response.totalPages || 1
    } else {
      leaderboard.value = []
      totalPages.value = 1
    }
  } catch {
    leaderboard.value = []
    totalPages.value = 1
  } finally {
    loading.value = false
  }
}

function changePage(direction) {
  if (direction === 'next' && page.value < totalPages.value) {
    page.value++
    fetchLeaderboardData()
  } else if (direction === 'prev' && page.value > 1) {
    page.value--
    fetchLeaderboardData()
  }
}

function getRank(index) {
  return (page.value - 1) * itemsPerPage.value + index + 1
}

onMounted(fetchLeaderboardData)

watch(itemsPerPage, () => {
  page.value = 1
  fetchLeaderboardData()
})
</script>

<template>
  <Card class="w-full max-w-lg border border-gray-300 rounded-lg bg-white">
    <div class="p-6 border-b border-gray-200 flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <h2 class="text-xl font-semibold text-center sm:text-left">{{ title }}</h2>
      <div class="mt-4 sm:mt-0">
        <label class="text-sm text-gray-600 mr-2">Éléments par page :</label>
        <select v-model="itemsPerPage" class="border border-gray-300 rounded px-2 py-1 text-sm">
          <option v-for="opt in itemsPerPageOptions" :key="opt" :value="opt">{{ opt }}</option>
        </select>
      </div>
    </div>

    <CardContent class="p-6">
      <div v-if="loading" class="text-center py-8 text-gray-600">Chargement du classement...</div>
      <div v-else-if="leaderboard.length === 0" class="text-center py-8 text-gray-500">Aucune participation pour le moment. Soyez le premier !</div>
      <div v-else class="space-y-3">
        <div
          v-for="(participant, index) in leaderboard"
          :key="participant.id || index"
          class="flex items-center justify-between px-5 py-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
        >
          <div class="flex items-center gap-4">
            <span class="text-2xl font-handwriting text-gray-600 min-w-[2.5rem] text-center">
              {{ getRank(index) }}
            </span>
            <span class="text-lg">{{ participant.playerName || participant.name || 'Anonyme' }}</span>
          </div>
          <span class="font-medium text-gray-700">{{ participant.score }}/{{ props.totalQuestions || '?' }}</span>
        </div>

        <div v-if="totalPages > 1" class="flex justify-center items-center gap-4 pt-6 mt-4 border-t border-gray-200">
          <Button @click="changePage('prev')" :disabled="page === 1" class="px-4 py-2">← Précédent</Button>
          <span class="text-sm text-gray-600">Page {{ page }} / {{ totalPages }}</span>
          <Button @click="changePage('next')" :disabled="page >= totalPages" class="px-4 py-2">Suivant →</Button>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
