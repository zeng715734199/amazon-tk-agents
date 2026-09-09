<template>
  <div class="page-heading">
    <a-space v-if="$slots.extra"><slot name="extra" /></a-space>
  </div>
</template>

<script setup>
import { Space as ASpace } from 'ant-design-vue'

defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
})
</script>
