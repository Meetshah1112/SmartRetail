import { Fragment } from 'react'
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { makeTooltip } from '../components/charts/ChartTooltip'
import { HBars } from '../components/charts/HBars'
import { TrendArea } from '../components/charts/TrendArea'
import { ChartCard } from '../components/ui/ChartCard'
import { data } from '../data/types'
import { int, money } from '../lib/format'
import { SEGMENT_COLORS } from '../lib/palette'
import './pages.css'

const { monthly, patterns, products, topCustomers, countries } = data
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

const CurrencyTooltip = makeTooltip((v) => money(v))

function Heatmap() {
  const lookup = new Map(patterns.heatmap.map((c) => [`${c.day}-${c.month}`, c.sales]))
  const max = Math.max(...patterns.heatmap.map((c) => c.sales))
  return (
    <div className="heatmap">
      <span />
      {MONTHS.map((m) => (
        <span key={m} className="axis">{m}</span>
      ))}
      {DAYS.map((day) => (
        <Fragment key={day}>
          <span className="axis">{day}</span>
          {MONTHS.map((_, mi) => {
            const sales = lookup.get(`${day}-${mi + 1}`) ?? 0
            return (
              <div
                key={`${day}-${mi}`}
                className="cell"
                title={`${day} · ${MONTHS[mi]} — ${money(sales)}`}
                style={{
                  background: sales
                    ? `color-mix(in srgb, var(--accent) ${Math.round((sales / max) * 88) + 8}%, var(--surface-2))`
                    : 'var(--surface-2)',
                }}
              />
            )
          })}
        </Fragment>
      ))}
    </div>
  )
}

export function Sales() {
  return (
    <div className="page grid" style={{ gap: 'var(--gap)' }}>
      <div className="grid cols-2">
        <ChartCard title="Monthly Sales" subtitle="Strong Sep–Nov seasonal peak both years">
          <TrendArea data={monthly} xKey="month" yKey="sales" name="Sales" color="#6c4ee0" />
        </ChartCard>
        <ChartCard title="Orders per Month">
          <ResponsiveContainer width="100%" height={230}>
            <BarChart data={monthly} margin={{ top: 8, right: 8, bottom: 0, left: 0 }}>
              <CartesianGrid vertical={false} strokeDasharray="3 4" />
              <XAxis dataKey="month" tickLine={false} axisLine={false} interval={2} />
              <YAxis tickLine={false} axisLine={false} width={44} tickFormatter={(v: number) => int(v)} />
              <Tooltip content={<makeTooltipOrders.Component />} cursor={{ fill: 'var(--accent-soft)' }} />
              <Bar isAnimationActive={false} dataKey="orders" name="Orders" fill="#2e9bf0" radius={[5, 5, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="grid cols-2">
        <ChartCard title="Sales by Day of Week" subtitle="The store barely trades on Saturdays">
          <ResponsiveContainer width="100%" height={210}>
            <BarChart data={patterns.weekday} margin={{ top: 8, right: 8, bottom: 0, left: 0 }}>
              <CartesianGrid vertical={false} strokeDasharray="3 4" />
              <XAxis dataKey="day" tickLine={false} axisLine={false} />
              <YAxis tickLine={false} axisLine={false} width={52} tickFormatter={(v: number) => money(v, 1)} />
              <Tooltip content={<CurrencyTooltip />} cursor={{ fill: 'var(--accent-soft)' }} />
              <Bar isAnimationActive={false} dataKey="sales" name="Sales" fill="#6c4ee0" radius={[5, 5, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
        <ChartCard title="Sales by Hour" subtitle="Lunchtime (12:00) is the busiest window">
          <ResponsiveContainer width="100%" height={210}>
            <BarChart data={patterns.hourly} margin={{ top: 8, right: 8, bottom: 0, left: 0 }}>
              <CartesianGrid vertical={false} strokeDasharray="3 4" />
              <XAxis dataKey="hour" tickLine={false} axisLine={false} />
              <YAxis tickLine={false} axisLine={false} width={52} tickFormatter={(v: number) => money(v, 1)} />
              <Tooltip content={<CurrencyTooltip />} cursor={{ fill: 'var(--accent-soft)' }} />
              <Bar isAnimationActive={false} dataKey="sales" name="Sales" fill="#f0862e" radius={[5, 5, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <ChartCard title="Sales Heatmap" subtitle="Weekday × month intensity — darker is stronger">
        <Heatmap />
      </ChartCard>

      <div className="grid cols-3">
        <ChartCard title="Top 10 Products">
          <HBars data={products.top.map((p) => ({ label: p.name, value: p.sales }))} />
        </ChartCard>
        <ChartCard title="Top Customers">
          <table className="data-table">
            <thead>
              <tr><th>Customer</th><th>Segment</th><th className="num">Orders</th><th className="num">Sales</th></tr>
            </thead>
            <tbody>
              {topCustomers.slice(0, 8).map((c) => (
                <tr key={c.customer_id}>
                  <td>#{c.customer_id}</td>
                  <td>
                    <span
                      className="badge"
                      style={{
                        background: `color-mix(in srgb, ${SEGMENT_COLORS[c.segment] ?? '#98a0b8'} 16%, transparent)`,
                        color: SEGMENT_COLORS[c.segment] ?? 'var(--ink-2)',
                      }}
                    >
                      {c.segment ?? '—'}
                    </span>
                  </td>
                  <td className="num">{int(c.orders)}</td>
                  <td className="num">{money(c.sales)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </ChartCard>
        <ChartCard title="International Markets" subtitle="Top countries outside the UK">
          <HBars
            data={countries.filter((c) => c.name !== 'United Kingdom').slice(0, 8).map((c) => ({ label: c.name, value: c.sales }))}
            color="var(--c-blue)"
          />
        </ChartCard>
      </div>
    </div>
  )
}

/* Orders tooltip needs integer formatting; wrap so hooks/naming stay tidy. */
const makeTooltipOrders = { Component: makeTooltip((v) => int(v)) }
