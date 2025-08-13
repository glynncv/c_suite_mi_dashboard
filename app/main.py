import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from src import kpis
from src.transforms import to_dataframe
from src.snow_client import fetch_incidents

load_dotenv()

def main():
    st.set_page_config(page_title="C‑suite MI Dashboard", layout="wide")
    
    st.title("C‑suite Major Incidents Dashboard")
    
    data_src = st.sidebar.selectbox("Data source", ["CSV sample", "ServiceNow API"])
    year = st.sidebar.number_input("Year", min_value=2020, max_value=2100, value=2025, step=1)
    
    if data_src == "CSV sample":
        path = os.path.join("data", "sample_incidents.csv")
        if not os.path.exists(path):
            st.info("No sample CSV found. Upload one below.")
            uploaded = st.file_uploader("Upload ServiceNow CSV (incidents)", type=["csv"])
            if uploaded:
                df = pd.read_csv(uploaded)
            else:
                st.stop()
        else:
            df = pd.read_csv(path)
            # Transform CSV data to match expected format
            df = transform_csv_data(df)
    else:
        # Use environment variable with proper fallback
        query = os.getenv("SNOW_QUERY", "")
        
        if not query:
            # Fallback to the working query format that matches your successful curl test
            query = "priorityIN1,2"
            st.info("SNOW_QUERY not set in environment; using fallback query: priorityIN1,2")
        else:
            st.info(f"Using SNOW_QUERY from environment: {query}")
        
        try:
            records = fetch_incidents(query=query)
            st.info(f"Raw records from ServiceNow: {len(records)} records")
            
            if records:
                st.info(f"First record keys: {list(records[0].keys()) if records else 'No records'}")
                st.info(f"Sample record: {records[0] if records else 'No records'}")
            
            df = to_dataframe(records)
            st.success(f"Fetched {len(df)} incidents from ServiceNow")
            
            # Debug: Show what columns we actually have
            st.info(f"Available columns: {list(df.columns)}")
            st.info(f"DataFrame shape: {df.shape}")
            
            # Ensure required columns exist
            if 'opened_at' not in df.columns:
                st.error("Missing 'opened_at' column after transformation")
                st.info("Original columns from ServiceNow: " + str(list(records[0].keys()) if records else "No records"))
                st.stop()
                
        except Exception as e:
            st.error(f"Failed to fetch from ServiceNow: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
            st.info("Falling back to CSV upload.")
            uploaded = st.file_uploader("Upload ServiceNow CSV (incidents)", type=["csv"])
            if not uploaded:
                st.stop()
            df = pd.read_csv(uploaded)
            df = transform_csv_data(df)
    
    # Normalise types if CSV path
    if "opened_at" in df.columns and not pd.api.types.is_datetime64_any_dtype(df["opened_at"]):
        for c in ["opened_at","resolved_at","closed_at"]:
            if c in df.columns:
                df[c] = pd.to_datetime(df[c], errors="coerce", utc=True)
    
    # Final safety check - ensure we have required columns
    required_columns = ["opened_at", "is_major"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Missing required columns: {missing_columns}")
        st.info(f"Available columns: {list(df.columns)}")
        st.stop()
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("MTTR (hrs)", f"{kpis.mttr_hours(df):.1f}")
    wk = kpis.weekly_counts(df)
    col2.metric("MIs (YTD)", int(df[df.get("is_major", True)].shape[0]))
    col3.metric("P1 ratio", f"{kpis.p1_ratio(df)*100:.0f}%")
    col4.metric("Sites impacted", kpis.sites_impacted(df))
    
    st.line_chart(wk.set_index("week")["mi_count"], height=280)
    st.subheader("Incident details")
    st.dataframe(df.head(500))

def transform_csv_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform CSV data to match expected column names and format"""
    # Rename columns to match expected format
    column_mapping = {
        'created_date': 'opened_at',
        'resolved_date': 'resolved_at',
        'u_resolved': 'resolved_at',
        'sites_impacted': 'location',
        'incident_number': 'number'
    }
    
    # Rename columns
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns:
            df = df.rename(columns={old_col: new_col})
    
    # Convert priority to numeric and determine if major incident
    if 'priority' in df.columns:
        # Handle both string and numeric priority values
        if df['priority'].dtype == 'object':
            df['priority'] = df['priority'].str.replace('P', '').astype(int)
        # Consider P1 and P2 as major incidents
        df['is_major'] = df['priority'].isin([1, 2])
    
    # Convert datetime columns - handle ServiceNow format
    for col in ['opened_at', 'resolved_at', 'closed_at']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    
    return df

if __name__ == "__main__":
    main()
