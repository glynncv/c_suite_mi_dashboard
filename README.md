# C‑suite MI Dashboard (ServiceNow)

## 1) Setup
- Install **uv**: https://docs.astral.sh/uv/
- `uv sync --all-extras --dev`
- Copy `.env.example` → `.env` and fill SNOW_* values.

## 2) Run (CSV demo)
- Put a CSV at `data/sample_incidents.csv` with columns:
  `number,priority,opened_at,resolved_at,closed_at,location,u_major_incident,...`
- `uv run streamlit run app/main.py`

## 3) Run (ServiceNow API)
- Ensure `.env` has `SNOW_INSTANCE`, `SNOW_USERNAME`, `SNOW_PASSWORD`, `SNOW_QUERY`.
- In the app sidebar, choose **ServiceNow API**.

## 4) Tests & quality
- `uv run ruff check .`
- `uv run mypy src`
- `uv run pytest -q --cov=src`

## 5) Deploy
- **Streamlit Cloud**: push to GitHub, set env vars, deploy.
- **Docker**: `docker build -t mi-dashboard . && docker run -p 8501:8501 --env-file=.env mi-dashboard`

## Notes
- KPI definitions live in `src/kpis.py`. Adjust formulas (e.g., pause windows) to match policy.
- For enterprise rollouts, move aggregates to Postgres/Snowflake and add SSO.
