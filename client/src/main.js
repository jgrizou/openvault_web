import Vue from 'vue'
import App from './App.vue'
import VueSocketIO from 'vue-socket.io'

Vue.use(new VueSocketIO({
  debug: true,
  connection: 'http://localhost:5000'
}))

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  render: h => h(App)
})
