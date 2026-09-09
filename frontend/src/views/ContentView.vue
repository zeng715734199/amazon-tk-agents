<template>
  <page-heading title="TikTok 内容" description="生成短视频脚本、直播话术并安排内容日历" />

  <a-row :gutter="[16, 16]">
    <a-col :xs="24" :xl="9">
      <a-card title="内容生成器">
        <a-form layout="vertical" :model="form">
          <a-form-item label="产品名称" required><a-input v-model:value="form.product_name" placeholder="例如：ProSound X1 Earbuds" /></a-form-item>
          <a-form-item label="产品特点" required><a-textarea v-model:value="form.features" :rows="3" placeholder="多个特点请用逗号分隔" /></a-form-item>
          <a-form-item label="视频格式"><a-select v-model:value="form.format_type" :options="formatOptions" :loading="loading" /></a-form-item>
          <a-form-item label="语言"><a-select v-model:value="form.language" :options="languageOptions" /></a-form-item>
          <a-row :gutter="12">
            <a-col :span="12"><a-form-item label="原价"><a-input-number v-model:value="form.price" :min="0" :precision="2" prefix="$" style="width: 100%" /></a-form-item></a-col>
            <a-col :span="12"><a-form-item label="直播价"><a-input-number v-model:value="form.promo_price" :min="0" :precision="2" prefix="$" style="width: 100%" /></a-form-item></a-col>
          </a-row>
          <a-space>
            <a-button type="primary" :loading="generating === 'script'" @click="generateScript"><video-camera-outlined />生成视频脚本</a-button>
            <a-button :loading="generating === 'live'" @click="generateLive"><audio-outlined />生成直播话术</a-button>
          </a-space>
        </a-form>
      </a-card>

      <a-card title="热门内容方向" class="section-gap">
        <a-space wrap>
          <a-tag color="blue">#TikTokMadeMeBuyIt</a-tag>
          <a-tag color="cyan">#Unboxing</a-tag>
          <a-tag color="purple">#ProductReview</a-tag>
          <a-tag color="green">#LifeHack</a-tag>
          <a-tag color="orange">#TikTokShop</a-tag>
        </a-space>
      </a-card>
    </a-col>

    <a-col :xs="24" :xl="15">
      <a-card title="生成结果" :loading="Boolean(generating)">
        <a-empty v-if="!result" description="填写左侧参数后生成内容" />
        <template v-else-if="resultType === 'script'">
          <a-alert :message="`格式：${result.format || form.format_type}`" :description="`生成耗时：${result.elapsed_ms || 0} ms`" type="success" show-icon />
          <a-typography-paragraph class="script-content" :copyable="{ text: result.script }">{{ result.script }}</a-typography-paragraph>
          <a-divider />
          <a-space wrap><a-tag v-for="tag in result.hashtags || []" :key="tag" color="blue">{{ tag }}</a-tag></a-space>
        </template>
        <template v-else>
          <a-descriptions :column="1" bordered size="small">
            <a-descriptions-item label="开场">{{ result.sections?.opening }}</a-descriptions-item>
            <a-descriptions-item label="产品介绍">
              <a-list size="small" :data-source="result.sections?.product_intro || []"><template #renderItem="{ item }"><a-list-item>{{ item }}</a-list-item></template></a-list>
            </a-descriptions-item>
            <a-descriptions-item label="互动话术">
              <a-list size="small" :data-source="result.sections?.engagement_hooks || []"><template #renderItem="{ item }"><a-list-item>{{ item }}</a-list-item></template></a-list>
            </a-descriptions-item>
            <a-descriptions-item label="收尾">{{ result.sections?.closing }}</a-descriptions-item>
          </a-descriptions>
        </template>
      </a-card>
    </a-col>
  </a-row>

  <a-card title="7 天内容日历" class="section-gap">
    <a-table row-key="date" :columns="calendarColumns" :data-source="calendar" :loading="loading" :pagination="false" :scroll="{ x: 900 }">
      <template #bodyCell="{ column, record }">
        <a-space v-if="column.key === 'tags'" wrap><a-tag v-for="tag in record.hashtag_set" :key="tag">{{ tag }}</a-tag></a-space>
      </template>
    </a-table>
  </a-card>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import {
  Alert as AAlert, Button as AButton, Card as ACard, Col as ACol, Descriptions as ADescriptions,
  DescriptionsItem as ADescriptionsItem, Divider as ADivider, Empty as AEmpty, Form as AForm,
  FormItem as AFormItem, Input as AInput, InputNumber as AInputNumber, Textarea as ATextarea,
  List as AList, ListItem as AListItem, Row as ARow, Select as ASelect, Space as ASpace,
  Table as ATable, Tag as ATag, TypographyParagraph as ATypographyParagraph, message,
} from 'ant-design-vue'
import { AudioOutlined, VideoCameraOutlined } from '@ant-design/icons-vue'
import PageHeading from '@/components/PageHeading.vue'
import { contentApi } from '@/services/api'

const form = reactive({
  product_name: 'ProSound X1 Earbuds',
  features: '主动降噪, 40 小时续航, IPX5 防水',
  format_type: 'unboxing',
  language: 'zh',
  price: 39.99,
  promo_price: 29.99,
})
const formatOptions = ref([])
const calendar = ref([])
const loading = ref(false)
const generating = ref('')
const resultType = ref('')
const result = ref()

const languageOptions = [{ label: '中文', value: 'zh' }, { label: '英文', value: 'en' }]
const calendarColumns = [
  { title: '日期', dataIndex: 'date', key: 'date', width: 120 },
  { title: '星期', dataIndex: 'day', key: 'day', width: 110 },
  { title: '商品', dataIndex: 'product', key: 'product', width: 190 },
  { title: '内容格式', dataIndex: 'format_name', key: 'format', width: 210 },
  { title: '时长', dataIndex: 'duration', key: 'duration', width: 100 },
  { title: '发布时间', dataIndex: 'post_time', key: 'post_time', width: 130 },
  { title: '标签', key: 'tags', width: 300 },
  { title: '备注', dataIndex: 'notes', key: 'notes', width: 180 },
]

function features() {
  return form.features.split(/[,，\n]/).map(item => item.trim()).filter(Boolean)
}

function validate() {
  if (!form.product_name.trim() || !features().length) {
    message.warning('请填写产品名称和产品特点')
    return false
  }
  return true
}

async function generateScript() {
  if (!validate()) return
  generating.value = 'script'
  try {
    result.value = await contentApi.script({ product_name: form.product_name, features: features(), format_type: form.format_type, language: form.language })
    resultType.value = 'script'
  } catch (error) {
    message.error(error.message)
  } finally {
    generating.value = ''
  }
}

async function generateLive() {
  if (!validate()) return
  generating.value = 'live'
  try {
    result.value = await contentApi.live({ product_name: form.product_name, features: features(), price: form.price, promo_price: form.promo_price })
    resultType.value = 'live'
  } catch (error) {
    message.error(error.message)
  } finally {
    generating.value = ''
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const [formats, calendarResult] = await Promise.all([contentApi.formats(), contentApi.calendar()])
    formatOptions.value = formats.map(item => ({ label: `${item.name}（${item.duration}）`, value: item.key }))
    calendar.value = calendarResult.calendar || []
  } catch (error) {
    message.error(error.message)
  } finally {
    loading.value = false
  }
})
</script>
