# Technical Project 02 — FRED Key Indicators Dashboard

**Stack:** Python · Pandas · Streamlit · Plotly · FRED API
**Skill demonstrated:** External API integration → live economic data → interactive UI

---

## What This Is

A Streamlit dashboard that pulls real-world economic data from **FRED (Federal Reserve Economic Data)** — the same underlying data source used in Lesson 8's Figma-to-code exercise, rebuilt here in Python/Streamlit to stay consistent with [Project 01](../01-ecommerce-analytics-dashboard/). Indicators are organized by category in a left sidebar (Key Indicators overview, Inflation, Employment, Interest Rates, Economic Growth, Exchange Rates, Housing, Consumer Spending), matching the layout of the lesson's reference app. Includes a dark mode toggle, same pattern as Project 01.

| File | What it does |
|------|----------------|
| [`fred_client.py`](fred_client.py) | Fetches series from the live FRED API when a key is configured; falls back to clearly labeled synthetic demo data otherwise |
| [`fred-dashboard.py`](fred-dashboard.py) | Streamlit UI — sidebar category navigation, KPI cards, trend charts, dark mode toggle |

## What It Tracks

Nine indicators across seven categories, pulled by FRED series ID:

| Category | Indicator | FRED Series ID |
|----------|-----------|-----------------|
| Economic Growth | Real GDP | `GDPC1` |
| Employment | Unemployment Rate | `UNRATE` |
| Inflation | CPI | `CPIAUCSL` |
| Interest Rates | Federal Funds Rate | `FEDFUNDS` |
| Interest Rates | 10-Year Treasury Yield | `DGS10` |
| Interest Rates | 3-Month Treasury Rate | `TB3MS` |
| Housing | Housing Starts | `HOUST` |
| Exchange Rates | Trade-Weighted Dollar Index | `DTWEXBGS` |
| Consumer Spending | Personal Consumption Expenditures | `PCE` |

The "Key Indicators" overview shows one representative series per category; selecting a category in the sidebar shows all of that category's series in more detail.

## Running It

```bash
pip install -r requirements.txt
streamlit run fred-dashboard.py
```

### Connecting real FRED data

The dashboard runs immediately with synthetic demo data (clearly labeled on-screen) — no setup required. To pull live data:

1. Get a free API key: https://fred.stlouisfed.org/docs/api/api_key.html
2. Copy `.env.example` to `.env`
3. Paste your key into `.env` as `FRED_API_KEY=...`
4. Restart the dashboard — it detects the key automatically and switches out of demo mode

`.env` is gitignored repo-wide, so your key never gets committed.

## Note on Testing

Both modes have been run end-to-end and verified: demo mode (synthetic data, UI, charts, sidebar navigation, dark mode) and live mode (real FRED API responses across all nine series, confirmed against a real key).

## Attribution

Inspired by Lesson 8 of DeepLearning.AI's short course *"Claude Code: A Highly Agentic Coding Assistant"* (built in partnership with Anthropic), which builds a Next.js + Recharts dashboard from a Figma mockup and wires it up to FRED data. That lesson's source repo has no pre-built app to copy — it's a live "build it with Claude Code" exercise using a Figma design file. This is an original Python/Streamlit build of the same concept (real-world economic data → interactive dashboard), not a port of any course code.

---

→ [See all technical projects](../README.md)
→ [Book a discovery call](https://tinyurl.com/maxxam-call)
