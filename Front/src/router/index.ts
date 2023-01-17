import { createRouter, createWebHistory } from 'vue-router'
import routes from '~pages'

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, _, next) => {
  next()
})