import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import OtherLogin from '../views/OtherLogin.vue'
import HotDebates from '../views/HotDebates.vue'
import AddDebateTopic from '../views/AddDebateTopic.vue'
import DebateView from '../views/DebateView.vue'
import UserProfile from '../views/UserProfile.vue'
import Discover from '../views/Discover.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
    meta: { public: true }  // 公开访问，不需要登录
  },
  {
    path: '/other-login',
    name: 'OtherLogin',
    component: OtherLogin,
    meta: { public: true }  // 公开访问，不需要登录
  },
  {
    path: '/hot-debates',
    name: 'HotDebates',
    component: HotDebates,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/add-debate-topic',
    name: 'AddDebateTopic',
    component: AddDebateTopic,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/debate',
    name: 'DebateView',
    component: DebateView,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true }  // 需要登录
  },
  {
    path: '/discover',
    name: 'Discover',
    component: Discover,
    meta: { requiresAuth: true }  // 需要登录
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 - 检查登录状态
router.beforeEach((to, from, next) => {
  // 检查是否有token（登录状态）
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token

  // 如果路由需要登录，但用户未登录
  if (to.meta.requiresAuth && !isAuthenticated) {
    console.log('需要登录，重定向到登录页面')
    next({
      path: '/',
      query: { redirect: to.fullPath }  // 保存原本要访问的路径
    })
    return
  }

  // 如果用户已登录，但访问登录页面，则跳转到首页
  if (to.meta.public && isAuthenticated && to.path === '/') {
    console.log('已登录，重定向到热点辩论页面')
    next({ path: '/hot-debates' })
    return
  }

  // 其他情况正常放行
  next()
})

// 路由错误处理
router.onError((error) => {
  console.error('路由错误:', error)
})

export default router
