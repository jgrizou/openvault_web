import 'bootstrap/dist/css/bootstrap.css'
import BootstrapVue from 'bootstrap-vue'
import Vue from 'vue'
import VueSocketIO from 'vue-socket.io'
import App from './App.vue'
import router from './router'

Vue.use(new VueSocketIO({
  debug: false,
  // connection: 'http://11.1.194.39:5000'
  // connection: 'http://150.10.147.98:5000'
  connection: 'http://localhost:5000'
}))

Vue.use(BootstrapVue)

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  render: h => h(App)
})
