from __future__ import annotations

import pandas as pd

RENAME_MAP = {
    "u_major_incident": "is_major",
    "opened_at": "opened_at",
    "u_resolved": "resolved_at",
    "closed_at": "closed_at",
    "location": "location",
}


def to_dataframe(records: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame.from_records(records)

    # normalise columns - only rename if the source column exists
    for k, v in RENAME_MAP.items():
        if k in df.columns:
            if k != v:  # Only rename if different
                df[v] = df[k]

    # Ensure opened_at exists (it should be there from ServiceNow)
    if 'opened_at' not in df.columns:
        # Try to find alternative column names
        for col in df.columns:
            if 'open' in col.lower() or 'created' in col.lower():
                df['opened_at'] = df[col]
                break

    # types - handle ServiceNow date format "YYYY-MM-DD HH:MM:SS"
    for col in ["opened_at","resolved_at","closed_at"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%Y-%m-%d %H:%M:%S", errors="coerce", utc=True)

    for col in ["priority","impact","urgency","severity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "is_major" in df.columns:
        df["is_major"] = df["is_major"].astype(str).str.lower().isin(["true","1","yes","y"])
    elif "priority" in df.columns:
        # Fallback heuristic: priority 1/2 often aligns with MI—tune for your process
        df["is_major"] = df["priority"].isin([1, 2])
    else:
        # If neither column exists, set all incidents as non-major
        df["is_major"] = False

    return df
