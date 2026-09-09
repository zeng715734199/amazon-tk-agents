<template>
  <page-heading title="利润分析" description="查看跨平台收入、成本结构和利润变化">
    <template #extra>
      <a-select v-model:value="period" :options="periodOptions" style="width: 130px" />
      <a-button @click="exportReport"><download-outlined />导出报告</a-button>
    </template>
  </page-heading>

  <a-row :gutter="[16, 16]">
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="总销售额" :value="summary.revenue" prefix="$" :precision="2" caption="较上期 +12.8%" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="毛利润" :value="summary.grossProfit" prefix="$" :precision="2" caption="较上期 +9.6%" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="净利润" :value="summary.netProfit" prefix="$" :precision="2" caption="较上期 +7.4%" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="净利率" :value="summary.netMargin" suffix="%" :precision="1" caption="目标 20%" /></a-col>
  </a-row>

  <a-row :gutter="[16, 16]" class="section-gap">
    <a-col :xs="24" :xl="14">
      <a-card title="P&L 分析">
        <a-table row-key="item" :columns="pnlColumns" :data-source="pnlRows" :pagination="false">
          <template #bodyCell="{ column, record }">
            <strong v-if="column.key === 'item' && record.highlight">{{ record.item }}</strong>
            <span v-else-if="column.key !== 'item'" :class="{ 'negative-value': record[column.dataIndex] < 0, 'strong-value': record.highlight }">{{ formatCurrency(record[column.dataIndex]) }}</span>
          </template>
        </a-table>
      </a-card>
    </a-col>
    <a-col :xs="24" :xl="10"><a-card title="平台利润对比"><base-chart :option="platformOption" height="360px" /></a-card></a-col>
  </a-row>

  <a-card title="近 12 周利润趋势" class="section-gap"><base-chart :option="trendOption" height="340px" /></a-card>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Button as AButton, Card as ACard, Col as ACol, Row as ARow, Select as ASelect, Table as ATable } from 'ant-design-vue'
import { DownloadOutlined } from '@ant-design/icons-vue'
import BaseChart from '@/components/BaseChart.vue'
import MetricCard from '@/components/MetricCard.vue'
import PageHeading from '@/components/PageHeading.vue'
import { downloadCsv } from '@/utils/export'
import { formatCurrency } from '@/utils/format'

const period = ref('30d')
const periodOptions = [{ label: '近 30 天', value: '30d' }, { label: '近 90 天', value: '90d' }, { label: '本年度', value: 'year' }]
const baseRows = [
  { item: '销售收入', amazon: 84260, tiktok: 51740, highlight: true },
  { item: '商品成本', amazon: -26780, tiktok: -15820 },
  { item: '平台佣金', amazon: -12639, tiktok: -4140 },
  { item: '广告费用', amazon: -8940, tiktok: -7230 },
  { item: '仓储与物流', amazon: -6740, tiktok: -4850 },
  { item: '退款与售后', amazon: -2180, tiktok: -1640 },
  { item: '净利润', amazon: 26981, tiktok: 18060, highlight: true },
]

const factor = computed(() => ({ '30d': 1, '90d': 2.82, year: 10.6 }[period.value]))
const pnlRows = computed(() => baseRows.map(row => ({ ...row, amazon: Math.round(row.amazon * factor.value), tiktok: Math.round(row.tiktok * factor.value), total: Math.round((row.amazon + row.tiktok) * factor.value) })))
const summary = computed(() => {
  const revenue = pnlRows.value[0].total
  const netProfit = pnlRows.value.at(-1).total
  const directCosts = Math.abs(pnlRows.value[1].total + pnlRows.value[2].total)
  return { revenue, grossProfit: revenue - directCosts, netProfit, netMargin: netProfit / revenue * 100 }
})
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
  xAxis: { type: 'category', data: ['销售收入', '毛利润', '净利润'] },
  yAxis: { type: 'value', axisLabel: { formatter: value => `$${Math.round(value / 1000)}k` } },
  series: [
    { name: 'Amazon', type: 'bar', data: [84260, 44841, 26981].map(value => Math.round(value * factor.value)) },
    { name: 'TikTok Shop', type: 'bar', data: [51740, 31780, 18060].map(value => Math.round(value * factor.value)) },
  ],
}))

const trendOption = {
  tooltip: { trigger: 'axis' },
  legend: { bottom: 0 },
  grid: { left: 64, right: 28, top: 30, bottom: 55 },
  xAxis: { type: 'category', data: Array.from({ length: 12 }, (_, index) => `第 ${index + 1} 周`) },
  yAxis: { type: 'value', axisLabel: { formatter: value => `$${Math.round(value / 1000)}k` } },
  series: [
    { name: '销售额', type: 'line', smooth: true, data: [25100, 26800, 27400, 29100, 28600, 31200, 32900, 34100, 35800, 37600, 39100, 41800] },
    { name: '净利润', type: 'line', smooth: true, areaStyle: { opacity: 0.08 }, data: [7200, 7900, 8100, 8400, 8200, 9100, 9800, 10200, 10800, 11400, 11900, 12600] },
  ],
}

function exportReport() {
  downloadCsv(`profit-${period.value}.csv`, pnlColumns.map(column => ({ title: column.title, dataIndex: column.dataIndex })), pnlRows.value)
}
</script>
