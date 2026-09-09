<template>
  <page-heading title="供应链管理" description="管理多仓库存，生成补货计划与需求预测">
    <template #extra>
      <a-button @click="exportInventory"><download-outlined />导出库存</a-button>
      <a-button :loading="loading" @click="loadData"><reload-outlined />刷新</a-button>
    </template>
  </page-heading>

  <a-alert v-if="error" type="error" show-icon :message="error" class="section-gap" />

  <a-row :gutter="[16, 16]">
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="SKU 数量" :value="stats?.total_skus || 0" :loading="loading" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="库存总量" :value="stats?.total_units || 0" suffix=" 件" :loading="loading" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="库存货值" :value="stats?.total_value || 0" prefix="$" :precision="2" :loading="loading" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="库存预警" :value="(stats?.critical_alerts || 0) + (stats?.warning_alerts || 0)" suffix=" 条" :loading="loading" /></a-col>
  </a-row>

  <a-card title="库存明细" class="section-gap">
    <template #extra>
      <a-select v-model:value="inventoryFilter" :options="inventoryOptions" style="width: 230px" />
    </template>
    <a-table row-key="key" :columns="inventoryColumns" :data-source="filteredInventory" :loading="loading" :pagination="{ pageSize: 10 }" :scroll="{ x: 1100 }">
      <template #bodyCell="{ column, record }">
        <a-tag v-if="column.key === 'status'" :color="statusColor(record.status)">{{ statusText(record.status) }}</a-tag>
        <span v-else-if="column.key === 'cost'">{{ formatCurrency(record.unit_cost) }}</span>
      </template>
    </a-table>
  </a-card>

  <a-row :gutter="[16, 16]" class="section-gap">
    <a-col :xs="24" :xl="12">
      <a-card title="智能补货计划">
        <a-space class="card-toolbar">
          <a-select v-model:value="restockProduct" :options="productOptions" style="width: 240px" />
          <a-button type="primary" :loading="restockLoading" @click="generateRestock">生成计划</a-button>
        </a-space>
        <a-empty v-if="!restockPlan" description="选择商品后生成补货计划" />
        <template v-else>
          <a-descriptions :column="2" bordered size="small">
            <a-descriptions-item label="商品">{{ restockPlan.product }}</a-descriptions-item>
            <a-descriptions-item label="SKU">{{ restockPlan.sku }}</a-descriptions-item>
            <a-descriptions-item label="计划采购">{{ formatNumber(restockPlan.total_units) }} 件</a-descriptions-item>
            <a-descriptions-item label="预计成本">{{ formatCurrency(restockPlan.total_cost) }}</a-descriptions-item>
          </a-descriptions>
          <a-table row-key="variant" size="small" :columns="restockColumns" :data-source="restockPlan.orders || []" :pagination="false" :scroll="{ x: 820 }" class="inner-table">
            <template #bodyCell="{ column, record }">
              <a-tag v-if="column.key === 'urgency'" :color="statusColor(record.urgency)">{{ statusText(record.urgency) }}</a-tag>
              <span v-else-if="column.key === 'cost'">{{ formatCurrency(record.cost) }}</span>
              <span v-else-if="column.key === 'shipping'">{{ statusText(record.ship_method) }}</span>
            </template>
          </a-table>
        </template>
      </a-card>
    </a-col>

    <a-col :xs="24" :xl="12">
      <a-card title="需求预测">
        <a-space class="card-toolbar">
          <a-select v-model:value="forecastProduct" :options="productOptions" style="width: 210px" />
          <a-select v-model:value="forecastDays" :options="dayOptions" style="width: 110px" />
          <a-button type="primary" :loading="forecastLoading" @click="generateForecast">开始预测</a-button>
        </a-space>
        <a-empty v-if="!forecast" description="选择商品和周期后开始预测" />
        <template v-else>
          <base-chart :option="forecastOption" height="260px" />
          <a-table row-key="variant" size="small" :columns="forecastColumns" :data-source="forecast.variants || []" :pagination="false">
            <template #bodyCell="{ column, record }">
              <a-tag v-if="column.key === 'stockout'" :color="record.stockout_date ? 'error' : 'success'">{{ record.stockout_date || '周期内安全' }}</a-tag>
            </template>
          </a-table>
        </template>
      </a-card>
    </a-col>
  </a-row>

  <a-card title="供应链预警" class="section-gap">
    <a-table row-key="key" :columns="alertColumns" :data-source="alertRows" :loading="loading" :pagination="false" :scroll="{ x: 700 }">
      <template #bodyCell="{ column, record }"><a-tag v-if="column.key === 'severity'" :color="statusColor(record.severity)">{{ statusText(record.severity) }}</a-tag></template>
    </a-table>
  </a-card>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  Alert as AAlert, Button as AButton, Card as ACard, Col as ACol, Descriptions as ADescriptions,
  DescriptionsItem as ADescriptionsItem, Empty as AEmpty, Row as ARow, Select as ASelect,
  Space as ASpace, Table as ATable, Tag as ATag, message,
} from 'ant-design-vue'
import { DownloadOutlined, ReloadOutlined } from '@ant-design/icons-vue'
import BaseChart from '@/components/BaseChart.vue'
import MetricCard from '@/components/MetricCard.vue'
import PageHeading from '@/components/PageHeading.vue'
import { supplyChainApi } from '@/services/api'
import { downloadCsv } from '@/utils/export'
import { formatCurrency, formatNumber, statusColor, statusText } from '@/utils/format'

const overview = ref()
const stats = ref()
const loading = ref(false)
const error = ref('')
const inventoryFilter = ref('all')
const restockProduct = ref('earbuds')
const restockPlan = ref()
const restockLoading = ref(false)
const forecastProduct = ref('earbuds')
const forecastDays = ref(30)
const forecast = ref()
const forecastLoading = ref(false)

const inventoryColumns = [
  { title: '商品', dataIndex: 'product', key: 'product', width: 220, fixed: 'left' },
  { title: 'SKU', dataIndex: 'sku', key: 'sku', width: 130 },
  { title: '规格', dataIndex: 'variant', key: 'variant', width: 100 },
  { title: '单位成本', key: 'cost', width: 110 },
  { title: 'Amazon FBA', dataIndex: 'amazon_fba', key: 'amazon_fba', width: 130 },
  { title: 'TikTok 仓', dataIndex: 'tiktok_warehouse', key: 'tiktok', width: 110 },
  { title: '在途', dataIndex: 'in_transit', key: 'transit', width: 90 },
  { title: '日均销量', dataIndex: 'daily_velocity', key: 'velocity', width: 110 },
  { title: '库存天数', dataIndex: 'days_of_stock', key: 'days', width: 110 },
  { title: '状态', key: 'status', width: 90, fixed: 'right' },
]
const restockColumns = [
  { title: '规格', dataIndex: 'variant', key: 'variant', width: 90 },
  { title: '当前库存', dataIndex: 'current_stock', key: 'current', width: 100 },
  { title: '采购量', dataIndex: 'order_quantity', key: 'order', width: 90 },
  { title: '成本', key: 'cost', width: 110 },
  { title: '紧急度', key: 'urgency', width: 90 },
  { title: '运输', key: 'shipping', width: 80 },
  { title: '预计到货', dataIndex: 'estimated_arrival', key: 'arrival', width: 120 },
]
const forecastColumns = [
  { title: '规格', dataIndex: 'variant', key: 'variant' },
  { title: '当前库存', dataIndex: 'current_stock', key: 'stock' },
  { title: '日均销量', dataIndex: 'avg_daily_velocity', key: 'velocity' },
  { title: '预计销量', dataIndex: 'projected_30d_sales', key: 'sales' },
  { title: '预计缺货', key: 'stockout' },
]
const alertColumns = [
  { title: '等级', key: 'severity', width: 100 },
  { title: '商品', dataIndex: 'product', key: 'product', width: 240 },
  { title: '规格', dataIndex: 'variant', key: 'variant', width: 120 },
  { title: '说明', dataIndex: 'message', key: 'message' },
]

const inventoryRows = computed(() => (overview.value?.products || []).flatMap(product => product.variants.map(variant => ({
  ...variant, key: `${product.key}-${variant.variant}`, productKey: product.key, product: product.name, sku: product.sku, unit_cost: product.unit_cost,
}))))
const filteredInventory = computed(() => inventoryFilter.value === 'all' ? inventoryRows.value : inventoryRows.value.filter(item => item.productKey === inventoryFilter.value))
const productOptions = computed(() => (overview.value?.products || []).map(item => ({ label: item.name, value: item.key })))
const inventoryOptions = computed(() => [{ label: '全部商品', value: 'all' }, ...productOptions.value])
const dayOptions = [30, 60, 90].map(value => ({ label: `${value} 天`, value }))
const alertRows = computed(() => (overview.value?.alerts || []).map((item, index) => ({ ...item, key: index })))
const forecastOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { bottom: 0 },
  grid: { left: 48, right: 20, top: 24, bottom: 55 },
  xAxis: { type: 'category', data: forecast.value?.variants?.[0]?.daily_forecast?.map(item => item.date.slice(5)) || [] },
  yAxis: { type: 'value' },
  series: (forecast.value?.variants || []).map(item => ({ name: `${item.variant} 库存`, type: 'line', showSymbol: false, data: item.daily_forecast.map(day => day.projected_stock) })),
}))

async function loadData() {
  loading.value = true
  error.value = ''
  try {
    [overview.value, stats.value] = await Promise.all([supplyChainApi.overview(), supplyChainApi.stats()])
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    loading.value = false
  }
}

async function generateRestock() {
  restockLoading.value = true
  try {
    restockPlan.value = await supplyChainApi.restock(restockProduct.value)
    message.success('补货计划已生成')
  } catch (requestError) {
    message.error(requestError.message)
  } finally {
    restockLoading.value = false
  }
}

async function generateForecast() {
  forecastLoading.value = true
  try {
    forecast.value = await supplyChainApi.forecast(forecastProduct.value, forecastDays.value)
  } catch (requestError) {
    message.error(requestError.message)
  } finally {
    forecastLoading.value = false
  }
}

function exportInventory() {
  downloadCsv('inventory.csv', inventoryColumns.filter(column => column.dataIndex).map(column => ({ title: column.title, dataIndex: column.dataIndex })), inventoryRows.value)
}

onMounted(loadData)
</script>
