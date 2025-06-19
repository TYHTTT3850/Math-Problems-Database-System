<template>
    <div class="p-6 overflow-y-auto">
        <!-- 筛选区域 -->
        <div class="filters mb-4">
            <label>
                题目标签：
                <select v-model="selectedTag" @change="resetPage">
                    <option value="all">全部</option>
                    <!-- 动态生成标签选项 -->
                    <option v-for="tag in tags" :key="tag.id" :value="tag.tag_name">
                        {{ tag.tag_name }}
                    </option>
                </select>
            </label>
            <label class="ml-4">
                上传时间：
                <select v-model="selectedTimeRange" @change="resetPage">
                    <option value="all">全部</option>
                    <option value="oneMonth">近一个月</option>
                    <option value="threeMonths">近三个月</option>
                    <option value="sixMonths">近六个月</option>
                    <option value="oneYear">近一年</option>
                </select>
            </label>
        </div>

        <!-- 题目列表 -->
        <div v-if="!selectedQuestion">
            <h2 class="text-xl font-semibold mb-4">题目列表</h2>
            <ul>
                <!-- 使用 paginatedQuestions 替代整个 questions 数组 -->
                <li
                        v-for="(q, index) in paginatedQuestions"
                        :key="index"
                        @click="selectQuestion(index)"
                        class="link-style list-item"
                >
                    <div class="question-header">
                        <!-- 用行号代替 id -->
                        <span class="question-number">
              <strong>{{ (currentPage - 1) * pageSize + index + 1 }}</strong>
            </span>
                        <span class="question-preview" v-html="renderLatexPreview(q.content)"></span>
                    </div>
                </li>
            </ul>
        </div>

        <!-- 题目详情 -->
        <div v-else>
            <button @click="selectedQuestion = null" class="back-button">← 返回题目列表</button>
            <h2 class="text-xl font-semibold mb-3">题目详情</h2>
            <div class="problem-content">
                <LatexRenderer :content="selectedQuestion.content" :displayMode="true"/>
            </div>
            <div class="metadata mt-4 text-sm text-gray-600">
                <p><strong>专业课程：</strong>{{ selectedQuestion.tag }}</p>
                <p><strong>上传者：</strong>{{ selectedQuestion.Uploader }}</p>
                <p><strong>上传时间：</strong>{{ selectedQuestion.Upload_time }}</p>
            </div>
        </div>

        <!-- 分页控制按钮 -->
        <div class="pagination flex justify-center items-center gap-4">
            <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
            <span>第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
        </div>
    </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import LatexRenderer from './LatexRender.vue'

// 原始题目数据
const questions = ref([])
// 当前选中的题目
const selectedQuestion = ref(null)
// 当前页码，初始为第一页
const currentPage = ref(1)
// 每页显示几题
const pageSize = 9

// 新增：标签列表（动态从后端获取）
const tags = ref([])

// 新增：筛选条件
const selectedTag = ref('all')
const selectedTimeRange = ref('all')

// 计算过滤后的题目列表
const filteredQuestions = computed(() => {
    let filtered = questions.value

    // 按标签筛选（假设题目的 tag 属性保存标签名称，与 tag_name 对应）
    if (selectedTag.value !== 'all') {
        filtered = filtered.filter(q => q.tag === selectedTag.value)
    }

    // 按上传时间筛选
    if (selectedTimeRange.value !== 'all') {
        const now = new Date()
        let thresholdDate = new Date()
        if (selectedTimeRange.value === 'oneMonth') {
            thresholdDate.setMonth(now.getMonth() - 1)
        } else if (selectedTimeRange.value === 'threeMonths') {
            thresholdDate.setMonth(now.getMonth() - 3)
        } else if (selectedTimeRange.value === 'sixMonths') {
            thresholdDate.setMonth(now.getMonth() - 6)
        } else if (selectedTimeRange.value === 'oneYear') {
            thresholdDate.setFullYear(now.getFullYear() - 1)
        }
        filtered = filtered.filter(q => new Date(q.Upload_time) >= thresholdDate)
    }
    return filtered
})

// 分页：使用过滤后的题目数据
const paginatedQuestions = computed(() => {
    const startIndex = (currentPage.value - 1) * pageSize
    return filteredQuestions.value.slice(startIndex, startIndex + pageSize)
})

// 计算总页数基于过滤后的数据
const totalPages = computed(() => {
    return Math.ceil(filteredQuestions.value.length / pageSize)
})

// 获取题目数据，并按 id 升序排序
async function fetchProblems() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/problems')
        if (response.ok) {
            const res = await response.json()
            const data = res.data ? res.data : res
            // 按 id 升序排序（数据排序不会影响分页或过滤）
            questions.value = data.sort((a, b) => a.id - b.id)
        } else {
            console.error(`获取数据失败：${response.statusText}`)
        }
    } catch (error) {
        console.error('获取数据时发生错误：', error)
    }
}

// 获取标签数据（从后台 tags 表读取动态标签）
async function fetchTags() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/tags')
        if (response.ok) {
            const res = await response.json()
            if (res.status === 200) {
                tags.value = res.data
            } else {
                console.error("获取标签失败：", res.msg)
            }
        } else {
            console.error(`获取标签失败：${response.statusText}`)
        }
    } catch (error) {
        console.error('获取标签时发生错误：', error)
    }
}

// 选择题目时计算全局索引
function selectQuestion(indexInPage) {
    const globalIndex = (currentPage.value - 1) * pageSize + indexInPage
    selectedQuestion.value = filteredQuestions.value[globalIndex]
}

// 分页控制：下一页
function nextPage() {
    if (currentPage.value < totalPages.value) {
        currentPage.value++
    }
}

// 分页控制：上一页
function prevPage() {
    if (currentPage.value > 1) {
        currentPage.value--
    }
}

// 筛选条件改变时，将页码重置为第一页
function resetPage() {
    currentPage.value = 1
}

onMounted(() => {
    fetchProblems()
    fetchTags()
})

// 渲染 LaTeX 预览，确保公式显示正确
function renderLatexPreview(content) {
    try {
        return katex.renderToString(content, {
            throwOnError: false,
            displayMode: false
        })
    } catch (error) {
        console.error("渲染 LaTeX 预览出错：", error)
        return content
    }
}

// 让父组件可以调用刷新方法
defineExpose({refreshProblems: fetchProblems})
</script>

<style>
/* 与原有样式保持一致，如有需要可进行扩展 */

/* 筛选区域样式 */
.filters {
    margin-bottom: 16px;
}

.filters label {
    font-size: 16px;
}

.filters select {
    margin-left: 8px;
    padding: 4px 6px;
}

/* 其他样式照常 */
ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.list-item {
    display: flex;
    flex-direction: column;
    padding: 8px 0;
    margin-bottom: 12px;
    border-bottom: 1px solid #f0f0f0;
    transition: background-color 0.3s, color 0.3s;
}

.link-style:hover {
    text-decoration: underline;
    cursor: pointer;
    color: #1890ff;
}

.question-header {
    display: flex;
    align-items: center;
    gap: 16px;
}

.question-number,
.question-preview {
    display: inline-block;
}

.back-button {
    color: black;
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    background-color: #eeeae7;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

.back-button:hover {
    background-color: #e2dedb;
    transform: scale(1.05);
}

.back-button:active {
    background-color: #e2dedb;
    transform: scale(0.95);
}

.metadata p {
    margin: 4px 0;
}

.pagination {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #fff;
    padding: 8px 0;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 16px;
    z-index: 100;
}

.pagination button {
    padding: 4px 8px;
    border: none;
    background-color: #fff;
    border-radius: 3px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.pagination button:disabled {
    cursor: not-allowed;
    opacity: 0.5;
}

.pagination button:hover:not(:disabled) {
    background-color: #f0f0f0;
}
</style>
