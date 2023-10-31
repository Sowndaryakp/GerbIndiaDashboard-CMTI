import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from './axios';
import PrimeVue from 'primevue/config';

import '@fortawesome/fontawesome-free/css/all.css';
import CanvasJSChart from '@canvasjs/vue-charts';
import html2pdf from 'html2pdf.js';

// Importing and applying the Tailwind CSS and Font Awesome styles
import 'tailwindcss/tailwind.css';



const app = createApp(App);
app.config.globalProperties.$axios = axios;
app.use(CanvasJSChart,router);
app.use(router) // install the CanvasJS Vuejs Chart Plugin
app.mount('#app');
app.use(PrimeVue);