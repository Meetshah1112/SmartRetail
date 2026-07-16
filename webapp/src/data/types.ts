export interface KpiBlock {
  sales: number
  profit: number
  orders: number
  customers: number
  margin: number
  aov: number
  returnedValue: number
  products: number
  countries: number
  records: number
}

export interface Kpis {
  total: KpiBlock
  delta: { sales: number; profit: number; orders: number; customers: number; margin: number }
  deltaWindow: string
}

export interface MonthlyPoint {
  month: string
  sales: number
  profit: number
  orders: number
}

export interface CategoryRow {
  name: string
  sales: number
  profit: number
  units: number
}

export interface ProductRow {
  name: string
  sales: number
  profit: number
  units: number
}

export interface CustomerRow {
  customer_id: number
  sales: number
  orders: number
  segment: string
}

export interface CountryRow {
  name: string
  sales: number
  customers: number
  orders: number
}

export interface SegmentProfile {
  name: string
  customers: number
  revenue: number
  avgRecency: number
  avgOrders: number
  avgSpend: number
}

export interface RfmPoint {
  recency_days: number
  monetary: number
  segment: string
  frequency: number
}

export interface ForecastPoint {
  month: string
  sales: number | null
  fitted: number
  kind: 'actual' | 'forecast'
}

export interface MovementRow {
  name: string
  products: number
  revenue: number
}

export interface FastMover {
  description: string
  category: string
  sales_velocity: number
  units_sold: number
  days_since_sale?: number
}

export interface DiscountBand {
  band: string
  margin: number
  sales: number
}

export interface DashboardData {
  meta: { title: string; dataset: string; window: string; generated: string; currency: string }
  kpis: Kpis
  monthly: MonthlyPoint[]
  categories: CategoryRow[]
  products: { top: ProductRow[]; scatter: ProductRow[] }
  topCustomers: CustomerRow[]
  countries: CountryRow[]
  patterns: {
    weekday: { day: string; sales: number }[]
    hourly: { hour: number; sales: number }[]
    heatmap: { day: string; month: number; sales: number }[]
  }
  segments: { profile: SegmentProfile[]; scatter: RfmPoint[] }
  forecast: ForecastPoint[]
  inventory: {
    movement: MovementRow[]
    fastest: FastMover[]
    restock: FastMover[]
    deadStock: number
    totalProducts: number
  }
  discountBands: DiscountBand[]
  stats: { meanOrder: number; medianOrder: number; stdOrder: number; ci95: [number, number] }
  models: {
    forecast: { mape: number; mae: number; r2Train: number; algorithm: string }
    classification: {
      logistic: { accuracy: number; f1: number }
      tree: { accuracy: number; f1: number }
      algorithm: string
    }
    hypothesis: { name: string; pValue: string; verdict: string }[]
  }
}

import raw from './dashboard.json'

export const data = raw as unknown as DashboardData
