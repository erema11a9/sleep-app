import { createRouter, createWebHistory } from "vue-router";
import SignIn from "../views/SignIn.vue";
import home from "../views/Home.vue" 

const routes = [
  { path: "/", component: home }, 
  { path: "/signin", component: SignIn }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
