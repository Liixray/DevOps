<script setup>
import { ref } from 'vue'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { loginUser } from '@/services/auth'

const mail = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)

const showMailPh = ref(true)
const showPwdPh = ref(true)

async function submit() {
  error.value = ''
  success.value = false
  loading.value = true
  try {
    const token = await loginUser(mail.value, password.value)
    localStorage.setItem('user_token', token)
    success.value = true
    password.value = ''
  } catch (e) {
    error.value = e.message || 'Identifiants invalides'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-muted">
    <Card class="w-[340px] sm:w-[380px] shadow border-none">
      <CardHeader class="pb-0">
        <CardTitle class="text-center text-[42px] tracking-tight">Connexion</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="submit" class="mt-12 flex flex-col space-y-4">
          <Input
            v-model="mail"
            type="email"
            :disabled="loading"
            :placeholder="showMailPh ? 'Email' : ''"
            @focus="showMailPh = false"
            @blur="!mail && (showMailPh = true)"
            class="h-12 rounded-xl text-center text-base border-none focus-visible:ring-primary"
          />
          <Input
            v-model="password"
            type="password"
            :disabled="loading"
            :placeholder="showPwdPh ? 'Mot de passe' : ''"
            @focus="showPwdPh = false"
            @blur="!password && (showPwdPh = true)"
            class="h-12 rounded-xl text-center text-base border-none focus-visible:ring-primary"
          />
          <Button
            type="submit"
            :disabled="loading || !mail || !password"
            class="h-12 rounded-xl text-base font-medium shadow-sm disabled:opacity-60 flex items-center justify-center gap-2"
          >
            <span v-if="!loading">Se connecter</span>
            <span v-else class="flex items-center gap-2">
              <svg class="animate-spin h-5 w-5 text-current" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
              </svg>
              <span>Connexion...</span>
            </span>
          </Button>

          <p v-if="error" class="text-center text-sm text-red-600">{{ error }}</p>
          <p v-if="success" class="text-center text-sm text-green-600">Connecté.</p>
        </form>
      </CardContent>
      <CardFooter class="justify-center text-xs text-muted-foreground">
        Utilisateur
      </CardFooter>
    </Card>
  </div>
</template>