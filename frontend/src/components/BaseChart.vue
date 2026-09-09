<template>
  <div ref="chartElement" class="base-chart" :style="{ height }"></div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  option: { type: Object, required: true },
  height: { type: String, default: '300px' },
})

const chartElement = ref()
let chart
let observer

async function render() {
  await nextTick()
  if (!chartElement.value) return
  chart ||= echarts.init(chartElement.value)
  chart.setOption(props.option, true)
}

watch(() => props.option, render, { deep: true })

onMounted(() => {
  render()
  observer = new ResizeObserver(() => chart?.resize())
  observer.observe(chartElement.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()
  chart?.dispose()
})
</script>
