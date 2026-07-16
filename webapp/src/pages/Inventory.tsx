import { Donut } from '../components/charts/Donut'
import { HBars } from '../components/charts/HBars'
import { ChartCard } from '../components/ui/ChartCard'
import { IconBox, IconTrend, IconWarehouse } from '../components/ui/Icons'
import { KpiCard } from '../components/ui/KpiCard'
import { data } from '../data/types'
import { int } from '../lib/format'
import { MOVEMENT_COLORS } from '../lib/palette'
import './pages.css'

const { inventory } = data

export function Inventory() {
  const fastCount = inventory.movement.find((m) => m.name === 'Fast')?.products ?? 0

  return (
    <div className="page grid" style={{ gap: 'var(--gap)' }}>
      <div className="grid kpi-row" style={{ gridTemplateColumns: 'repeat(4, minmax(0,1fr))' }}>
        <KpiCard label="Products Tracked" value={inventory.totalProducts} format={(v) => int(v)} tint="var(--accent)" icon={<IconBox />} />
        <KpiCard label="Fast Movers" value={fastCount} format={(v) => int(v)} tint="var(--c-teal)" icon={<IconTrend />} />
        <KpiCard label="Restock Candidates" value={inventory.restock.length} format={(v) => int(v)} tint="var(--c-orange)" icon={<IconWarehouse />} />
        <KpiCard label="Dead Stock (90+ days)" value={inventory.deadStock} format={(v) => int(v)} tint="var(--c-slate)" icon={<IconBox />} />
      </div>

      <div className="grid cols-2">
        <ChartCard title="Products by Movement Class" subtitle="Velocity quartiles + staleness rules">
          <Donut
            data={inventory.movement.map((m) => ({ name: m.name, value: m.products }))}
            colors={(name) => MOVEMENT_COLORS[name] ?? '#98a0b8'}
            centerValue={int(inventory.totalProducts)}
            centerLabel="products"
          />
        </ChartCard>
        <ChartCard title="Revenue by Movement Class" subtitle="Fast movers = 15% of products, ~54% of revenue">
          <HBars
            data={inventory.movement.map((m) => ({ label: m.name, value: m.revenue }))}
            color={(i) => Object.values(MOVEMENT_COLORS)[i]}
          />
        </ChartCard>
      </div>

      <div className="grid cols-2">
        <ChartCard title="Fastest Moving Products" subtitle="Units per active week">
          <HBars
            data={inventory.fastest.map((f) => ({ label: f.description, value: f.sales_velocity }))}
            color="var(--c-teal)"
            format={(v) => `${int(v)} u/wk`}
          />
        </ChartCard>

        <ChartCard title="Restock Recommendations" subtitle="Fast movers that sold within the last 14 days">
          <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Category</th>
                <th className="num">Velocity</th>
                <th className="num">Units sold</th>
              </tr>
            </thead>
            <tbody>
              {inventory.restock.map((r) => (
                <tr key={r.description}>
                  <td>{r.description}</td>
                  <td style={{ fontSize: 11 }}>{r.category}</td>
                  <td className="num">{int(r.sales_velocity)}/wk</td>
                  <td className="num">{int(r.units_sold)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        </ChartCard>
      </div>
    </div>
  )
}
