<template>
  <a-layout class="app-layout" :class="{ 'is-collapsed': collapsed }">
    <a-layout-sider
      ref="siderRef"
      v-model:collapsed="collapsed"
      collapsible
      theme="light"
      :width="220"
      :collapsed-width="72"
      class="shell-sider"
    >
      <div class="brand" @click="router.push('/dashboard')">
        <div class="brand-mark">A</div>
        <strong v-if="!collapsed">Amazon&Tk Agent</strong>
      </div>
      <a-menu mode="inline" :selected-keys="selectedKeys" @click="navigate">
        <a-menu-item v-for="item in navigation" :key="item.name">
          <component :is="item.icon" />
          <span>{{ item.label }}</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <a-layout class="shell-main">
      <a-layout-header class="shell-header">
        <div class="header-title">
          <strong>{{ route.meta.title }}</strong>
          <span>{{ route.meta.description }}</span>
        </div>
        <div class="header-actions">
          <a-tag :color="online ? 'success' : 'error'">{{ online ? '系统在线' : '连接异常' }}</a-tag>
          <a-input
            ref="commandInput"
            v-model:value="command"
            allow-clear
            class="command-box"
            placeholder="输入模块名称，按 Enter 跳转"
            @press-enter="runCommand"
          >
            <template #prefix><search-outlined /></template>
          </a-input>
          <a-dropdown>
            <a-button><download-outlined />导出</a-button>
            <template #overlay>
              <a-menu @click="handleExport">
                <a-menu-item key="summary">运营摘要 CSV</a-menu-item>
                <a-menu-item key="print">打印当前页面</a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
          <a-button @click="tourOpen = true"><question-circle-outlined />引导</a-button>
          <a-button @click="toggleFullscreen"><fullscreen-outlined />全屏</a-button>
          <span class="header-clock">{{ clock }}</span>
        </div>
      </a-layout-header>

      <a-layout-content ref="contentRef" class="shell-content">
        <router-view />
      </a-layout-content>
    </a-layout>
  </a-layout>

  <a-tour v-model:current="tourCurrent" :open="tourOpen" :steps="tourSteps" @close="tourOpen = false" />
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Layout as ALayout, LayoutSider as ALayoutSider, LayoutHeader as ALayoutHeader,
  LayoutContent as ALayoutContent, Menu as AMenu, MenuItem as AMenuItem,
  Input as AInput, Button as AButton, Dropdown as ADropdown, Tag as ATag,
  Tour as ATour, message, notification,
} from 'ant-design-vue'
import {
  AppstoreOutlined, CustomerServiceOutlined, FileTextOutlined, VideoCameraOutlined,
  EyeOutlined, CarOutlined, DollarOutlined, SearchOutlined, DownloadOutlined,
  QuestionCircleOutlined, FullscreenOutlined,
} from '@ant-design/icons-vue'
import { systemApi } from '@/services/api'
import { downloadCsv } from '@/utils/export'

const router = useRouter()
const route = useRoute()
const collapsed = ref(false)
const online = ref(false)
const command = ref('')
const commandInput = ref()
const siderRef = ref()
const contentRef = ref()
const clock = ref('')
const tourOpen = ref(false)
const tourCurrent = ref(0)

const navigation = [
  { name: 'dashboard', label: '总览面板', icon: AppstoreOutlined, keywords: ['总览', '首页', 'dashboard'] },
  { name: 'customer-service', label: '智能客服', icon: CustomerServiceOutlined, keywords: ['客服', '消息', 'customer'] },
  { name: 'listing', label: 'Listing 生成', icon: FileTextOutlined, keywords: ['listing', '商品文案'] },
  { name: 'content', label: 'TikTok 内容', icon: VideoCameraOutlined, keywords: ['内容', '脚本', 'tiktok', '直播'] },
  { name: 'competitor', label: '竞品监控', icon: EyeOutlined, keywords: ['竞品', '价格'] },
  { name: 'supply-chain', label: '供应链管理', icon: CarOutlined, keywords: ['供应链', '库存', '补货'] },
  { name: 'profit', label: '利润分析', icon: DollarOutlined, keywords: ['利润', '成本', 'profit'] },
]

const selectedKeys = computed(() => [route.name])
const tourSteps = computed(() => [
  { title: '业务导航', description: '通过左侧菜单切换七个业务模块。', placement: 'right', target: () => siderRef.value?.$el },
  { title: '快捷命令', description: '输入模块名称或按 Ctrl+K 快速定位。', placement: 'bottom', target: () => commandInput.value?.$el },
  { title: '页面内容', description: '每个模块的数据、表格和图表都在这里展示。', placement: 'rightTop', target: () => contentRef.value?.$el },
])

const SIMULATION_EVENTS = [
  () => ({ icon: '🛒', title: '新订单', message: `${['ProSound X1 耳机', 'ZenFlex 瑜伽垫', 'LumiPro 台灯'][Math.floor(Math.random() * 3)]} — ${['Amazon', 'TikTok Shop'][Math.floor(Math.random() * 2)]}` }),
  () => ({ icon: '📦', title: '库存预警', message: `${['ZenFlex 瑜伽垫 Teal 款', 'ProSound X1 白色款', 'LumiPro 台灯 黑色款'][Math.floor(Math.random() * 3)]} FBA 库存低于安全线` }),
  () => ({ icon: '💰', title: '竞品降价', message: ['SoundCore A40 降至 $33.99', 'YogaPro Mat 降至 $24.99', 'BrightDesk LED 降至 $28.99'][Math.floor(Math.random() * 3)] }),
  () => ({ icon: '⭐', title: '新评论', message: `${['ProSound X1 收到 5 星好评', 'ZenFlex 瑜伽垫 收到 4 星评价', 'LumiPro 台灯 收到 5 星好评'][Math.floor(Math.random() * 3)]}` }),
]
let simulationTimer = null

function scheduleSimulation() {
  const delay = 8000 + Math.random() * 4000
  simulationTimer = window.setTimeout(() => {
    const event = SIMULATION_EVENTS[Math.floor(Math.random() * SIMULATION_EVENTS.length)]()
    notification.open({
      message: event.title,
      description: event.message,
      icon: () => event.icon,
      placement: 'bottomRight',
      duration: 4.5,
    })
    scheduleSimulation()
  }, delay)
}

function navigate({ key }) {
  router.push({ name: key })
}

function runCommand() {
  const keyword = command.value.trim().toLowerCase()
  if (!keyword) return
  const target = navigation.find(item => item.label.toLowerCase().includes(keyword)
    || item.keywords.some(itemKeyword => itemKeyword.includes(keyword) || keyword.includes(itemKeyword)))
  if (!target) {
    message.warning('未找到对应模块')
    return
  }
  router.push({ name: target.name })
  command.value = ''
}

function handleExport({ key }) {
  if (key === 'print') {
    window.print()
    return
  }
  downloadCsv('agenthub-summary.csv', [
    { title: '项目', dataIndex: 'name' },
    { title: '内容', dataIndex: 'value' },
  ], [
    { name: '当前模块', value: route.meta.title },
    { name: '导出时间', value: new Date().toLocaleString('zh-CN') },
    { name: '系统状态', value: online.value ? '在线' : '连接异常' },
  ])
}

async function toggleFullscreen() {
  if (document.fullscreenElement) await document.exitFullscreen()
  else await document.documentElement.requestFullscreen()
}

function updateClock() {
  clock.value = new Date().toLocaleTimeString('zh-CN', { hour12: false })
}

function onShortcut(event) {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    commandInput.value?.focus()
  }
}

onMounted(async () => {
  updateClock()
  const timer = window.setInterval(updateClock, 1000)
  clock.timer = timer
  window.addEventListener('keydown', onShortcut)
  scheduleSimulation()
  try {
    await systemApi.status()
    online.value = true
  } catch {
    online.value = false
  }
})

onBeforeUnmount(() => {
  window.clearInterval(clock.timer)
  window.removeEventListener('keydown', onShortcut)
  window.clearTimeout(simulationTimer)
})
</script>
