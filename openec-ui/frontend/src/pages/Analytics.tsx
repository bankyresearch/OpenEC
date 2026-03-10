import { useEffect, useState } from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { Bar, Line } from 'react-chartjs-2'
import { fetchAPI, groupBy, formatNumber, formatPercent } from '../api/client'
import KPICard from '../components/KPICard'
import ChartCard from '../components/ChartCard'
import DataTable from '../components/DataTable'
import type { FunnelConversion } from '../types/models'

ChartJS.register(CategoryScale, LinearScale, BarElement, PointElement, LineElement, Title, Tooltip, Legend)

const STAGE_ORDER = ['visitors', 'product_views', 'add_to_cart', 'checkout', 'purchase']

export default function Analytics() {
  const [data, setData] = useState<FunnelConversion[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI<FunnelConversion[]>('/funnel/conversion')
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>

  // Aggregate funnel by stage
  const byStage = groupBy(data, 'stage', ['users'])
  const orderedStages = STAGE_ORDER.filter(s => byStage.some(b => b.stage === s))
  const sortedFunnel = orderedStages.map(s => byStage.find(b => b.stage === s)!).filter(Boolean)

  const topStage = sortedFunnel.length > 0 ? Number(sortedFunnel[0].users) : 0
  const bottomStage = sortedFunnel.length > 0 ? Number(sortedFunnel[sortedFunnel.length - 1].users) : 0
  const overallConversion = topStage > 0 ? (bottomStage / topStage) * 100 : 0

  // Daily visitors (sum users per date for the first stage)
  const visitorData = data.filter(d => d.stage === (orderedStages[0] || 'visitors'))
  const byDate = groupBy(visitorData, 'date', ['users'])

  const avgDailyVisitors = byDate.length > 0
    ? byDate.reduce((s, d) => s + Number(d.users), 0) / byDate.length
    : 0

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Total Visitors" value={formatNumber(topStage)} />
        <KPICard title="Total Purchases" value={formatNumber(bottomStage)} />
        <KPICard title="Overall Conversion" value={formatPercent(overallConversion)} />
        <KPICard title="Avg Daily Visitors" value={formatNumber(Math.round(avgDailyVisitors))} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="Conversion Funnel">
          <Bar
            data={{
              labels: sortedFunnel.map(s => String(s.stage).replace(/_/g, ' ')),
              datasets: [{
                label: 'Users',
                data: sortedFunnel.map(s => Number(s.users)),
                backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
              }],
            }}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              indexAxis: 'y',
              plugins: { legend: { display: false } },
            }}
          />
        </ChartCard>

        <ChartCard title="Daily Visitors">
          <Line
            data={{
              labels: byDate.map(d => String(d.date).slice(5)),
              datasets: [{
                label: 'Visitors',
                data: byDate.map(d => Number(d.users)),
                borderColor: '#3b82f6',
                tension: 0.3,
              }],
            }}
            options={{ responsive: true, maintainAspectRatio: false }}
          />
        </ChartCard>
      </div>

      <DataTable
        columns={[
          { key: 'date', label: 'Date' },
          { key: 'stage', label: 'Stage' },
          { key: 'users', label: 'Users', align: 'right', format: v => formatNumber(Number(v)) },
          { key: 'conversion_rate', label: 'Conv. Rate', align: 'right', format: v => formatPercent(Number(v)) },
          { key: 'drop_off_rate', label: 'Drop-off', align: 'right', format: v => formatPercent(Number(v)) },
        ]}
        data={data}
      />
    </div>
  )
}
