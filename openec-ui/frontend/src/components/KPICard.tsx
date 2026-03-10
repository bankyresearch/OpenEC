interface KPICardProps {
  title: string
  value: string
  subtitle?: string
}

export default function KPICard({ title, value, subtitle }: KPICardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
      <p className="text-sm text-gray-500 font-medium">{title}</p>
      <p className="text-2xl font-bold mt-1 text-gray-900">{value}</p>
      {subtitle && <p className="text-xs text-gray-400 mt-1">{subtitle}</p>}
    </div>
  )
}
