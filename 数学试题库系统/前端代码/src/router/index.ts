// src/router/index.ts
import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";
const LogRes = () => import("../components/LoginRegister.vue");
const user = () => import("../components/MainWindow.vue");

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    component: LogRes,
    meta: {
      title: "登录",
    },
  },
  {
    path: "/user",
    component: user,
    meta: {
      title: "用户界面",
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
