import Vue from 'vue'
import Router from 'vue-router'
import PasswordUI from './../pages/PasswordUI'
import LevelSelection from './../pages/LevelSelection'
import Test from './../pages/Test'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LevelSelection',
      component: LevelSelection
    },
    {
      path: '/*',
      name: 'PasswordUI',
      component: PasswordUI
    }
  ]
})
