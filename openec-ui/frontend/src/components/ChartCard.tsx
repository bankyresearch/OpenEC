import { ReactNode } from 'react'

interface ChartCardProps {
  title: string
  children: ReactNode
  height?: string
}

export default function ChartCard({ title, children, height = 'h-72' }: ChartCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
      <h3 className="text-sm font-semibold text-gray-700 mb-4">{title}</h3>
      <div className={height}>
        {children}
      </div>
    </div>
  )
}
