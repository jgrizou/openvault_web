import Vue from 'vue'
import VueSocketIO from 'vue-socket.io'
import App from './App.vue'
import router from './router'

Vue.use(new VueSocketIO({
  debug: false,
  connection: 'http://127.0.0.1:5000'
}))

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  render: h => h(App)
})
