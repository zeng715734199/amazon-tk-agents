<template>
  <page-heading title="竞品监控" description="比较商品价格和排名，并获取动态定价建议">
    <template #extra><a-button :loading="loading" @click="loadOverview"><reload-outlined />刷新</a-button></template>
  </page-heading>

  <a-card>
    <a-row :gutter="[16, 16]" align="middle">
      <a-col :xs="24" :md="12">
        <a-segmented v-model:value="selectedProduct" :options="productOptions" block @change="loadOverview" />
      </a-col>
      <a-col :xs="24" :md="12">
        <a-input-search v-model:value="searchQuery" enter-button="实时搜索" placeholder="搜索竞品名称或关键词" :loading="searching" @search="searchCompetitor" />
      </a-col>
    </a-row>
  </a-card>

  <a-alert v-if="error" class="section-gap" type="error" show-icon :message="error" />

  <a-row :gutter="[16, 16]" class="section-gap">
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="我方价格" :value="overview?.product?.price || 0" prefix="$" :precision="2" :loading="loading" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="市场均价" :value="overview?.price_analysis?.market_avg || 0" prefix="$" :precision="2" :loading="loading" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="价格竞争力" :value="overview?.price_analysis?.price_competitiveness || 0" suffix=" 分" :loading="loading" /></a-col>
    <a-col :xs="24" :sm="12" :xl="6"><metric-card title="当前毛利率" :value="overview?.recommendation?.current_margin || 0" suffix="%" :precision="1" :loading="loading" /></a-col>
  </a-row>

  <a-row :gutter="[16, 16]" class="section-gap">
    <a-col :xs="24" :xl="12"><a-card title="当前价格对比" :loading="loading"><base-chart :option="priceOption" /></a-card></a-col>
    <a-col :xs="24" :xl="12"><a-card title="近七期价格趋势" :loading="loading"><base-chart :option="historyOption" /></a-card></a-col>
  </a-row>

  <a-card title="竞品明细" class="section-gap">
    <a-table row-key="asin" :columns="competitorColumns" :data-source="overview?.competitors || []" :loading="loading" :pagination="false" :scroll="{ x: 850 }">
      <template #bodyCell="{ column, record }">
        <span v-if="column.key === 'price'">{{ formatCurrency(record.current_price) }}</span>
        <span v-else-if="column.key === 'rating'">{{ record.rating }} / 5</span>
        <span v-else-if="column.key === 'bsr'">{{ record.bsr ? `#${formatNumber(record.bsr)}` : '--' }}</span>
      </template>
    </a-table>
  </a-card>

  <a-row :gutter="[16, 16]" class="section-gap">
    <a-col :xs="24" :xl="12">
      <a-card title="价格预警">
        <a-empty v-if="!overview?.alerts?.length" description="暂无价格预警" />
        <a-list v-else :data-source="overview.alerts">
          <template #renderItem="{ item }"><a-list-item><a-list-item-meta :title="item.competitor" :description="item.detail"><template #avatar><a-tag color="warning">价格</a-tag></template></a-list-item-meta></a-list-item></template>
        </a-list>
      </a-card>
    </a-col>
    <a-col :xs="24" :xl="12">
      <a-card title="定价建议" :loading="loading">
        <a-result v-if="overview?.recommendation" :status="recommendationStatus" :title="statusText(overview.recommendation.action)" :sub-title="overview.recommendation.reasoning">
          <template #extra>
            <a-space>
              <a-statistic title="建议价格" :value="overview.recommendation.suggested_price" prefix="$" :precision="2" />
              <a-statistic title="预计毛利率" :value="overview.recommendation.projected_margin" suffix="%" :precision="1" />
            </a-space>
          </template>
        </a-result>
      </a-card>
    </a-col>
  </a-row>

  <a-card v-if="searchResult" title="实时搜索结果" class="section-gap">
    <a-alert v-if="searchResult.note" :message="searchResult.note" type="info" show-icon />
    <a-table v-if="searchResult.results?.length" row-key="link" :columns="searchColumns" :data-source="searchResult.results" :pagination="{ pageSize: 5 }">
      <template #bodyCell="{ column, record }">
        <a v-if="column.key === 'title'" :href="record.link" target="_blank" rel="noreferrer">{{ record.title }}</a>
      </template>
    </a-table>
    <a-empty v-else description="没有搜索结果" />
  </a-card>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import {
  Alert as AAlert, Button as AButton, Card as ACard, Col as ACol, Empty as AEmpty,
  InputSearch as AInputSearch, List as AList, ListItem as AListItem, ListItemMeta as AListItemMeta,
  Result as AResult, Row as ARow, Segmented as ASegmented, Space as ASpace, Statistic as AStatistic,
  Table as ATable, Tag as ATag, message,
} from 'ant-design-vue'
import { ReloadOutlined } from '@ant-design/icons-vue'
import BaseChart from '@/components/BaseChart.vue'
import MetricCard from '@/components/MetricCard.vue'
import PageHeading from '@/components/PageHeading.vue'
import { competitorApi } from '@/services/api'
import { formatCurrency, formatNumber, statusText } from '@/utils/format'

const products = ref([])
const selectedProduct = ref('earbuds')
const overview = ref()
const loading = ref(false)
const error = ref('')
const searchQuery = ref('')
const searching = ref(false)
const searchResult = ref()

const competitorColumns = [
  { title: '竞品', dataIndex: 'name', key: 'name' },
  { title: '品牌', dataIndex: 'brand', key: 'brand' },
  { title: '平台', dataIndex: 'platform', key: 'platform', width: 100 },
  { title: '价格', key: 'price', width: 120 },
  { title: '评分', key: 'rating', width: 100 },
  { title: '评论数', dataIndex: 'reviews', key: 'reviews', width: 120 },
  { title: 'BSR', key: 'bsr', width: 100 },
]
const searchColumns = [
  { title: '标题', key: 'title' },
  { title: '摘要', dataIndex: 'snippet', key: 'snippet' },
  { title: '来源', dataIndex: 'source', key: 'source', width: 140 },
]

const productOptions = computed(() => products.value.map(item => ({ label: item.name, value: item.key })))
const recommendationStatus = computed(() => overview.value?.recommendation?.action === 'hold' ? 'success' : 'info')
const priceOption = computed(() => {
  const rows = overview.value ? [{ name: overview.value.product.name, current_price: overview.value.product.price }, ...(overview.value.competitors || [])] : []
  return {
    tooltip: { trigger: 'axis' },
    grid: { left: 48, right: 20, top: 24, bottom: 70 },
    xAxis: { type: 'category', data: rows.map(item => item.name), axisLabel: { rotate: 24 } },
    yAxis: { type: 'value', axisLabel: { formatter: '${value}' } },
    series: [{ type: 'bar', data: rows.map((item, index) => ({ value: item.current_price, itemStyle: { color: index === 0 ? '#1677ff' : '#91caff' } })) }],
  }
})
const historyOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { bottom: 0 },
  grid: { left: 48, right: 20, top: 24, bottom: 60 },
  xAxis: { type: 'category', data: ['T-6', 'T-5', 'T-4', 'T-3', 'T-2', 'T-1', '当前'] },
  yAxis: { type: 'value', axisLabel: { formatter: '${value}' } },
  series: (overview.value?.competitors || []).map(item => ({ name: item.name, type: 'line', smooth: true, data: item.price_history || [] })),
}))

async function loadOverview() {
  loading.value = true
  error.value = ''
  try {
    overview.value = await competitorApi.overview(selectedProduct.value)
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    loading.value = false
  }
}

async function searchCompetitor() {
  if (!searchQuery.value.trim()) return
  searching.value = true
  try {
    searchResult.value = await competitorApi.search(searchQuery.value.trim())
  } catch (requestError) {
    message.error(requestError.message)
  } finally {
    searching.value = false
  }
}

onMounted(async () => {
  try {
    products.value = await competitorApi.products()
    selectedProduct.value = products.value[0]?.key || 'earbuds'
    await loadOverview()
  } catch (requestError) {
    error.value = requestError.message
  }
})
</script>
