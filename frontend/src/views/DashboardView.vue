<template>
  <page-heading title="总览面板" description="查看客服、库存和竞品的核心运营指标">
    <template #extra><a-button :loading="loading" @click="loadData"><reload-outlined />刷新</a-button></template>
  </page-heading>

  <a-alert v-if="error" type="error" show-icon :message="error" class="section-gap" />

  <a-row :gutter="[16, 16]">
    <a-col :xs="24" :sm="12" :xl="6">
      <metric-card title="今日客服会话" :value="dashboard?.customer_service?.today?.total || 0" caption="今日接待总量" :loading="loading" />
    </a-col>
    <a-col :xs="24" :sm="12" :xl="6">
      <metric-card title="自动解决" :value="dashboard?.customer_service?.today?.auto_resolved || 0" caption="无需人工介入" :loading="loading" />
    </a-col>
    <a-col :xs="24" :sm="12" :xl="6">
      <metric-card title="库存总量" :value="dashboard?.supply_chain?.total_units || 0" suffix=" 件" caption="含在途库存" :loading="loading" />
    </a-col>
    <a-col :xs="24" :sm="12" :xl="6">
      <metric-card title="库存货值" :value="dashboard?.supply_chain?.total_value || 0" prefix="$" :precision="2" caption="按采购成本估算" :loading="loading" />
    </a-col>
  </a-row>

  <a-row :gutter="[16, 16]" class="section-gap">
    <a-col :xs="24" :xl="8">
      <a-card title="客服意图分布" :loading="loading"><base-chart :option="intentOption" /></a-card>
    </a-col>
    <a-col :xs="24" :xl="8">
      <a-card title="近七日销售趋势"><base-chart :option="salesOption" /></a-card>
    </a-col>
    <a-col :xs="24" :xl="8">
      <a-card title="仓库库存分布" :loading="loading"><base-chart :option="warehouseOption" /></a-card>
    </a-col>
  </a-row>

  <a-row :gutter="[16, 16]" class="section-gap">
    <a-col :xs="24" :xl="16">
      <a-card title="竞品动态">
        <a-table row-key="product" :columns="competitorColumns" :data-source="competitorRows" :loading="loading" :pagination="false" :scroll="{ x: 760 }">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'price'">{{ formatCurrency(record.our_price) }}</template>
            <template v-else-if="column.key === 'market'">{{ formatCurrency(record.market_avg) }}</template>
            <template v-else-if="column.key === 'action'">
              <a-tag :color="statusColor(record.recommendation?.action)">{{ statusText(record.recommendation?.action) }}</a-tag>
            </template>
            <template v-else-if="column.key === 'suggested'">{{ formatCurrency(record.recommendation?.suggested_price) }}</template>
          </template>
        </a-table>
      </a-card>
    </a-col>
    <a-col :xs="24" :xl="8">
      <a-card title="API 连接状态" :loading="loading">
        <a-list :data-source="connectionRows" size="small">
          <template #renderItem="{ item }">
            <a-list-item><span>{{ item.label }}</span><a-tag :color="item.connected ? 'success' : 'default'">{{ item.connected ? '已连接' : '未配置' }}</a-tag></a-list-item>
          </template>
        </a-list>
      </a-card>
    </a-col>
  </a-row>

  <a-card title="库存预警" class="section-gap">
    <a-table row-key="key" :columns="alertColumns" :data-source="inventoryAlerts" :loading="loading" :pagination="false" :scroll="{ x: 680 }">
      <template #bodyCell="{ column, record }">
        <a-tag v-if="column.key === 'severity'" :color="statusColor(record.severity)">{{ statusText(record.severity) }}</a-tag>
      </template>
    </a-table>
  </a-card>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  Alert as AAlert, Button as AButton, Card as ACard, Col as ACol, Row as ARow,
  Table as ATable, Tag as ATag, List as AList, ListItem as AListItem,
} from 'ant-design-vue'
import { ReloadOutlined } from '@ant-design/icons-vue'
import PageHeading from '@/components/PageHeading.vue'
import MetricCard from '@/components/MetricCard.vue'
import BaseChart from '@/components/BaseChart.vue'
import { systemApi } from '@/services/api'
import { formatCurrency, statusColor, statusText } from '@/utils/format'

const loading = ref(false)
const error = ref('')
const dashboard = ref()

const intentNames = { logistics: '物流', pre_sale: '售前', after_sale: '售后', complaint: '投诉', general: '其他' }
const connectionNames = { llm: '大语言模型', amazon: 'Amazon', tiktok: 'TikTok Shop', serper: '搜索服务', erp: 'ERP', webhook: 'Webhook' }

const competitorColumns = [
  { title: '商品', dataIndex: 'product', key: 'product' },
  { title: '当前价格', key: 'price' },
  { title: '市场均价', key: 'market' },
  { title: '跟踪竞品', dataIndex: 'competitors_count', key: 'count' },
  { title: '建议', key: 'action' },
  { title: '建议价格', key: 'suggested' },
]
const alertColumns = [
  { title: '等级', key: 'severity', width: 100 },
  { title: '商品', dataIndex: 'product', key: 'product' },
  { title: '规格', dataIndex: 'variant', key: 'variant', width: 120 },
  { title: '说明', dataIndex: 'message', key: 'message' },
]

const competitorRows = computed(() => dashboard.value?.competitor_briefing?.sections || [])
const inventoryAlerts = computed(() => (dashboard.value?.inventory_alerts || []).map((item, index) => ({ ...item, key: index })))
const connectionRows = computed(() => Object.entries(dashboard.value?.connections || {}).map(([key, connected]) => ({ key, label: connectionNames[key] || key, connected })))

const intentOption = computed(() => ({
  tooltip: { trigger: 'item' },
  legend: { bottom: 0 },
  series: [{ type: 'pie', radius: ['42%', '68%'], data: (dashboard.value?.customer_service?.top_intents || []).map(item => ({ value: item.count, name: intentNames[item.intent] || item.intent })) }],
}))

const warehouseOption = computed(() => {
  const warehouses = dashboard.value?.supply_chain?.warehouses || {}
  return {
    tooltip: { trigger: 'item' },
    legend: { bottom: 0 },
    series: [{ type: 'pie', radius: ['42%', '68%'], data: [
      { name: 'Amazon FBA', value: warehouses.amazon_fba || 0 },
      { name: 'TikTok 仓', value: warehouses.tiktok || 0 },
      { name: '在途', value: warehouses.in_transit || 0 },
    ] }],
  }
})

const salesOption = {
  tooltip: { trigger: 'axis' },
  legend: { data: ['Amazon', 'TikTok'] },
  grid: { left: 48, right: 24, top: 40, bottom: 36 },
  xAxis: { type: 'category', data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'] },
  yAxis: { type: 'value' },
  series: [
    { name: 'Amazon', type: 'line', smooth: true, data: [142, 158, 151, 176, 183, 214, 226] },
    { name: 'TikTok', type: 'line', smooth: true, data: [96, 108, 121, 118, 143, 177, 189] },
  ],
}

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    dashboard.value = await systemApi.dashboard()
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>
