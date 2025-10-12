import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AdminLoginView from '@/views/AdminLoginView.vue'
import UserLoginView from '@/views/UserLoginView.vue'
import UserRegisterView from '@/views/UserRegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
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
  ],
})

export default router
