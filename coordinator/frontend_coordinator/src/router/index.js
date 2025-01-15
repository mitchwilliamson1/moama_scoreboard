import { createRouter, createWebHistory } from 'vue-router'
import Coordinator from '../views/Coordinator.vue'

const routes = [
  {
    path: '/',
    name: 'Coordinator',
    component: Coordinator
  },
    {
    path: '/players',
    name: 'Players',
    component: () => import('../views/PlayersView.vue')
  },
  {
    path: '/clubs',
    name: 'Clubs',
    component: () => import('../views/ClubsView.vue')
  },
  {
    path: '/rinks',
    name: 'Rinks',
    component: () => import('../views/RinkManager.vue')
  },
  {
    path: '/bigboard',
    name: 'Big Board',
    component: () => import('../views/BigBoard.vue')
  },
  {
    path: '/support',
    name: 'Support',
    component: () => import('../views/Support.vue')
  },
]

const router = createRouter({
  mode: 'history',
  history: createWebHistory('/#'),
  routes
})

export default router
