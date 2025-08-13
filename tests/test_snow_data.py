from src.snow_client import fetch_incidents

# Test different query syntaxes for multiple priority values
queries = [
    'priorityIN1,2',             # IN operator - most likely to work
    'priority=1^OR^priority=2',  # Standard ServiceNow OR
    'priority=1^priority=2',     # Alternative OR syntax
    'priority=1',                 # Individual priority 1
    'priority=2',                 # Individual priority 2
    '',  # No query - get all incidents
]

for query in queries:
    query_desc = f"'{query}'" if query else "all incidents"
    print(f"\nTesting query: {query_desc}")
    
    try:
        records = fetch_incidents(query=query)
        print(f"Fetched {len(records)} incidents")
        
        if records:
            print(f"First record keys: {list(records[0].keys())}")
            print(f"Sample record: {records[0]}")
            print(f"Priority values found: {list(set(r.get('priority', 'N/A') for r in records[:10]))}")
            if len(records) > 0:
                print(f"✅ SUCCESS: Query '{query}' works!")
                break  # Found working query, no need to test more
        else:
            print("No incidents found")
    except Exception as e:
        print(f"Error: {e}")
        continue  # Try next query even if this one fails
