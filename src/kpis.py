from __future__ import annotations
import pandas as pd

def mttr_hours(df: pd.DataFrame) -> float:
    """Mean time to resolve (hours) for major incidents only."""
    d = df[df["is_major"]].copy()
    d = d[(~d["opened_at"].isna()) & (~d["resolved_at"].isna())]
    if d.empty:
        return 0.0
    hours = (d["resolved_at"] - d["opened_at"]).dt.total_seconds() / 3600.0
    return float(hours.mean())

def weekly_counts(df: pd.DataFrame) -> pd.DataFrame:
    d = df[df["is_major"]].copy()
    d["week"] = d["opened_at"].dt.to_period("W").dt.start_time
    out = d.groupby("week", as_index=False).size()
    out.rename(columns={"size": "mi_count"}, inplace=True)
    return out.sort_values("week")

def p1_ratio(df: pd.DataFrame) -> float:
    d = df[df["is_major"]].copy()
    if d.empty:
        return 0.0
    p1 = (d["priority"] == 1).sum()
    return float(p1 / len(d))

def sites_impacted(df: pd.DataFrame, site_col: str = "location") -> int:
    if site_col not in df.columns:
        return 0
    d = df[df["is_major"] & df[site_col].notna()]
    return int(d[site_col].nunique())
