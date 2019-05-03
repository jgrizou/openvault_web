import Vue from 'vue'
import Router from 'vue-router'
import LevelSelection from './../pages/LevelSelection'
import SPA from './../pages/SPA'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LevelSelection',
      component: LevelSelection
    },
    {
      path: '/ui/*',
      name: 'SPA',
      component: SPA
    }
  ]
})
