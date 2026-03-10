// src/store/modules/auth.js
export default {
  state: {
    isLoggedIn: false,
    username: '',
    uid: null,
    token: null,
    refreshToken: null
  },
  mutations: {
    SET_LOGIN(state, payload) {
        state.isLoggedIn = true
        state.username = payload.username
        state.uid = payload.uid
        state.token = payload.token
        state.refreshToken = payload.refreshToken
        localStorage.setItem('token', payload.token)
        localStorage.setItem('uid', payload.uid)
        localStorage.setItem('username', payload.username)
        localStorage.setItem('refreshToken', payload.refreshToken)
    },
    SET_LOGOUT(state) {
        state.isLoggedIn = false
        state.username = ''
        state.uid = null
        state.token = null
        state.refreshToken = null
        localStorage.removeItem('token')
        localStorage.removeItem('uid')
        localStorage.removeItem('username')
        localStorage.removeItem('refreshToken')
    }
  },
  actions: {
    login({ commit }, userData) {
      commit('SET_LOGIN', userData)
    },
    logout({ commit }) {
      commit('SET_LOGOUT')
    }
  },
  getters: {
    isLoggedIn: state => state.isLoggedIn,
    username: state => state.username,
    uid: state => state.uid,
    token: state => state.token
  }
}
