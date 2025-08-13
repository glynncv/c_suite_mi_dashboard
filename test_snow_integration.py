#!/usr/bin/env python3
"""
Test script to verify ServiceNow integration with actual API response format.
Run this to test if your ServiceNow client can properly fetch and transform data.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from snow_client import fetch_incidents
from transforms import to_dataframe
from kpis import mttr_hours, weekly_counts, p1_ratio, sites_impacted

def test_snow_integration():
    """Test the complete ServiceNow integration pipeline"""
    print("Testing ServiceNow integration...")
    
    # Test query for high priority incidents this year
    query = "priorityIN1,2^opened_atONThis%20year@javascript:gs.beginningOfThisYear()@javascript:gs.endOfThisYear()^u_resolvedISNOTEMPTY"
    
    try:
        print(f"Fetching incidents with query: {query}")
        records = fetch_incidents(query=query, page_size=10)  # Limit to 10 for testing
        
        if not records:
            print("No records returned from ServiceNow")
            return False
            
        print(f"Successfully fetched {len(records)} incidents")
        print(f"Sample record: {records[0]}")
        
        # Transform to DataFrame
        print("\nTransforming data...")
        df = to_dataframe(records)
        print(f"DataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Data types:\n{df.dtypes}")
        
        # Test KPIs
        print("\nTesting KPIs...")
        print(f"MTTR (hours): {mttr_hours(df):.1f}")
        print(f"P1 ratio: {p1_ratio(df)*100:.0f}%")
        print(f"Sites impacted: {sites_impacted(df)}")
        
        # Show weekly counts
        weekly = weekly_counts(df)
        print(f"Weekly counts shape: {weekly.shape}")
        
        print("\n✅ ServiceNow integration test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ ServiceNow integration test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    load_dotenv()
    success = test_snow_integration()
    sys.exit(0 if success else 1)
