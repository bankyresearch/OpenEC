import { useEffect, useState } from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'
import { fetchAPI, groupBy, formatCurrency, formatNumber, getChartColors } from '../api/client'
import KPICard from '../components/KPICard'
import ChartCard from '../components/ChartCard'
import DataTable from '../components/DataTable'
import type { SalesHistorical } from '../types/models'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend)

export default function Products() {
  const [data, setData] = useState<SalesHistorical[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI<SalesHistorical[]>('/sales/historical')
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>

  const totalRevenue = data.reduce((s, r) => s + r.revenue, 0)
  const totalUnits = data.reduce((s, r) => s + r.units_sold, 0)
  const avgRating = data.length > 0 ? data.reduce((s, r) => s + r.rating, 0) / data.length : 0

  const byDate = groupBy(data, 'date', ['units_sold', 'revenue'])
  const byProduct = groupBy(data, 'name', ['revenue'])
    .sort((a, b) => Number(b.revenue) - Number(a.revenue))

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Products</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Total Revenue" value={formatCurrency(totalRevenue)} />
        <KPICard title="Total Units Sold" value={formatNumber(totalUnits)} />
        <KPICard title="Avg Rating" value={avgRating.toFixed(1)} />
        <KPICard title="Products Tracked" value={formatNumber(new Set(data.map(d => d.sku)).size)} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="Daily Units Sold">
          <Line
            data={{
              labels: byDate.map(d => String(d.date).slice(5)),
              datasets: [{
                label: 'Units Sold',
                data: byDate.map(d => Number(d.units_sold)),
                borderColor: '#3b82f6', tension: 0.3, fill: false,
              }],
            }}
            options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }}
          />
        </ChartCard>

        <ChartCard title="Revenue by Product">
          <Bar
            data={{
              labels: byProduct.map(p => String(p.name).slice(0, 20)),
              datasets: [{
                label: 'Revenue',
                data: byProduct.map(p => Number(p.revenue)),
                backgroundColor: getChartColors(byProduct.length),
              }],
            }}
            options={{ responsive: true, maintainAspectRatio: false, indexAxis: 'y', plugins: { legend: { display: false } } }}
          />
        </ChartCard>
      </div>

      <DataTable
        columns={[
          { key: 'date', label: 'Date' },
          { key: 'sku', label: 'SKU' },
          { key: 'name', label: 'Product' },
          { key: 'units_sold', label: 'Units', align: 'right' },
          { key: 'revenue', label: 'Revenue', align: 'right', format: v => formatCurrency(Number(v)) },
          { key: 'marketplace', label: 'Marketplace' },
          { key: 'rating', label: 'Rating', align: 'right' },
        ]}
        data={data}
      />
    </div>
  )
}
