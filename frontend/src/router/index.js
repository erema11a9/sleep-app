import { createRouter, createWebHistory } from "vue-router";
import SignUp from "../views/SignUp.vue";
import SignIn from "../views/SignIn.vue";
import Home from "@/views/Home.vue";
import AboutUs from "@/views/AboutUs.vue";

const routes = [
    { path: "/", component: Home },
    { path: "/sign-up", component: SignUp },
    { path: "/about-us", component: AboutUs },
    { path: "/sign-in", component: SignIn },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
