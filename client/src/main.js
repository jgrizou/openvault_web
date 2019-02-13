import Vue from 'vue'
import App from './App.vue'
import VueSocketIO from 'vue-socket.io'
import BootstrapVue from 'bootstrap-vue'

import './../node_modules/jquery/dist/jquery.min.js'
import './../node_modules/bootstrap/dist/css/bootstrap.min.css'
import './../node_modules/bootstrap/dist/js/bootstrap.min.js'

Vue.use(new VueSocketIO({
  debug: true,
  connection: 'http://localhost:5000'
}))

Vue.use(BootstrapVue)

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  render: h => h(App)
})
