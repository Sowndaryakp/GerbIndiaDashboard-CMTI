import { createRouter, createWebHistory } from 'vue-router';
import { RouterLink } from 'vue-router';

import Home from '../views/Home.vue';
import About from '../views/About.vue';
import admintable from '../views/admintable.vue';
import weldertable from '../views/weldertable.vue';
import machinescheduling from '../views/machinescheduling.vue';
import reporttable from '../views/reporttable.vue';

import testlogin from "@/components/testlogin.vue";
import testhome from "@/components/testhome.vue";
import error404 from "@/components/error404.vue";

//authorization lock 
//meta: { requiresAuth: true }

const routes = [
  { path: "/log", component: testlogin },
  { path: "/home", component: testhome,meta: { requiresAuth: true } },
  {
    path: '/',
    name: 'Home',
    component: Home,meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'About',
    component: About,meta: { requiresAuth: true }
  },
  {
    path: '/admintable',
    name: 'admintable', // Make sure the name matches
    component: admintable,meta: { requiresAuth: true }
  },
  // {
  //   path: '/admintable',
  //   name: 'admintable', // Make sure the name matches
  //   component: () => import('@/views/admintable.vue',) // Your AdminTable component path
  // },
  {
    path: '/weldertable',
    name: 'Welder Table',
    component: weldertable,meta: { requiresAuth: true }
  },
  {
    path: '/machinescheduling',
    name: 'machine scheduling',
    component: machinescheduling,meta: { requiresAuth: true }
  },
  {
    path: '/reporttable',
    name: 'reporttable',
    component: reporttable,meta: { requiresAuth: true }
  },
  {
    path: '/error404',
    name: 'error404',
    component: error404,
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
