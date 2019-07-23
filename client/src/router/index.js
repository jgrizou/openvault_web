import Vue from 'vue'
import Router from 'vue-router'
import LevelSelection from './../pages/LevelSelection'
import UI from './../pages/UI'
import Embed from './../pages/Embed'

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
    },
    {
      path: '/embed',
      name: 'embed',
      component: Embed
    }
  ]
})
