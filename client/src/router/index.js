import Vue from 'vue'
import Router from 'vue-router'
import LevelSelection from './../pages/LevelSelection'
import UI from './../pages/UI'

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
      name: 'UI',
      component: UI
    }
  ]
})
