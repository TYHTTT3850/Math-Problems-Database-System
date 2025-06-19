import { createApp } from 'vue'
import App from './App.vue'

// Element Plus
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import router from './router'

// 引入 axios 配置
import http from './api'

const app = createApp(App)

// 使用 Element Plus 插件
app.use(ElementPlus)

// 使用路由
app.use(router)

// 将 axios 挂载到全局
app.config.globalProperties.$axios = http

// 挂载到 #app
app.mount('#app')
