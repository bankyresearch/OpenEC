const API_BASE = '/api/api/v1'

let currentProvider = 'demo'

export function setProvider(provider: string) {
  currentProvider = provider
}

export function getProvider() {
  return currentProvider
}

export async function fetchAPI<T = Record<string, unknown>[]>(path: string): Promise<T> {
  const url = `${API_BASE}${path}?provider=${currentProvider}`
  const res = await fetch(url)
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`)
  const data = await res.json()
  return data.results ?? data
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function groupBy(
  arr: any[],
  key: string,
  sumFields: string[]
): Record<string, unknown>[] {
  const groups: Record<string, Record<string, unknown>> = {}
  for (const item of arr) {
    const k = String(item[key])
    if (!groups[k]) {
      groups[k] = { [key]: k }
      for (const f of sumFields) groups[k][f] = 0
    }
    for (const f of sumFields) {
      groups[k][f] = (groups[k][f] as number) + (Number(item[f]) || 0)
    }
  }
  return Object.values(groups)
}

export function formatCurrency(val: number): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val)
}

export function formatNumber(val: number): string {
  return new Intl.NumberFormat('en-US').format(val)
}

export function formatPercent(val: number): string {
  return `${val.toFixed(1)}%`
}

const CHART_COLORS = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444',
  '#8b5cf6', '#ec4899', '#06b6d4', '#84cc16',
]

export function getChartColors(count: number): string[] {
  return CHART_COLORS.slice(0, count)
}
