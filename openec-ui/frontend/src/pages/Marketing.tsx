import { useEffect, useState } from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'
import { fetchAPI, groupBy, formatCurrency, formatNumber } from '../api/client'
import KPICard from '../components/KPICard'
import ChartCard from '../components/ChartCard'
import DataTable from '../components/DataTable'
import type { CampaignPerformance } from '../types/models'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend)

export default function Marketing() {
  const [data, setData] = useState<CampaignPerformance[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI<CampaignPerformance[]>('/campaigns/performance')
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>

  const totalSpend = data.reduce((s, d) => s + d.spend, 0)
  const totalRevenue = data.reduce((s, d) => s + d.revenue, 0)
  const avgROAS = totalSpend > 0 ? totalRevenue / totalSpend : 0

  const byChannel = groupBy(data, 'channel', ['spend', 'revenue', 'conversions'])
  const bestChannel = byChannel.reduce((a, b) => {
    const roasA = Number(a.spend) > 0 ? Number(a.revenue) / Number(a.spend) : 0
    const roasB = Number(b.spend) > 0 ? Number(b.revenue) / Number(b.spend) : 0
    return roasA > roasB ? a : b
  }, byChannel[0])

  const byDate = groupBy(data, 'date', ['spend', 'revenue'])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Marketing</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Total Spend" value={formatCurrency(totalSpend)} />
        <KPICard title="Total Revenue" value={formatCurrency(totalRevenue)} />
        <KPICard title="Average ROAS" value={`${avgROAS.toFixed(2)}x`} />
        <KPICard title="Best Channel" value={String(bestChannel?.channel || '--')} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="Daily Spend vs Revenue">
          <Line
            data={{
              labels: byDate.map(d => String(d.date).slice(5)),
              datasets: [
                { label: 'Spend', data: byDate.map(d => Number(d.spend)), borderColor: '#ef4444', tension: 0.3 },
                { label: 'Revenue', data: byDate.map(d => Number(d.revenue)), borderColor: '#10b981', tension: 0.3 },
              ],
            }}
            options={{ responsive: true, maintainAspectRatio: false }}
          />
        </ChartCard>

        <ChartCard title="ROAS by Channel">
          <Bar
            data={{
              labels: byChannel.map(c => String(c.channel)),
              datasets: [{
                label: 'ROAS',
                data: byChannel.map(c => Number(c.spend) > 0 ? Number(c.revenue) / Number(c.spend) : 0),
                backgroundColor: '#8b5cf6',
              }],
            }}
            options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }}
          />
        </ChartCard>
      </div>

      <DataTable
        columns={[
          { key: 'date', label: 'Date' },
          { key: 'channel', label: 'Channel' },
          { key: 'impressions', label: 'Impressions', align: 'right', format: v => formatNumber(Number(v)) },
          { key: 'clicks', label: 'Clicks', align: 'right', format: v => formatNumber(Number(v)) },
          { key: 'spend', label: 'Spend', align: 'right', format: v => formatCurrency(Number(v)) },
          { key: 'revenue', label: 'Revenue', align: 'right', format: v => formatCurrency(Number(v)) },
          { key: 'roas', label: 'ROAS', align: 'right', format: v => `${Number(v).toFixed(2)}x` },
        ]}
        data={data}
      />
    </div>
  )
}
