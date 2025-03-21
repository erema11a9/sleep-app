import { createRouter, createWebHistory } from "vue-router";
import SignIn from "../views/SignIn.vue"; 

const routes = [
  { path: "/", component: SignIn }, 
  { path: "/signin", component: SignIn }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
