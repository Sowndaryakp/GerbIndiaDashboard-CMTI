import { createRouter, createWebHashHistory } from 'vue-router';
import { RouterLink } from 'vue-router';

import Home from '../views/Home.vue';
import About from '../views/About.vue';
import admintable from '../views/admintable.vue';
import weldertable from '../views/weldertable.vue';
import machinescheduling from '../views/machinescheduling.vue';
import reporttable from '../views/reporttable.vue';
import elementMasterTable from '../views/elementMasterTable.vue';
import welderMasterTable from '../views/welderMasterTable.vue';
import projectMasterTable from '../views/projectMasterTable.vue';
import testlogin from "@/components/testlogin.vue";
import testhome from "@/components/testhome.vue";
import error404 from "@/components/error404.vue";

const routes = [
  { path: "/log", component: testlogin },
  { path: "/home", component: testhome, meta: { requiresAuth: true } },
  { path: '/', name: 'Home', component: Home, meta: { requiresAuth: true } },
  { path: '/about', name: 'About', component: About, meta: { requiresAuth: true } },
  { path: '/weldertable', name: 'Welder Table', component: weldertable, meta: { requiresAuth: true } },
  { path: '/machinescheduling', name: 'machine scheduling', component: machinescheduling, meta: { requiresAuth: true } },
  { path: '/reporttable', name: 'reporttable', component: reporttable, meta: { requiresAuth: true } },
  { path: '/elementMasterTable', name: 'elementMasterTable', component: elementMasterTable, meta: { requiresAuth: true } },
  { path: '/welderMasterTable', name: 'welderMasterTable', component: welderMasterTable, meta: { requiresAuth: true } },
  { path: '/projectMasterTable', name: 'projectMasterTable', component: projectMasterTable, meta: { requiresAuth: true } },
  { path: '/error404', name: 'error404', component: error404 },
];

const router = createRouter({
  history: createWebHashHistory(), // Use createWebHashHistory instead of createWebHistory
  routes,
});

export default router;
