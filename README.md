# C‑suite Major Incidents Dashboard (ServiceNow)

## Quick Start
1) Install deps: `uv sync --dev`
2) Copy `.env.example` → `.env` and set SNOW_* values
3) Run: `uv run streamlit run app/main.py`
4) In the app sidebar: pick **CSV** (upload) or **ServiceNow API**

## Tests
- Offline unit tests: `uv run pytest -q`
- Live SNOW test (requires .env): `uv run pytest -q -m integration`

## Notes
- MI definition = **P1 or P2** (priority parsing handles "2 - High" strings)
- MTTR = `resolved_at - opened_at`

# Data folder

- **test_incidents.csv** — Local-only ServiceNow export for testing the CSV path in the dashboard.
- Not committed to git; add your own export here for local dev.
