import { ChartCard } from '../components/ui/ChartCard'
import { data } from '../data/types'
import { int, money, pct } from '../lib/format'
import './pages.css'

const { meta, stats, models, kpis } = data

const PIPELINE = [
  ['Data Cleaning', 'Duplicates, cancelled orders, fee rows, outliers removed; profit/discount/category derived'],
  ['EDA', 'Sales, profit, product, customer, region and discount analysis'],
  ['Statistics', 'Central tendency, dispersion, 95% confidence intervals'],
  ['Hypothesis Testing', 'T-test, ANOVA and chi-square on real business questions'],
  ['Regression', 'Monthly sales forecast (trend + seasonality)'],
  ['Classification', 'Profitable-order prediction with decision tree & logistic regression'],
  ['Clustering', 'K-Means customer segmentation on RFM features'],
  ['Inventory Analysis', 'Sales velocity, movement classes, restock recommendations'],
  ['Dashboards', 'Power BI star schema + this React dashboard'],
]

export function About() {
  return (
    <div className="page grid" style={{ gap: 'var(--gap)' }}>
      <div className="grid cols-2">
        <ChartCard title="The Project" subtitle="Smart Retail Store Analytics with Sales Forecasting & Customer Segmentation">
          <div style={{ fontSize: 12.5, color: 'var(--ink-2)', lineHeight: 1.7 }}>
            <p style={{ marginTop: 0 }}>
              <strong>{meta.dataset}</strong> — every number in this dashboard is computed from the
              real transaction log ({meta.window}) by a 10-module Python pipeline (pandas, NumPy,
              SciPy, scikit-learn), then served as precomputed aggregates.
            </p>
            <p>
              After cleaning, <strong>{int(kpis.total.records)}</strong> sales lines remain, worth{' '}
              <strong>{money(kpis.total.sales)}</strong> across{' '}
              <strong>{int(kpis.total.orders)}</strong> orders and{' '}
              <strong>{int(kpis.total.customers)}</strong> identified customers in{' '}
              <strong>{kpis.total.countries}</strong> countries.
            </p>
            <p style={{ marginBottom: 0 }}>
              <strong>Honest caveat:</strong> the raw data has no cost, discount, category or
              segment columns. Profit assumes cost = 70% of each product's median price; discount
              is inferred from price shortfalls; categories come from description keywords;
              segments from K-Means clustering. The methodology matters more than the absolute
              profit figures.
            </p>
          </div>
        </ChartCard>

        <ChartCard title="Pipeline" subtitle="src/m00 … m10 — one module per stage">
          <ol style={{ margin: 0, paddingLeft: 18, fontSize: 12.5, color: 'var(--ink-2)', lineHeight: 1.65 }}>
            {PIPELINE.map(([stage, detail]) => (
              <li key={stage} style={{ paddingBottom: 4 }}>
                <strong style={{ color: 'var(--ink)' }}>{stage}</strong> — {detail}
              </li>
            ))}
          </ol>
        </ChartCard>
      </div>

      <div className="metric-tiles">
        <div className="card metric-tile">
          <div className="big">{money(stats.meanOrder)}</div>
          <div className="small">Mean order value</div>
        </div>
        <div className="card metric-tile">
          <div className="big">{money(stats.medianOrder)}</div>
          <div className="small">Median order value</div>
        </div>
        <div className="card metric-tile">
          <div className="big">
            {money(stats.ci95[0])}–{money(stats.ci95[1])}
          </div>
          <div className="small">95% CI, avg order value</div>
        </div>
        <div className="card metric-tile">
          <div className="big">{pct(models.classification.tree.accuracy, 1)}</div>
          <div className="small">Decision-tree accuracy</div>
        </div>
        <div className="card metric-tile">
          <div className="big">{pct(models.forecast.mape)}</div>
          <div className="small">Forecast MAPE</div>
        </div>
      </div>

      <div className="grid cols-2">
        <ChartCard title="Hypothesis Tests" subtitle="All three reject H0 at α = 0.05">
          <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr><th>Test</th><th className="num">p-value</th><th>Conclusion</th></tr>
            </thead>
            <tbody>
              {models.hypothesis.map((h) => (
                <tr key={h.name}>
                  <td style={{ whiteSpace: 'nowrap' }}>{h.name}</td>
                  <td className="num">{h.pValue}</td>
                  <td>{h.verdict}</td>
                </tr>
              ))}
            </tbody>
          </table>
          </div>
        </ChartCard>

        <ChartCard title="Machine Learning Summary">
          <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr><th>Task</th><th>Algorithm</th><th className="num">Score</th></tr>
            </thead>
            <tbody>
              <tr>
                <td>Sales forecasting</td>
                <td>Linear Regression</td>
                <td className="num">{pct(models.forecast.mape)} MAPE</td>
              </tr>
              <tr>
                <td>Profitability classification</td>
                <td>Decision Tree</td>
                <td className="num">{pct(models.classification.tree.accuracy, 1)} acc · {models.classification.tree.f1.toFixed(3)} F1</td>
              </tr>
              <tr>
                <td>Profitability classification</td>
                <td>Logistic Regression</td>
                <td className="num">{pct(models.classification.logistic.accuracy, 1)} acc · {models.classification.logistic.f1.toFixed(3)} F1</td>
              </tr>
              <tr>
                <td>Customer segmentation</td>
                <td>K-Means (k=4, RFM)</td>
                <td className="num">4 segments</td>
              </tr>
            </tbody>
          </table>
          </div>
          <div className="card-sub" style={{ marginTop: 10 }}>
            Stack: Python · pandas · scikit-learn · SciPy · Power BI · React + Recharts. Generated{' '}
            {meta.generated}.
          </div>
        </ChartCard>
      </div>
    </div>
  )
}
