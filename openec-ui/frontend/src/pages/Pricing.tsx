import { useEffect, useState } from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { Bar } from 'react-chartjs-2'
import { fetchAPI, formatCurrency, formatPercent, getChartColors } from '../api/client'
import KPICard from '../components/KPICard'
import ChartCard from '../components/ChartCard'
import DataTable from '../components/DataTable'
import type { CompetitorPrice } from '../types/models'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default function Pricing() {
  const [data, setData] = useState<CompetitorPrice[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI<CompetitorPrice[]>('/competitor/current')
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>

  const avgPriceDiff = data.length > 0
    ? data.reduce((s, d) => s + d.price_difference_pct, 0) / data.length
    : 0
  const competitorsSet = new Set(data.map(d => d.competitor))
  const productsSet = new Set(data.map(d => d.product_name))
  const cheaperCount = data.filter(d => d.price_difference > 0).length

  // Grouped bar: our price vs competitors per product
  const products = [...productsSet].slice(0, 8)
  const competitors = [...competitorsSet]
  const colors = getChartColors(competitors.length + 1)

  const comparisonDatasets = competitors.map((comp, i) => ({
    label: comp,
    data: products.map(p => {
      const entry = data.find(d => d.product_name === p && d.competitor === comp)
      return entry ? entry.price : 0
    }),
    backgroundColor: colors[i + 1] || colors[0],
  }))

  // Price difference distribution
  const diffBuckets = [
    { label: '< -10%', min: -Infinity, max: -10 },
    { label: '-10% to -5%', min: -10, max: -5 },
    { label: '-5% to 0%', min: -5, max: 0 },
    { label: '0% to 5%', min: 0, max: 5 },
    { label: '5% to 10%', min: 5, max: 10 },
    { label: '> 10%', min: 10, max: Infinity },
  ]
  const diffCounts = diffBuckets.map(b =>
    data.filter(d => d.price_difference_pct >= b.min && d.price_difference_pct < b.max).length
  )

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Pricing</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Products Tracked" value={String(productsSet.size)} />
        <KPICard title="Competitors" value={String(competitorsSet.size)} />
        <KPICard title="Avg Price Diff" value={formatPercent(avgPriceDiff)} />
        <KPICard title="We're Cheaper" value={`${cheaperCount} / ${data.length}`} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="Price Comparison by Product">
          <Bar
            data={{
              labels: products,
              datasets: comparisonDatasets,
            }}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { position: 'bottom' } },
            }}
          />
        </ChartCard>

        <ChartCard title="Price Difference Distribution">
          <Bar
            data={{
              labels: diffBuckets.map(b => b.label),
              datasets: [{
                label: 'Products',
                data: diffCounts,
                backgroundColor: diffCounts.map((_, i) => i < 3 ? '#ef4444' : '#10b981'),
              }],
            }}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { display: false } },
            }}
          />
        </ChartCard>
      </div>

      <DataTable
        columns={[
          { key: 'product_name', label: 'Product' },
          { key: 'competitor', label: 'Competitor' },
          { key: 'price', label: 'Price', align: 'right', format: v => formatCurrency(Number(v)) },
          { key: 'price_difference', label: 'Diff ($)', align: 'right', format: v => formatCurrency(Number(v)) },
          { key: 'price_difference_pct', label: 'Diff (%)', align: 'right', format: v => formatPercent(Number(v)) },
          { key: 'in_stock', label: 'In Stock', format: v => v ? 'Yes' : 'No' },
        ]}
        data={data}
      />
    </div>
  )
}
