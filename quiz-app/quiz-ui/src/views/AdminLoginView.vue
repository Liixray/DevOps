<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { loginAdmin } from '@/services/auth'
import { validateAdminToken } from '@/services/auth'

const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)
const showPlaceholder = ref(true)
const router = useRouter()

async function submit() {
  error.value = ''
  success.value = false
  loading.value = true
  try {
    const token = await loginAdmin(password.value)
    localStorage.setItem('admin_token', token)
    success.value = true
    password.value = ''
    router.push('/admin/dashboard') 
  } catch (e) {
    error.value = "Mot de passe incorrect"
  } finally {
    loading.value = false
  }
}

async function checkAdminToken() {
  const token = localStorage.getItem('admin_token');
  if (token) {
    try {
      const isValid = await validateAdminToken(token);
      if (isValid) {
        router.push('/admin/dashboard');
      }
    } catch (e) {
      console.error('Token validation failed', e);
    }
  }
}

onMounted(() => {
  checkAdminToken();
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-muted">
    <Card class="w-[340px] sm:w-[380px] shadow border-none">
      <CardHeader class="pb-0">
        <CardTitle class="text-center text-[42px] tracking-tight">Connexion</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="submit" class="mt-12 flex flex-col space-y-6">
          <Input
            v-model="password"
            :disabled="loading"
            type="password"
            :placeholder="showPlaceholder ? 'Mot de passe' : ''"
            @focus="showPlaceholder = false"
            @blur="!password && (showPlaceholder = true)"
            class="h-12 rounded-xl text-center text-base border-none focus-visible:ring-primary"
          />
          <Button
            type="submit"
            :disabled="loading || !password"
            class="h-12 rounded-xl text-base font-medium shadow-sm disabled:opacity-60 flex items-center justify-center gap-2"
          >
            <span v-if="!loading">Se connecter</span>
            <span v-else class="flex items-center gap-2">
              <svg class="animate-spin h-5 w-5 text-current" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/>
              </svg>
            </span>
          </Button>

          <p v-if="error" class="text-center text-sm text-red-600">{{ error }}</p>
          <p v-if="success" class="text-center text-sm text-green-600">
            Connecté. Jeton stocké.
          </p>
        </form>
      </CardContent>
    </Card>
  </div>
</template>