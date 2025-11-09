import { createRouter, createWebHistory } from 'vue-router'
import AdminLoginView from '@/views/AdminLoginView.vue'
import UserLoginView from '@/views/UserLoginView.vue'
import UserRegisterView from '@/views/UserRegisterView.vue'
import HomePage from '../views/HomePage.vue'
import AdminDashboardView from '@/views/AdminDashboardView.vue'
import LeaderboardView from '@/views/LeaderboardView.vue'
import { validateAdminToken } from '@/services/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/admin/login',
      name: 'admin-login',
      component: AdminLoginView,
    },
    {
      path: '/user/login',
      name: 'user-login',
      component: UserLoginView,
    },
    {
      path: '/user/register',
      name: 'user-register',
      component: UserRegisterView,
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: AdminDashboardView,
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: LeaderboardView,
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  if (to.name === 'admin-dashboard') {
    const isValid = await validateAdminToken()
    if (!isValid) {
      return next({ name: 'admin-login' })
    }
  }
  next()
})

export default router
