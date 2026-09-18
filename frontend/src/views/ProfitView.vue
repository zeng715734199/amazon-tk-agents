<template>
  <page-heading title="利润分析" description="查看跨平台收入、成本结构和利润变化">
    <template #extra>
      <a-select v-model:value="period" :options="periodOptions" style="width: 130px" @change="loadReport" />
      <a-button @click="exportReport"><download-outlined />导出报告</a-button>
    </template>
  </page-heading>

  <a-row :gutter="[16, 16]">
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="总销售额" :value="report?.summary?.revenue || 0" prefix="$" :precision="2" :loading="loading" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="毛利润" :value="report?.summary?.gross_profit || 0" prefix="$" :precision="2" :loading="loading" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="净利润" :value="report?.summary?.net_profit || 0" prefix="$" :precision="2" :loading="loading" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="净利率" :value="report?.summary?.net_margin || 0" suffix="%" :precision="1" :loading="loading" /></a-col>
  </a-row>

  <a-row :gutter="[16, 16]" class="section-gap">
    <a-col :xs="24" :xl="14">
      <a-card title="P&L 分析" :loading="loading">
        <a-table row-key="item" :columns="pnlColumns" :data-source="report?.pnl_rows || []" :pagination="false">
          <template #bodyCell="{ column, record }">
            <strong v-if="column.key === 'item' && record.highlight">{{ record.item }}</strong>
            <span v-else-if="column.key !== 'item'" :class="{ 'negative-value': record[column.dataIndex] < 0, 'strong-value': record.highlight }">{{ formatCurrency(record[column.dataIndex]) }}</span>
          </template>
        </a-table>
      </a-card>
    </a-col>
    <a-col :xs="24" :xl="10"><a-card title="平台利润对比" :loading="loading"><base-chart :option="platformOption" height="360px" /></a-card></a-col>
  </a-row>

  <a-card title="近 12 周利润趋势" class="section-gap" :loading="loading"><base-chart :option="trendOption" height="340px" /></a-card>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { Button as AButton, Card as ACard, Col as ACol, Row as ARow, Select as ASelect, Table as ATable, message } from 'ant-design-vue'
import { DownloadOutlined } from '@ant-design/icons-vue'
import BaseChart from '@/components/BaseChart.vue'
import MetricCard from '@/components/MetricCard.vue'
import PageHeading from '@/components/PageHeading.vue'
import { profitApi } from '@/services/api'
import { downloadCsv } from '@/utils/export'
import { formatCurrency } from '@/utils/format'

const period = ref('30d')
const report = ref()
const loading = ref(false)
const periodOptions = [{ label: '近 30 天', value: '30d' }, { label: '近 90 天', value: '90d' }, { label: '本年度', value: 'year' }]
const pnlColumns = [
  { title: '项目', dataIndex: 'item', key: 'item' },
  { title: 'Amazon', dataIndex: 'amazon', key: 'amazon', align: 'right' },
  { title: 'TikTok Shop', dataIndex: 'tiktok', key: 'tiktok', align: 'right' },
  { title: '合计', dataIndex: 'total', key: 'total', align: 'right' },
]

const platformOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { bottom: 0 },
  grid: { left: 60, right: 24, top: 30, bottom: 55 },
  xAxis: { type: 'category', data: (report.value?.platform_comparison || []).map(item => item.metric) },
  yAxis: { type: 'value', axisLabel: { formatter: value => `$${Math.round(value / 1000)}k` } },
  series: [
    { name: 'Amazon', type: 'bar', data: (report.value?.platform_comparison || []).map(item => item.amazon) },
    { name: 'TikTok Shop', type: 'bar', data: (report.value?.platform_comparison || []).map(item => item.tiktok) },
  ],
}))

const trendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { bottom: 0 },
  grid: { left: 64, right: 28, top: 30, bottom: 55 },
  xAxis: { type: 'category', data: (report.value?.trend || []).map(item => item.label) },
  yAxis: { type: 'value', axisLabel: { formatter: value => `$${Math.round(value / 1000)}k` } },
  series: [
    { name: '销售额', type: 'line', smooth: true, data: (report.value?.trend || []).map(item => item.revenue) },
    { name: '净利润', type: 'line', smooth: true, areaStyle: { opacity: 0.08 }, data: (report.value?.trend || []).map(item => item.net_profit) },
  ],
}))

async function loadReport() {
  loading.value = true
  try {
    report.value = await profitApi.report(period.value)
  } catch (error) {
    message.error(error.message)
  } finally {
    loading.value = false
  }
}

function exportReport() {
  downloadCsv(`profit-${period.value}.csv`, pnlColumns.map(column => ({ title: column.title, dataIndex: column.dataIndex })), report.value?.pnl_rows || [])
}

onMounted(loadReport)
</script>
