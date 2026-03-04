import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import OtherLogin from '../views/OtherLogin.vue'
import HotDebates from '../views/HotDebates.vue'
import AddDebateTopic from '../views/AddDebateTopic.vue'
import AddDebateDetail from '../views/AddDebateDetail.vue'
import DebateView from '../views/DebateView.vue'
import UserProfile from '../views/UserProfile.vue'
import Discover from '../views/Discover.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/other-login',
    name: 'OtherLogin',
    component: OtherLogin
  },
  {
    path: '/hot-debates',
    name: 'HotDebates',
    component: HotDebates
  },
  {
    path: '/add-debate-topic',
    name: 'AddDebateTopic',
    component: AddDebateTopic
  },
  {
    path: '/add-debate-detail',
    name: 'AddDebateDetail',
    component: AddDebateDetail
  },
  {
    path: '/debate',
    name: 'DebateView',
    component: DebateView
  },
  {
    path: '/user-profile',
    name: 'UserProfile',
    component: UserProfile
  },
  {
    path: '/discover',
    name: 'Discover',
    component: Discover
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
