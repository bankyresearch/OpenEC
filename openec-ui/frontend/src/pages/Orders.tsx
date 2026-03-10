import { useEffect, useState } from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { Line } from 'react-chartjs-2'
import { fetchAPI, formatCurrency, formatNumber } from '../api/client'
import KPICard from '../components/KPICard'
import ChartCard from '../components/ChartCard'
import DataTable from '../components/DataTable'
import type { OrderSummary } from '../types/models'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

export default function Orders() {
  const [data, setData] = useState<OrderSummary[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI<OrderSummary[]>('/orders/summary')
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>

  const totalOrders = data.reduce((s, o) => s + o.total_orders, 0)
  const totalRevenue = data.reduce((s, o) => s + o.total_revenue, 0)
  const totalCancelled = data.reduce((s, o) => s + o.cancelled_orders, 0)
  const totalReturned = data.reduce((s, o) => s + o.returned_orders, 0)

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Orders</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Total Orders" value={formatNumber(totalOrders)} />
        <KPICard title="Total Revenue" value={formatCurrency(totalRevenue)} />
        <KPICard title="Cancellation Rate" value={`${((totalCancelled / totalOrders) * 100).toFixed(1)}%`} />
        <KPICard title="Return Rate" value={`${((totalReturned / totalOrders) * 100).toFixed(1)}%`} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="Orders & Revenue Trend">
          <Line
            data={{
              labels: data.map(d => d.date.slice(5)),
              datasets: [
                { label: 'Orders', data: data.map(d => d.total_orders), borderColor: '#3b82f6', tension: 0.3, yAxisID: 'y' },
                { label: 'Revenue', data: data.map(d => d.total_revenue), borderColor: '#10b981', tension: 0.3, yAxisID: 'y1' },
              ],
            }}
            options={{
              responsive: true, maintainAspectRatio: false,
              scales: {
                y: { position: 'left', title: { display: true, text: 'Orders' } },
                y1: { position: 'right', grid: { drawOnChartArea: false }, title: { display: true, text: 'Revenue' } },
              },
            }}
          />
        </ChartCard>

        <ChartCard title="Average Order Value Trend">
          <Line
            data={{
              labels: data.map(d => d.date.slice(5)),
              datasets: [{
                label: 'AOV',
                data: data.map(d => d.average_order_value),
                borderColor: '#f59e0b', tension: 0.3, fill: false,
              }],
            }}
            options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }}
          />
        </ChartCard>
      </div>

      <DataTable
        columns={[
          { key: 'date', label: 'Date' },
          { key: 'total_orders', label: 'Orders', align: 'right' },
          { key: 'total_revenue', label: 'Revenue', align: 'right', format: v => formatCurrency(Number(v)) },
          { key: 'average_order_value', label: 'AOV', align: 'right', format: v => formatCurrency(Number(v)) },
          { key: 'cancelled_orders', label: 'Cancelled', align: 'right' },
          { key: 'returned_orders', label: 'Returned', align: 'right' },
          { key: 'marketplace', label: 'Marketplace' },
        ]}
        data={data}
      />
    </div>
  )
}
