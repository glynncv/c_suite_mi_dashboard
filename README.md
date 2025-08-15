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

# Project Structure

## Data Organization
- **`data/`** — Production data folder (gitignored)
  - Add your ServiceNow exports here for local development
  - Files are not committed to git for security
  - Use `.env` file for configuration

- **`tests/data/`** — Test data folder (committed to git)
  - `test_incidents.csv` — Sample data for unit tests
  - `sample_incidents.csv` — Sample data for integration tests
  - These files are committed to git for CI/CD compatibility

## Test Data
Test data is automatically available for all developers and CI/CD pipelines. Production data should be placed in the `data/` folder and will be ignored by git.
