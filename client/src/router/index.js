import Vue from 'vue'
import Router from 'vue-router'
import LevelSelection from './../pages/LevelSelection'
import UI from './../pages/UI'
import LandingPage from './../pages/LandingPage'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/level-selection',
      name: 'LevelSelection',
      component: LevelSelection
    },
    {
      path: '/ui/*',
      name: 'UI',
      component: UI
    },
    {
      path: '/',
      name: 'LandingPage',
      component: LandingPage
    }
  ]
})
