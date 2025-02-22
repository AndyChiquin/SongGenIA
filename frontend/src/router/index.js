import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import LoginForm from "@/components/LoginForm.vue";
import RegisterForm from "@/components/RegisterForm.vue";

const routes = [
  { path: "/", component: HomeView },
  { path: "/login", component: LoginForm },
  { path: "/register", component: RegisterForm },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
