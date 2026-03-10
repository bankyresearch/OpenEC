import { useEffect, useState } from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js'
import { Line, Doughnut, Bar } from 'react-chartjs-2'
import { fetchAPI, groupBy, formatCurrency, formatNumber, getChartColors } from '../api/client'
import KPICard from '../components/KPICard'
import ChartCard from '../components/ChartCard'
import DataTable from '../components/DataTable'
import type { OrderSummary, SalesHistorical, CampaignPerformance, InventoryLevel } from '../types/models'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, ArcElement, Title, Tooltip, Legend)

export default function Overview() {
  const [orders, setOrders] = useState<OrderSummary[]>([])
  const [sales, setSales] = useState<SalesHistorical[]>([])
  const [marketing, setMarketing] = useState<CampaignPerformance[]>([])
  const [inventory, setInventory] = useState<InventoryLevel[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetchAPI<OrderSummary[]>('/orders/summary'),
      fetchAPI<SalesHistorical[]>('/sales/historical'),
      fetchAPI<CampaignPerformance[]>('/campaigns/performance'),
      fetchAPI<InventoryLevel[]>('/levels/current'),
    ]).then(([o, s, m, i]) => {
      setOrders(o); setSales(s); setMarketing(m); setInventory(i)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20 text-gray-400">Loading dashboard...</div>

  const totalRevenue = orders.reduce((s, o) => s + o.total_revenue, 0)
  const totalOrders = orders.reduce((s, o) => s + o.total_orders, 0)
  const avgAOV = totalOrders > 0 ? totalRevenue / totalOrders : 0
  const totalProducts = new Set(sales.map(s => s.sku)).size

  // Revenue trend by date
  const revenueByDate = groupBy(orders, 'date', ['total_revenue'])

  // Sales by category
  const salesByCat = groupBy(sales, 'category', ['revenue'])
  const catLabels = salesByCat.map(c => String(c.category))
  const catValues = salesByCat.map(c => Number(c.revenue))

  // Marketing ROAS by channel
  const mktByChannel = groupBy(marketing, 'channel', ['spend', 'revenue'])

  // Inventory status counts
  const statusCounts: Record<string, number> = {}
  inventory.forEach(i => { statusCounts[i.status] = (statusCounts[i.status] || 0) + 1 })

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Overview</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Total Revenue (30d)" value={formatCurrency(totalRevenue)} />
        <KPICard title="Total Orders (30d)" value={formatNumber(totalOrders)} />
        <KPICard title="Average Order Value" value={formatCurrency(avgAOV)} />
        <KPICard title="Products Tracked" value={formatNumber(totalProducts)} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="Revenue Trend (30d)">
          <Line
            data={{
              labels: revenueByDate.map(d => String(d.date).slice(5)),
              datasets: [{
                label: 'Revenue',
                data: revenueByDate.map(d => Number(d.total_revenue)),
                borderColor: '#3b82f6',
                backgroundColor: '#3b82f620',
                tension: 0.3,
                fill: true,
              }],
            }}
            options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }}
          />
        </ChartCard>

        <ChartCard title="Sales by Category">
          <Doughnut
            data={{
              labels: catLabels,
              datasets: [{
                data: catValues,
                backgroundColor: getChartColors(catLabels.length),
              }],
            }}
            options={{ responsive: true, maintainAspectRatio: false }}
          />
        </ChartCard>

        <ChartCard title="Marketing: Spend vs Revenue by Channel">
          <Bar
            data={{
              labels: mktByChannel.map(m => String(m.channel)),
              datasets: [
                { label: 'Spend', data: mktByChannel.map(m => Number(m.spend)), backgroundColor: '#ef4444' },
                { label: 'Revenue', data: mktByChannel.map(m => Number(m.revenue)), backgroundColor: '#10b981' },
              ],
            }}
            options={{ responsive: true, maintainAspectRatio: false }}
          />
        </ChartCard>

        <ChartCard title="Inventory Status">
          <Doughnut
            data={{
              labels: Object.keys(statusCounts),
              datasets: [{
                data: Object.values(statusCounts),
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
              }],
            }}
            options={{ responsive: true, maintainAspectRatio: false }}
          />
        </ChartCard>
      </div>

      <DataTable
        columns={[
          { key: 'date', label: 'Date' },
          { key: 'total_orders', label: 'Orders', align: 'right' },
          { key: 'total_revenue', label: 'Revenue', align: 'right', format: v => formatCurrency(Number(v)) },
          { key: 'average_order_value', label: 'AOV', align: 'right', format: v => formatCurrency(Number(v)) },
          { key: 'marketplace', label: 'Marketplace' },
        ]}
        data={orders}
      />
    </div>
  )
}
