import { createRouter, createWebHistory } from 'vue-router';
import { RouterLink } from 'vue-router';

import Home from '../views/Home.vue';
import About from '../views/About.vue';
import admintable from '../views/admintable.vue';
import weldertable from '../views/weldertable.vue';
import machinescheduling from '../views/machinescheduling.vue';
import reporttable from '../views/reporttable.vue';
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/about',
    name: 'About',
    component: About,
  },
  {
    path: '/admintable',
    name: 'admintable', // Make sure the name matches
    component: () => import('@/views/admintable.vue') // Your AdminTable component path
  },
  {
    path: '/weldertable',
    name: 'Welder Table',
    component: weldertable,
  },
  {
    path: '/machinescheduling',
    name: 'machine scheduling',
    component: machinescheduling,
  },
  {
    path: '/reporttable',
    name: 'reporttable',
    component: reporttable,
  },
  // Add other routes here if needed
  // {
  //   path: '/data-table',
  //   name: 'DataTable',
  //   component: DataTable,
  // },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
