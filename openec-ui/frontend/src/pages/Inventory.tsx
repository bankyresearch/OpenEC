import { useEffect, useState } from 'react'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend } from 'chart.js'
import { Bar, Doughnut } from 'react-chartjs-2'
import { fetchAPI, formatNumber, getChartColors } from '../api/client'
import KPICard from '../components/KPICard'
import ChartCard from '../components/ChartCard'
import DataTable from '../components/DataTable'
import type { InventoryLevel } from '../types/models'

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Title, Tooltip, Legend)

export default function Inventory() {
  const [data, setData] = useState<InventoryLevel[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAPI<InventoryLevel[]>('/levels/current')
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20 text-gray-400">Loading...</div>

  const totalSKUs = new Set(data.map(d => d.sku)).size
  const lowStock = data.filter(d => d.status === 'low_stock').length
  const outOfStock = data.filter(d => d.status === 'out_of_stock').length
  const avgDaysSupply = data.length > 0 ? data.reduce((s, d) => s + d.days_of_supply, 0) / data.length : 0

  // Stock by warehouse
  const warehouses = [...new Set(data.map(d => d.warehouse))]
  const products = [...new Set(data.map(d => d.name))]

  const statusCounts: Record<string, number> = {}
  data.forEach(d => { statusCounts[d.status] = (statusCounts[d.status] || 0) + 1 })

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Inventory</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Total SKUs" value={formatNumber(totalSKUs)} />
        <KPICard title="Low Stock Items" value={formatNumber(lowStock)} />
        <KPICard title="Out of Stock" value={formatNumber(outOfStock)} />
        <KPICard title="Avg Days of Supply" value={avgDaysSupply.toFixed(1)} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="Quantity by Product">
          <Bar
            data={{
              labels: products.map(p => p.slice(0, 20)),
              datasets: warehouses.map((wh, i) => ({
                label: wh,
                data: products.map(p => {
                  const item = data.find(d => d.name === p && d.warehouse === wh)
                  return item?.quantity || 0
                }),
                backgroundColor: getChartColors(warehouses.length)[i],
              })),
            }}
            options={{ responsive: true, maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true } } }}
          />
        </ChartCard>

        <ChartCard title="Stock Status Distribution">
          <Doughnut
            data={{
              labels: Object.keys(statusCounts).map(s => s.replace('_', ' ')),
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
          { key: 'sku', label: 'SKU' },
          { key: 'name', label: 'Product' },
          { key: 'warehouse', label: 'Warehouse' },
          { key: 'quantity', label: 'Qty', align: 'right' },
          { key: 'status', label: 'Status', format: v => {
            const s = String(v)
            const color = s === 'in_stock' ? 'text-green-600' : s === 'low_stock' ? 'text-amber-600' : 'text-red-600'
            return `${s.replace('_', ' ')}`
          }},
          { key: 'days_of_supply', label: 'Days Supply', align: 'right' },
        ]}
        data={data}
      />
    </div>
  )
}
