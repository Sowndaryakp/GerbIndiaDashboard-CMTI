// src/store/index.js
import { createStore } from 'vuex';

export default createStore({
  state: {
    isAuthenticated: !!localStorage.getItem("authToken"),
    userToken: localStorage.getItem("authToken"),
  },
  mutations: {
    setAuth(state, { isAuthenticated, userToken }) {
      state.isAuthenticated = isAuthenticated;
      state.userToken = userToken;
    },
  },
  actions: {
    login({ commit }, userToken) {
      commit('setAuth', { isAuthenticated: true, userToken });
    },
    logout({ commit }) {
      localStorage.removeItem("authToken");
      commit('setAuth', { isAuthenticated: false, userToken: null });
    },
  },
  modules: {},
});

