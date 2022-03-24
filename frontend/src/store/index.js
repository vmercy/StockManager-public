import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        searchTerm: '',
        token: '',
        username: '',
        isAuthenticated: false,
        darkMode: false
    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('token') && localStorage.getItem('username')) {
                state.token = localStorage.getItem('token')
                state.username = localStorage.getItem('username')
                state.isAuthenticated = true
            } else {
                state.token = ''
                state.isAuthenticated = false
            }
        },
        setToken(state, token) {
            state.token = token
            state.isAuthenticated = true
        },
        removeToken(state) {
            state.token = ''
            state.isAuthenticated = false
            localStorage.removeItem('token')
            localStorage.removeItem('username')
        }
    },
    actions: {},
    modules: {}
})