# Technical Project 02 — FRED Key Indicators Dashboard

**Stack:** Python · Pandas · Streamlit · Plotly · FRED API
**Skill demonstrated:** External API integration → live economic data → interactive UI

---

## What This Is

A Streamlit dashboard that pulls real-world economic data from **FRED (Federal Reserve Economic Data)** — the same underlying data source used in Lesson 8's Figma-to-code exercise, rebuilt here in Python/Streamlit to stay consistent with [Project 01](../01-ecommerce-analytics-dashboard/).

| File | What it does |
|------|----------------|
| [`fred_client.py`](fred_client.py) | Fetches series from the live FRED API when a key is configured; falls back to clearly labeled synthetic demo data otherwise |
| [`fred-dashboard.py`](fred-dashboard.py) | Streamlit UI — KPI cards and trend charts for each indicator |

## What It Tracks

Four key indicators, pulled by FRED series ID:

| Indicator | FRED Series ID |
|-----------|-----------------|
| Real GDP | `GDPC1` |
| Unemployment Rate | `UNRATE` |
| CPI (Inflation) | `CPIAUCSL` |
| Federal Funds Rate | `FEDFUNDS` |

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

The demo-mode path (synthetic data, UI, charts) has been run end-to-end and verified working. The live-mode FRED integration is written against the documented `fredapi` client but has not been exercised against a real API key — I don't hold one, and generating one requires signing up with a personal account, which isn't something to do on someone else's behalf. Add your key and give it a run; if the live path needs a fix, that's a quick follow-up.

## Attribution

Inspired by Lesson 8 of DeepLearning.AI's short course *"Claude Code: A Highly Agentic Coding Assistant"* (built in partnership with Anthropic), which builds a Next.js + Recharts dashboard from a Figma mockup and wires it up to FRED data. That lesson's source repo has no pre-built app to copy — it's a live "build it with Claude Code" exercise using a Figma design file. This is an original Python/Streamlit build of the same concept (real-world economic data → interactive dashboard), not a port of any course code.

---

→ [See all technical projects](../README.md)
→ [Book a discovery call](https://tinyurl.com/maxxam-call)
