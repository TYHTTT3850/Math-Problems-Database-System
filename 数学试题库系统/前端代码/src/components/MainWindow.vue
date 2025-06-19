<template>
    <div>
        <div class="body">
            <!-- 左侧导航栏 -->
            <div class="liner">
                <el-menu
                        :default-active="active"
                        class="el-menu-vertical-demo"
                        background-color="#eeeae7"
                        text-color="#000000"
                        active-text-color="#000000"
                        @select="handleSelect"
                >
                    <el-menu-item index="1">
                        <i class="el-icon-menu"></i>
                        <span>浏览题目</span>
                    </el-menu-item>

                    <el-menu-item index="2">
                        <i class="el-icon-user"></i>
                        <span>个人信息</span>
                    </el-menu-item>

                    <el-menu-item index="3">
                        <i class="el-icon-lock"></i>
                        <span>修改密码</span>
                    </el-menu-item>

                    <el-menu-item index="4">
                        <i class="el-icon-lock"></i>
                        <span>上传题目</span>
                    </el-menu-item>
                </el-menu>
            </div>

            <!-- 右侧内容区域 -->
            <div class="main">
                <QuestionViewer v-show="active === '1'" ref="questionViewerRef"/>
                <IndividualMessage v-show="active === '2'"/>
                <ChangePassword v-show="active === '3'"/>
                <!-- ADDED: 监听 UploadProblems 组件发射的 problemUploaded 事件 -->
                <UploadProblems v-show="active === '4'" @problemUploaded="handleProblemUploaded"/>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'

import QuestionViewer from './QuestionViewer.vue'
import IndividualMessage from './IndividualMessage.vue'
import ChangePassword from './ChangePassword.vue'
import UploadProblems from "./UploadProblems.vue"

const active = ref('1')

// ADDED: 使用 any 类型解决 TS 的类型报错
const questionViewerRef = ref<any>(null)

function handleSelect(index: string) {
    active.value = index
}

// ADDED: 当 UploadProblems 上传成功后，调用 QuestionViewer 的 refreshProblems 方法刷新题目列表
function handleProblemUploaded() {
  if (questionViewerRef.value && typeof questionViewerRef.value.refreshProblems === 'function') {
    questionViewerRef.value.refreshProblems()
  } else {
    console.warn("无法调用 refreshProblems 方法，请确认 QuestionViewer 组件中已正确暴露该方法。")
  }
}
</script>

<style>
.body {
    width: 100%;
    height: 648px;
    display: flex;
    justify-content: flex-start; /* 让左侧导航栏和右侧内容对齐 */
    align-items: stretch; /* 让子元素高度一致 */
    padding: 20px; /* 增加整体内边距 */
}

/* 左侧导航栏 */
.liner {
    width: 15%;
    min-height: 648px; /* 让 liner 至少和 body 一样高 */
    background-color: #eeeae7;
    border-radius: 15px; /* 设置圆角 */
    margin-right: 20px; /* 右侧留出间距 */
    padding: 10px; /* 内边距，让内容不贴边 */
    background-clip: padding-box; /* 让背景色填充整个圆角区域 */
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

.el-menu {
    overflow: hidden;
    border-radius: 15px !important;; /* 设置圆角 */
    border: none !important;
    box-shadow: none !important;
}

.el-menu-item {
    border-radius: 15px !important;;
}

/* 悬停时的样式 */
.el-menu-item:hover {
    border-radius: 15px !important;; /* 设置圆角 */
    background-color: #d6d2cf !important; /* 悬停时的背景颜色 */
    color: #000000 !important; /* 悬停时的文字颜色 */
}

/* 选中时的样式 */
.el-menu-item.is-active {
    border-radius: 15px !important;; /* 设置圆角 */
    background-color: #e2dedb !important; /* 选中项的背景颜色 */
    color: #000000 !important; /* 选中项的文字颜色 */
}

/* 按下时的样式 */
.el-menu-item:active {
    border-radius: 15px !important;
    background-color: #e2dedb !important; /* 按下时颜色 */
}

/* 右侧内容区域 */
.main {
    width: 85%;
    height: 630px;
    background-color: #f8f4f2;
    border-radius: 15px; /* 右侧内容也加圆角，保持一致 */
    padding: 5px 20px 5px 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); /* 添加柔和阴影 */
}
</style>
