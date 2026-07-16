# RetailIQ Dashboard Webapp

React + TypeScript + Vite + Recharts dashboard over the SmartRetail analytics
pipeline. All figures are real, precomputed by `src/m10_webapp_export.py` into
`src/data/dashboard.json` (~180 KB) — the app ships aggregates, not the 1M-row
fact table.

## Run it

```powershell
cd webapp
npm install        # first time only
npm run dev        # http://localhost:5173
```

## Build for production

```powershell
npm run build      # outputs to dist/ (deploy anywhere static)
npm run preview    # serve the production build locally
```

## Pages

Executive · Sales · Customers · Products · Profit · Inventory · Forecast · About

## Refresh the data

Re-run the pipeline, then:

```powershell
cd ../src
py m10_webapp_export.py
```

The dev server hot-reloads the new JSON automatically.

## Notes

- Light/dark theme: toggle in the top bar (persisted), or force with
  `?theme=light` / `?theme=dark` in the URL.
- Routing is hash-based (`/#/sales`) so the build works from any static host
  or even the local file system.
