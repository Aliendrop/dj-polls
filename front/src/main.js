import Vue from 'vue'
import App from './App.vue'
import store from './store'
import axios from './http'

Vue.config.productionTip = false
Vue.prototype.$http = axios

new Vue({
  store,
  render: h => h(App),
}).$mount('#app')
