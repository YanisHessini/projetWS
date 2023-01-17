import { createHead } from '@vueuse/head'

import { router } from './router'

import App from './App.vue'

import 'tailwindcss/tailwind.css'
import './styles/main.css'

createApp(App)
  .use(createHead())
  .use(router)
  .mount('#app')