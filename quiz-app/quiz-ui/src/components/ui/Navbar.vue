<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goTo(route) {
  router.push(route)
}
</script>

<template>
  <nav class="border-b border-border">
    <div class="container mx-auto px-4 py-3 flex justify-between items-center">
      <div class="text-2xl font-bold text-green-600 cursor-pointer" @click="goTo('/')">
        Quizz App
      </div>

      <div class="flex gap-4">
        <span class="text-xl text-green-600 cursor-pointer font-medium" @click="goTo('/admin/login')">Admin</span>
        <span class="text-xl text-green-600 cursor-pointer font-medium" @click="goTo('/leaderboard')">Leaderboard</span>
      </div>
    </div>
  </nav>
</template>

<style scoped>
nav {
  width: 100%;
}

span {
  transition: color 0.3s;
}

span:hover {
  color: #064632;
}
</style>