<template>
  <page-heading title="智能客服" description="模拟 TikTok Shop 与 Amazon 的客户咨询处理" />

  <a-row :gutter="[16, 16]">
    <a-col :xs="24" :xl="16">
      <a-card title="客服会话">
        <template #extra>
          <a-select v-model:value="platform" :options="platformOptions" style="width: 150px" />
        </template>

        <div ref="messageList" class="chat-list">
          <a-empty v-if="!messages.length" description="暂无消息" />
          <div v-for="item in messages" :key="item.id" class="chat-row" :class="{ customer: item.role === 'customer' }">
            <a-avatar :style="{ backgroundColor: item.role === 'customer' ? '#1677ff' : '#52c41a' }">
              <user-outlined v-if="item.role === 'customer'" />
              <robot-outlined v-else />
            </a-avatar>
            <div class="chat-bubble">
              <div class="chat-meta-line">{{ item.role === 'customer' ? '客户' : 'AgentHub' }} · {{ item.time }}</div>
              <div>{{ item.content }}</div>
            </div>
          </div>
          <div v-if="sending" class="chat-row">
            <a-avatar style="background-color: #52c41a"><robot-outlined /></a-avatar>
            <div class="chat-bubble"><a-spin size="small" /> 正在生成回复...</div>
          </div>
        </div>

        <a-space wrap class="quick-replies">
          <a-button v-for="text in quickReplies" :key="text" size="small" @click="sendQuickReply(text)">{{ text }}</a-button>
        </a-space>
        <a-input-search v-model:value="draft" enter-button="发送" size="large" placeholder="输入客户消息" :loading="sending" @search="sendMessage" />
      </a-card>
    </a-col>

    <a-col :xs="24" :xl="8">
      <a-space direction="vertical" size="middle" style="width: 100%">
        <a-card title="今日服务统计" :loading="loadingStats">
          <a-row :gutter="[12, 12]">
            <a-col :span="12"><a-statistic title="会话量" :value="stats?.today?.total || 0" /></a-col>
            <a-col :span="12"><a-statistic title="自动解决" :value="stats?.today?.auto_resolved || 0" /></a-col>
            <a-col :span="12"><a-statistic title="转人工" :value="stats?.today?.escalated || 0" /></a-col>
            <a-col :span="12"><a-statistic title="平均响应" :value="stats?.today?.avg_response_ms || 0" suffix=" ms" /></a-col>
          </a-row>
        </a-card>

        <a-card title="本次识别结果">
          <a-empty v-if="!lastResult" description="发送消息后显示" />
          <a-descriptions v-else :column="1" size="small" bordered>
            <a-descriptions-item label="意图">{{ intentNames[lastResult.intent] || lastResult.intent }}</a-descriptions-item>
            <a-descriptions-item label="语言">{{ lastResult.language === 'zh' ? '中文' : '英文' }}</a-descriptions-item>
            <a-descriptions-item label="响应时间">{{ lastResult.elapsed_ms }} ms</a-descriptions-item>
            <a-descriptions-item label="处理方式">
              <a-tag :color="lastResult.escalated ? 'error' : 'success'">{{ lastResult.escalated ? '转人工' : '自动回复' }}</a-tag>
            </a-descriptions-item>
          </a-descriptions>
        </a-card>

        <a-card title="订单与知识库">
          <a-empty v-if="!lastResult" description="暂无匹配信息" />
          <template v-else>
            <a-descriptions v-if="lastResult.order_info?.found" :column="1" size="small" bordered title="订单信息">
              <a-descriptions-item label="状态">{{ lastResult.order_info.status }}</a-descriptions-item>
              <a-descriptions-item label="商品">{{ lastResult.order_info.items?.join('、') }}</a-descriptions-item>
              <a-descriptions-item label="物流单号">{{ lastResult.order_info.tracking || '--' }}</a-descriptions-item>
            </a-descriptions>
            <a-list v-if="lastResult.kb_results?.length" size="small" :data-source="lastResult.kb_results" header="知识库匹配">
              <template #renderItem="{ item }"><a-list-item>{{ item.category }}（{{ Math.round((item.score || 0) * 100) }}%）</a-list-item></template>
            </a-list>
            <a-empty v-if="!lastResult.order_info?.found && !lastResult.kb_results?.length" description="没有匹配到订单或知识库" />
          </template>
        </a-card>
      </a-space>
    </a-col>
  </a-row>
</template>

<script setup>
import { nextTick, onMounted, ref } from 'vue'
import {
  Avatar as AAvatar, Button as AButton, Card as ACard, Col as ACol,
  Descriptions as ADescriptions, DescriptionsItem as ADescriptionsItem, Empty as AEmpty,
  InputSearch as AInputSearch, List as AList, ListItem as AListItem, Row as ARow,
  Select as ASelect, Space as ASpace, Spin as ASpin, Statistic as AStatistic, Tag as ATag, message,
} from 'ant-design-vue'
import { RobotOutlined, UserOutlined } from '@ant-design/icons-vue'
import PageHeading from '@/components/PageHeading.vue'
import { customerServiceApi } from '@/services/api'

const platform = ref('tiktok')
const draft = ref('')
const sending = ref(false)
const loadingStats = ref(false)
const stats = ref()
const lastResult = ref()
const messageList = ref()
const messages = ref([
  { id: 1, role: 'agent', content: '您好，我是 AgentHub 智能客服。请选择快捷问题或直接输入消息。', time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) },
])

const platformOptions = [{ label: 'TikTok Shop', value: 'tiktok' }, { label: 'Amazon', value: 'amazon' }]
const intentNames = { logistics: '物流咨询', pre_sale: '售前咨询', after_sale: '售后服务', complaint: '投诉', general: '一般咨询' }
const quickReplies = [
  '我的订单 ORD-20250305-002 到哪了？',
  '收到的商品有损坏，我想退货',
  '有哪些尺码可选？',
  '你们支持批发价格吗？',
]

async function scrollToBottom() {
  await nextTick()
  if (messageList.value) messageList.value.scrollTop = messageList.value.scrollHeight
}

async function sendMessage(value = draft.value) {
  const content = String(value || '').trim()
  if (!content || sending.value) return
  messages.value.push({ id: Date.now(), role: 'customer', content, time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) })
  draft.value = ''
  sending.value = true
  await scrollToBottom()
  try {
    const result = await customerServiceApi.chat({ message: content, platform: platform.value })
    lastResult.value = result
    messages.value.push({ id: Date.now() + 1, role: 'agent', content: result.response, time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }) })
  } catch (error) {
    message.error(error.message)
  } finally {
    sending.value = false
    scrollToBottom()
  }
}

function sendQuickReply(text) {
  draft.value = text
  sendMessage(text)
}

onMounted(async () => {
  loadingStats.value = true
  try {
    stats.value = await customerServiceApi.stats()
  } catch (error) {
    message.error(error.message)
  } finally {
    loadingStats.value = false
  }
})
</script>
