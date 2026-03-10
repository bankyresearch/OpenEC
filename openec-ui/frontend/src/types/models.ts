export interface SalesHistorical {
  date: string
  sku: string
  name: string
  category: string
  brand: string
  price: number
  units_sold: number
  revenue: number
  marketplace: string
  rating: number
  review_count: number
}

export interface OrderSummary {
  date: string
  total_orders: number
  total_revenue: number
  average_order_value: number
  total_units: number
  cancelled_orders: number
  returned_orders: number
  marketplace: string
}

export interface CustomerSegment {
  segment: string
  customer_count: number
  percentage: number
  avg_recency_days: number
  avg_frequency: number
  avg_monetary: number
}

export interface InventoryLevel {
  sku: string
  name: string
  quantity: number
  warehouse: string
  status: string
  reorder_point: number
  days_of_supply: number
}

export interface CampaignPerformance {
  date: string
  channel: string
  impressions: number
  clicks: number
  ctr: number
  spend: number
  conversions: number
  revenue: number
  roas: number
  cpc: number
  cpa: number
}

export interface FunnelConversion {
  date: string
  stage: string
  users: number
  conversion_rate: number
  drop_off_rate: number
}

export interface CompetitorPrice {
  date: string
  sku: string
  product_name: string
  competitor: string
  price: number
  marketplace: string
  in_stock: boolean
  price_difference: number
  price_difference_pct: number
}
