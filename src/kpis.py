from __future__ import annotations

import pandas as pd


def mttr_hours(df: pd.DataFrame) -> float:
    """Mean time to resolve (hours) for major incidents only."""
    major_incidents = df[df["is_major"]]
    valid_incidents = major_incidents[(~major_incidents["opened_at"].isna()) & (~major_incidents["resolved_at"].isna())]
    if valid_incidents.empty:
        return 0.0
    hours = (valid_incidents["resolved_at"] - valid_incidents["opened_at"]).dt.total_seconds() / 3600.0
    return float(hours.mean())

def weekly_counts(df: pd.DataFrame) -> pd.DataFrame:
    major_incidents = df[df["is_major"]]
    major_incidents_with_week = major_incidents.assign(week=major_incidents["opened_at"].dt.to_period("W").dt.start_time)
    out = major_incidents_with_week.groupby("week", as_index=False).size()
    out.rename(columns={"size": "mi_count"}, inplace=True)
    return out.sort_values("week")

def p1_ratio(df: pd.DataFrame) -> float:
    major_incidents = df[df["is_major"]]
    if major_incidents.empty:
        return 0.0
    p1_count = (major_incidents["priority"] == 1).sum()
    return float(p1_count / len(major_incidents))

def sites_impacted(df: pd.DataFrame, site_col: str = "location") -> int:
    if site_col not in df.columns:
        return 0
    d = df[df["is_major"] & df[site_col].notna()]
    return int(d[site_col].nunique())
