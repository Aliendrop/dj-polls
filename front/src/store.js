import Vue from 'vue'
import Vuex from 'vuex'
import polls from '@/storeModules/polls'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    test: 'test',
  },
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    polls,
  },
})
