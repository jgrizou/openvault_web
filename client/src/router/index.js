import Vue from 'vue'
import Router from 'vue-router'
import V1 from './../pages/V1'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'V1',
      component: V1
    }
  ]
})
