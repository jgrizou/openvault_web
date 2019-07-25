import Vue from 'vue'
import VueSocketIO from 'vue-socket.io'
import App from './App.vue'
import router from './router'

Vue.use(new VueSocketIO({
  debug: false,
  connection: 'https://openvault.jgrizou.com'
}))

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  render: h => h(App)
})
