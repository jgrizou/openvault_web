import Vue from 'vue'
import Router from 'vue-router'
import PasswordUI from './../pages/PasswordUI'
import LevelSelection from './../pages/LevelSelection'
import VaultControl from './../pages/VaultControl'

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
      name: 'PasswordUI',
      component: PasswordUI
    },
    {
      path: '/vaultcontrol',
      name: 'VaultControl',
      component: VaultControl
    }
  ]
})
