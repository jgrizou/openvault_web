import Vue from 'vue'
import Router from 'vue-router'
import Test from './../pages/Test'
import Test2 from './../pages/Test2'
import V1 from './../pages/V1'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'V1',
      component: V1
    },
    {
      path: '/test',
      name: 'Test',
      component: Test
    },
    {
      path: '/test2',
      name: 'Test2',
      component: Test2
    }
  ]
})
