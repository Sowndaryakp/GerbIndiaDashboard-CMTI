// main.js

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from './axios';
import PrimeVue from 'primevue/config';
import VueApexCharts from 'vue-apexcharts';
import '@fortawesome/fontawesome-free/css/all.css';
import CanvasJSChart from '@canvasjs/vue-charts';
import html2pdf from 'html2pdf.js';

// Importing and applying the Tailwind CSS and Font Awesome styles
import 'tailwindcss/tailwind.css';

const app = createApp(App);

// Configure global properties
app.config.globalProperties.$axios = axios;
axios.defaults.baseURL = "http://192.168.0.105:6969";

// Use plugins
app.use(CanvasJSChart, router);
app.use(router);
app.use(PrimeVue);
app.component('apexchart', VueApexCharts);
// Global navigation guard to check if the user is authenticated before accessing protected routes
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem("authToken");
  console.log("autenticatioooooom")
  console.log(isAuthenticated)
  console.log(to.meta)
  console.log(to.meta.requiresAuth)
  console.log(!isAuthenticated)

  if (to.meta.requiresAuth && !isAuthenticated) {
    // If the route requires authentication and the user is not authenticated, redirect to the login page
    console.log("iside function")
    console.log(to.meta.requiresAuth)
    console.log(!isAuthenticated)
    next("/error404");
  } else {
    next();
  }
});

app.mount('#app');
