<template>
  <div ref="container" v-html="htmlContent"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  displayMode: {
    type: Boolean,
    default: false  // false 表示行内公式，true 表示块级公式
  }
})

const container = ref(null)
const htmlContent = ref('')

const renderMath = () => {
  try {
    htmlContent.value = katex.renderToString(props.content, {
      throwOnError: false,
      displayMode: props.displayMode
    })
  } catch (e) {
    htmlContent.value = `<span style="color: red;">Invalid LaTeX: ${e.message}</span>`
  }
}

onMounted(renderMath)
watch(() => props.content, renderMath)
</script>
