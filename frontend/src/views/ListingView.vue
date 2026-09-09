<template>
  <page-heading title="Listing 生成" description="基于商品、平台和语言生成 Listing，并分析 SEO 表现" />

  <a-card title="生成参数">
    <a-form layout="vertical" :model="form" @finish="generate">
      <a-row :gutter="16">
        <a-col :xs="24" :md="8">
          <a-form-item label="商品" name="product_key" :rules="[{ required: true, message: '请选择商品' }]">
            <a-select v-model:value="form.product_key" :options="productOptions" :loading="loadingProducts" />
          </a-form-item>
        </a-col>
        <a-col :xs="24" :md="8">
          <a-form-item label="平台" name="platform">
            <a-select v-model:value="form.platform" :options="platformOptions" />
          </a-form-item>
        </a-col>
        <a-col :xs="24" :md="8">
          <a-form-item label="语言" name="language">
            <a-select v-model:value="form.language" :options="languageOptions" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-button type="primary" html-type="submit" :loading="generating"><thunderbolt-outlined />生成 Listing</a-button>
      <span class="form-hint">调用大语言模型时可能需要几十秒</span>
    </a-form>
  </a-card>

  <a-result v-if="!result && !generating" status="info" title="尚未生成 Listing" sub-title="配置参数后点击“生成 Listing”查看完整结果" />

  <template v-if="result">
    <a-row :gutter="[16, 16]" class="section-gap">
      <a-col :xs="24" :lg="16">
        <a-card title="Listing 预览">
          <a-descriptions :column="1" bordered size="small">
            <a-descriptions-item label="商品">{{ result.product?.name }}</a-descriptions-item>
            <a-descriptions-item label="标题">
              <a-typography-paragraph :copyable="{ text: result.listing?.title }">{{ result.listing?.title }}</a-typography-paragraph>
            </a-descriptions-item>
            <a-descriptions-item label="描述">
              <a-typography-paragraph :copyable="{ text: result.listing?.description }">{{ result.listing?.description }}</a-typography-paragraph>
            </a-descriptions-item>
            <a-descriptions-item label="后台关键词">{{ result.listing?.backend_keywords }}</a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="8">
        <a-card title="SEO 质量">
          <a-progress type="circle" :percent="result.seo?.score || 0" />
          <a-divider />
          <a-statistic title="关键词覆盖" :value="result.seo?.keyword_coverage || 0" suffix="%" />
          <a-list v-if="result.seo?.issues?.length" size="small" :data-source="result.seo.issues" header="待优化项">
            <template #renderItem="{ item }"><a-list-item><a-tag color="warning">建议</a-tag>{{ item }}</a-list-item></template>
          </a-list>
          <a-alert v-else type="success" show-icon message="未发现明显 SEO 问题" />
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="[16, 16]" class="section-gap">
      <a-col :xs="24" :lg="12">
        <a-card title="核心卖点">
          <a-list :data-source="bulletPoints" bordered>
            <template #renderItem="{ item, index }"><a-list-item><a-tag color="blue">{{ index + 1 }}</a-tag>{{ item }}</a-list-item></template>
          </a-list>
        </a-card>
      </a-col>
      <a-col :xs="24" :lg="12">
        <a-card title="关键词分组">
          <a-descriptions :column="1" bordered size="small">
            <a-descriptions-item v-for="group in keywordGroups" :key="group.key" :label="group.label">
              <a-space wrap><a-tag v-for="keyword in group.values" :key="keyword">{{ keyword }}</a-tag></a-space>
            </a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>
    </a-row>

    <a-card title="竞品对比" class="section-gap">
      <a-table row-key="rank" :columns="competitorColumns" :data-source="result.competitors || []" :pagination="false" :scroll="{ x: 640 }">
        <template #bodyCell="{ column, record }">
          <span v-if="column.key === 'price'">{{ formatCurrency(record.price) }}</span>
          <span v-else-if="column.key === 'rating'">{{ record.rating }} / 5</span>
        </template>
      </a-table>
    </a-card>
  </template>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import {
  Alert as AAlert, Button as AButton, Card as ACard, Col as ACol, Descriptions as ADescriptions,
  DescriptionsItem as ADescriptionsItem, Divider as ADivider, Form as AForm, FormItem as AFormItem,
  List as AList, ListItem as AListItem, Progress as AProgress, Result as AResult, Row as ARow,
  Select as ASelect, Space as ASpace, Statistic as AStatistic, Table as ATable, Tag as ATag,
  TypographyParagraph as ATypographyParagraph, message,
} from 'ant-design-vue'
import { ThunderboltOutlined } from '@ant-design/icons-vue'
import PageHeading from '@/components/PageHeading.vue'
import { listingApi } from '@/services/api'
import { formatCurrency } from '@/utils/format'

const form = reactive({ product_key: 'earbuds', platform: 'amazon', language: 'en' })
const products = ref([])
const result = ref()
const loadingProducts = ref(false)
const generating = ref(false)

const platformOptions = [{ label: 'Amazon', value: 'amazon' }, { label: 'TikTok Shop', value: 'tiktok' }]
const languageOptions = [{ label: '英文', value: 'en' }, { label: '中文', value: 'zh' }, { label: '西班牙文', value: 'es' }, { label: '日文', value: 'ja' }]
const competitorColumns = [
  { title: '排名', dataIndex: 'rank', key: 'rank', width: 80 },
  { title: '标题', dataIndex: 'title', key: 'title' },
  { title: '价格', key: 'price', width: 120 },
  { title: '评分', key: 'rating', width: 100 },
  { title: '评论数', dataIndex: 'reviews', key: 'reviews', width: 110 },
  { title: 'BSR', dataIndex: 'bsr', key: 'bsr', width: 100 },
]

const productOptions = computed(() => products.value.map(item => ({ label: `${item.name} · ${formatCurrency(item.price)}`, value: item.key })))
const bulletPoints = computed(() => [1, 2, 3, 4, 5].map(index => result.value?.listing?.[`bullet${index}`]).filter(Boolean))
const keywordGroups = computed(() => [
  { key: 'primary', label: '核心关键词', values: result.value?.keywords?.primary || [] },
  { key: 'secondary', label: '扩展关键词', values: result.value?.keywords?.secondary || [] },
  { key: 'backend', label: '后台关键词', values: result.value?.keywords?.backend || [] },
])

async function generate() {
  generating.value = true
  try {
    result.value = await listingApi.generate({ ...form })
    message.success('Listing 生成完成')
  } catch (error) {
    message.error(error.message)
  } finally {
    generating.value = false
  }
}

onMounted(async () => {
  loadingProducts.value = true
  try {
    products.value = await listingApi.products()
  } catch (error) {
    message.error(error.message)
  } finally {
    loadingProducts.value = false
  }
})
</script>
