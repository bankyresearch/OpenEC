import { useEffect, useState } from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js'
import { Doughnut, Bar } from 'react-chartjs-2'
import { fetchAPI, formatCurrency, formatNumber, getChartColors } from '../api/client'
import KPICard from '../components/KPICard'
import ChartCard from '../components/ChartCard'
import DataTable from '../components/DataTable'
import type { CustomerSegment } from '../types/models'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend)

export default function Customers() {
  const [data, setData] = useState<CustomerSegment[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI<CustomerSegment[]>('/segments/rfm')
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>

  const totalCustomers = data.reduce((s, d) => s + d.customer_count, 0)
  const largest = data.reduce((a, b) => a.customer_count > b.customer_count ? a : b, data[0])
  const highestMonetary = data.reduce((a, b) => a.avg_monetary > b.avg_monetary ? a : b, data[0])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Customers</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Total Customers" value={formatNumber(totalCustomers)} />
        <KPICard title="Segments" value={formatNumber(data.length)} />
        <KPICard title="Largest Segment" value={largest?.segment || '--'} subtitle={`${largest?.customer_count} customers`} />
        <KPICard title="Highest Avg Spend" value={formatCurrency(highestMonetary?.avg_monetary || 0)} subtitle={highestMonetary?.segment} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="Customer Segment Distribution">
          <Doughnut
            data={{
              labels: data.map(d => d.segment),
              datasets: [{
                data: data.map(d => d.customer_count),
                backgroundColor: getChartColors(data.length),
              }],
            }}
            options={{ responsive: true, maintainAspectRatio: false }}
          />
        </ChartCard>

        <ChartCard title="RFM Breakdown by Segment">
          <Bar
            data={{
              labels: data.map(d => d.segment),
              datasets: [
                { label: 'Avg Recency (days)', data: data.map(d => d.avg_recency_days), backgroundColor: '#3b82f6' },
                { label: 'Avg Frequency', data: data.map(d => d.avg_frequency), backgroundColor: '#10b981' },
                { label: 'Avg Monetary ($)', data: data.map(d => d.avg_monetary), backgroundColor: '#f59e0b' },
              ],
            }}
            options={{ responsive: true, maintainAspectRatio: false }}
          />
        </ChartCard>
      </div>

      <DataTable
        columns={[
          { key: 'segment', label: 'Segment' },
          { key: 'customer_count', label: 'Customers', align: 'right' },
          { key: 'percentage', label: '%', align: 'right', format: v => `${Number(v).toFixed(1)}%` },
          { key: 'avg_recency_days', label: 'Avg Recency', align: 'right' },
          { key: 'avg_frequency', label: 'Avg Frequency', align: 'right' },
          { key: 'avg_monetary', label: 'Avg Spend', align: 'right', format: v => formatCurrency(Number(v)) },
        ]}
        data={data}
      />
    </div>
  )
}
