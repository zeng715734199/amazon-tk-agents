<template>
  <a-card :loading="loading">
    <a-statistic :title="title" :value="value" :prefix="prefix" :suffix="suffix" :precision="precision" />
    <div v-if="caption" class="metric-caption">{{ caption }}</div>
  </a-card>
</template>

<script setup>
import { Card as ACard, Statistic as AStatistic } from 'ant-design-vue'

defineProps({
  title: { type: String, required: true },
  value: { type: [Number, String], default: 0 },
  prefix: { type: String, default: '' },
  suffix: { type: String, default: '' },
  precision: { type: Number, default: 0 },
  caption: { type: String, default: '' },
  loading: Boolean,
})
</script>
