<template>
    <div class="upload-problems">
        <div class="header">上传题目</div>

        <!-- 题目标签选择 -->
        <div class="form-group">
            <label for="tag">题目标签</label>
            <select id="tag" v-model="selectedTag">
                <!-- 默认提示，禁止选择 -->
                <option value="" disabled>请选择标签</option>
                <!-- 循环输出标签选项 -->
                <option v-for="item in tags" :key="item.id" :value="item['tag_name']">
                    {{ item['tag_name'] }}
                </option>
            </select>
        </div>

        <!-- LaTeX 语句输入 -->
        <div class="form-group">
            <label for="latexInput">LaTeX 语句</label>
            <textarea
                    id="latexInput"
                    v-model="latexContent"
                    placeholder="请输入 LaTeX 语句"
            ></textarea>
        </div>

        <!-- 实时预览 -->
        <div class="preview">
            <h3>实时预览</h3>
            <div v-html="renderLatexPreview(latexContent)"></div>
        </div>

        <!-- 按钮区域：取消按钮和上传按钮 -->
        <div class="button-group">
            <button class="cancel-button" @click="cancelInput">取消</button>
            <button class="upload-button" @click="uploadProblem">上传题目</button>
        </div>
    </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'


// 定义响应式数据
const latexContent = ref('')          // 用户输入的 LaTeX 语句
const selectedTag = ref('')            // 用户选择的题目标签
const tags = ref([])                   // 下拉选择的标签数据

// 利用 KaTeX 渲染 LaTeX 预览
function renderLatexPreview(content) {
    try {
        if (!content.trim()) return ''
        return katex.renderToString(content, {
            throwOnError: false,
            displayMode: true, // 使用块级显示模式便于预览
        })
    } catch (error) {
        console.error("LaTeX 渲染错误：", error)
        return content
    }
}

// 从后端接口获取标签数据
async function fetchTags() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/tags')
        if (response.ok) {
            const res = await response.json()
            // 假设返回的 JSON 格式为 { status: 200, data: [...] }
            tags.value = res.data ? res.data : res
        } else {
            console.error(`获取标签失败：${response.statusText}`)
        }
    } catch (error) {
        console.error('获取标签时出错：', error)
    }
}

const emit = defineEmits(['problemUploaded']) // ADDED: 定义发射事件

// 上传题目到后端
async function uploadProblem() {
    if (!latexContent.value.trim()) {
        alert("请输入 LaTeX 语句");
        return;
    }
    if (!selectedTag.value) {
        alert("请选择题目标签");
        return;
    }

    // 从 localStorage 中取出 token 和用户名
    const token = localStorage.getItem('token');// 登录后存储的 token

    const payload = {
        content: latexContent.value,
        tag: selectedTag.value,// 使用下拉选择的标签
        Upload_time: new Date().toISOString(),
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/api/problems', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'token': token
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert("题目上传成功");
            // 上传成功后清空输入
            latexContent.value = '';
            selectedTag.value = '';
            emit("problemUploaded") // ADDED: 发射事件，通知父组件刷新
        } else {
            alert(`上传失败：${response.statusText}`);
        }
    } catch (error) {
        console.error("上传题目时出错：", error);
        alert(`上传出错：${error.message}`);
    }
}

// 点击取消按钮，清空输入框
function cancelInput() {
    latexContent.value = ''
    selectedTag.value = ''
}

// 在组件挂载时获取标签数据
onMounted(() => {
    fetchTags()
})
</script>

<style scoped>
.header {
    width: 100%;
    height: 10%;
    text-align: center;
    line-height: 64px;
    font-size: 20px;
    font-weight: 800;
    border-bottom: 1px solid #e3e3e3;
}

/* 使组件和外层容器融为一体，不添加多余背景和边框 */
.upload-problems {
    width: 100%;
    padding: 0;
    background: transparent;
    border: none;
    box-shadow: none;
}

/* 表单组样式 */
.form-group {
    margin-bottom: 12px;
    display: flex;
    flex-direction: column;
}

.form-group label {
    margin-bottom: 6px;
    font-weight: 500;
}

/* 下拉选择框样式 */
.form-group select {
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

/* 输入框和文本域 */
.form-group input,
.form-group textarea {
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

textarea {
    min-height: 100px;
    resize: vertical;
}

/* 预览区域 */
.preview {
    margin-bottom: 12px;
    padding: 8px;
    background-color: #fafafa; /* 淡背景色 */
    border: 1px solid #ddd;
    border-radius: 4px;
}

/* 按钮区域 */
.button-group {
    display: flex;
    gap: 10px; /* 两个按钮之间的间隔 */
}

/* 取消按钮样式 */
.cancel-button {
    flex: 1;
    padding: 10px;
    font-size: 16px;
    background-color: #525565;
    color: #f13836;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.cancel-button:hover {
    background-color: #bd2e2c;
    color: #ffffff;
}

/* 上传按钮样式 */
.upload-button {
    flex: 1;
    padding: 10px;
    font-size: 16px;
    background-color: #3b8640;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.upload-button:hover {
    background-color: #3b9640;
}
</style>
