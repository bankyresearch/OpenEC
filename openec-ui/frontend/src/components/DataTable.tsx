interface DataTableProps {
  columns: { key: string; label: string; align?: 'left' | 'right'; format?: (v: unknown) => string }[]
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: any[]
  maxRows?: number
}

export default function DataTable({ columns, data, maxRows = 50 }: DataTableProps) {
  const rows = data.slice(0, maxRows)

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 border-b border-gray-100">
              {columns.map(col => (
                <th
                  key={col.key}
                  className={`px-4 py-3 font-semibold text-gray-600 whitespace-nowrap ${
                    col.align === 'right' ? 'text-right' : 'text-left'
                  }`}
                >
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i} className="border-b border-gray-50 hover:bg-gray-50/50">
                {columns.map(col => (
                  <td
                    key={col.key}
                    className={`px-4 py-2.5 whitespace-nowrap ${
                      col.align === 'right' ? 'text-right' : 'text-left'
                    }`}
                  >
                    {col.format ? col.format(row[col.key]) : String(row[col.key] ?? '')}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {data.length > maxRows && (
        <div className="px-4 py-2 text-xs text-gray-400 bg-gray-50 border-t">
          Showing {maxRows} of {data.length} rows
        </div>
      )}
    </div>
  )
}
