import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import { makeTooltip } from '../components/charts/ChartTooltip'
import { Donut } from '../components/charts/Donut'
import { HBars } from '../components/charts/HBars'
import { ChartCard } from '../components/ui/ChartCard'
import { data } from '../data/types'
import { int, money, truncate } from '../lib/format'
import { SERIES } from '../lib/palette'
import './pages.css'

const { categories, products } = data
const CurrencyTooltip = makeTooltip((v) => money(v))

export function Products() {
  return (
    <div className="page grid" style={{ gap: 'var(--gap)' }}>
      <div className="grid cols-2-1">
        <ChartCard title="Sales & Profit by Category" subtitle="Estimated profit uses the 70%-cost assumption">
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categories} margin={{ top: 8, right: 8, bottom: 42, left: 0 }}>
              <CartesianGrid vertical={false} strokeDasharray="3 4" />
              <XAxis
                dataKey="name"
                tickLine={false}
                axisLine={false}
                interval={0}
                angle={-28}
                textAnchor="end"
                tickFormatter={(v: string) => truncate(v, 16)}
              />
              <YAxis tickLine={false} axisLine={false} width={52} tickFormatter={(v: number) => money(v, 1)} />
              <Tooltip content={<CurrencyTooltip />} cursor={{ fill: 'var(--accent-soft)' }} />
              <Legend />
              <Bar isAnimationActive={false} dataKey="sales" name="Sales" fill="#6c4ee0" radius={[5, 5, 0, 0]} />
              <Bar isAnimationActive={false} dataKey="profit" name="Est. profit" fill="#17b8a0" radius={[5, 5, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Category Share">
          <Donut
            data={categories.slice(0, 6).map((c) => ({ name: c.name, value: c.sales }))}
            colors={SERIES}
            height={240}
            maxLegend={6}
          />
        </ChartCard>
      </div>

      <div className="grid cols-2">
        <ChartCard title="Best Sellers" subtitle="Top 10 products by revenue">
          <HBars data={products.top.map((p) => ({ label: p.name, value: p.sales }))} />
        </ChartCard>

        <ChartCard title="Category Detail">
          <table className="data-table">
            <thead>
              <tr>
                <th>Category</th>
                <th className="num">Units</th>
                <th className="num">Sales</th>
                <th className="num">Est. profit</th>
                <th className="num">Margin</th>
              </tr>
            </thead>
            <tbody>
              {categories.map((c) => (
                <tr key={c.name}>
                  <td>{c.name}</td>
                  <td className="num">{int(c.units)}</td>
                  <td className="num">{money(c.sales)}</td>
                  <td className="num">{money(c.profit)}</td>
                  <td className="num">{((c.profit / c.sales) * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </ChartCard>
      </div>
    </div>
  )
}
