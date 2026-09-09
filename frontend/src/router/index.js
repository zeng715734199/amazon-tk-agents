import { createRouter, createWebHashHistory } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'

const routes = [
  {
    path: '/',
    component: AppLayout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'dashboard', component: () => import('@/views/DashboardView.vue'), meta: { title: '总览面板', description: '核心业务指标与运营状态' } },
      { path: 'customer-service', name: 'customer-service', component: () => import('@/views/CustomerServiceView.vue'), meta: { title: '智能客服', description: '多平台客户咨询与服务分析' } },
      { path: 'listing', name: 'listing', component: () => import('@/views/ListingView.vue'), meta: { title: 'Listing 生成', description: '生成商品文案并检查 SEO 质量' } },
      { path: 'content', name: 'content', component: () => import('@/views/ContentView.vue'), meta: { title: 'TikTok 内容', description: '短视频脚本、直播话术与内容日历' } },
      { path: 'competitor', name: 'competitor', component: () => import('@/views/CompetitorView.vue'), meta: { title: '竞品监控', description: '竞品价格、排名与定价建议' } },
      { path: 'supply-chain', name: 'supply-chain', component: () => import('@/views/SupplyChainView.vue'), meta: { title: '供应链管理', description: '多仓库存、补货计划与需求预测' } },
      { path: 'profit', name: 'profit', component: () => import('@/views/ProfitView.vue'), meta: { title: '利润分析', description: '平台损益、成本结构与利润趋势' } },
    ],
  },
  { path: '/:pathMatch(.*)*', redirect: '/dashboard' },
]

export default createRouter({
  history: createWebHashHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})
