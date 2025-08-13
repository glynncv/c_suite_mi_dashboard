import pandas as pd
from datetime import datetime, timezone
from src import kpis

def _df():
    def ts(h): return datetime(2025, 5, 1, h, tzinfo=timezone.utc)
    return pd.DataFrame([
        {"is_major": True, "opened_at": ts(0),  "resolved_at": ts(5), "priority": 1, "location": "SiteA"},
        {"is_major": True, "opened_at": ts(2),  "resolved_at": ts(10), "priority": 2, "location": "SiteB"},
        {"is_major": False,"opened_at": ts(1),  "resolved_at": ts(3), "priority": 3, "location": "SiteA"},
    ])

def test_mttr_hours():
    assert abs(kpis.mttr_hours(_df()) - 6.5) < 1e-6

def test_weekly_counts_not_empty():
    wk = kpis.weekly_counts(_df())
    assert "mi_count" in wk.columns and wk["mi_count"].sum() == 2

def test_p1_ratio():
    assert kpis.p1_ratio(_df()) == 0.5

def test_sites_impacted():
    assert kpis.sites_impacted(_df()) == 2
