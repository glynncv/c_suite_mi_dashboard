import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_snow_connection():
    """Test ServiceNow connection with detailed diagnostics"""
    
    # Get credentials from environment or use defaults
    SNOW_INSTANCE = os.getenv("SNOW_INSTANCE", "phinia")
    SNOW_USERNAME = os.getenv("SNOW_USERNAME", "REST_API_DEFAULT")
    SNOW_PASSWORD = os.getenv("SNOW_PASSWORD", "EEL&9+5eXY")
    
    print(f"Testing connection to: {SNOW_INSTANCE}.service-now.com")
    print(f"Username: {SNOW_USERNAME}")
    print(f"Password: {'*' * len(SNOW_PASSWORD) if SNOW_PASSWORD else 'NOT SET'}")
    print("-" * 50)
    
    # Test 1: Simple query (like the working test)
    print("Test 1: Simple query (working)")
    url = f"https://{SNOW_INSTANCE}.service-now.com/api/now/table/incident"
    params = {
        "sysparm_limit": 1,
        "sysparm_query": "priorityIN1,2",
        "sysparm_display_value": "false",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "number,priority,opened_at"
    }
    
    try:
        resp = requests.get(url, auth=(SNOW_USERNAME, SNOW_PASSWORD), params=params, timeout=30)
        print(f"Simple query Status: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ SUCCESS: Simple query working!")
        else:
            print(f"❌ Simple query failed: {resp.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"❌ Simple query failed: {e}")
    
    print()
    
    # Test 2: Full query (like the main function)
    print("Test 2: Full query (like main function)")
    full_params = {
        "sysparm_query": "priority=1^OR^priority=2",
        "sysparm_display_value": "false",
        "sysparm_exclude_reference_link": "true",
        "sysparm_fields": "number,sys_id,priority,severity,state,opened_at,resolved_at,closed_at,category,subcategory,cmdb_ci,assignment_group,location,business_service,short_description,u_major_incident,impact,urgency",
        "sysparm_limit": "500",
        "sysparm_offset": "0"
    }
    
    try:
        resp = requests.get(url, auth=(SNOW_USERNAME, SNOW_PASSWORD), params=full_params, timeout=30)
        print(f"Full query Status: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ SUCCESS: Full query working!")
            data = resp.json()
            print(f"Fetched {len(data.get('result', []))} incidents")
        else:
            print(f"❌ Full query failed: {resp.text[:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"❌ Full query failed: {e}")
    
    return resp.status_code == 200

def test_simple_endpoint():
    """Test a simple endpoint that might not require authentication"""
    SNOW_INSTANCE = os.getenv("SNOW_INSTANCE", "phinia")
    
    print("\n" + "="*50)
    print("Test 3: Simple endpoint (no auth)")
    print("="*50)
    
    # Try to access the base URL
    base_url = f"https://{SNOW_INSTANCE}.service-now.com"
    
    try:
        resp = requests.get(base_url, timeout=30)
        print(f"Base URL Status: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ ServiceNow instance is reachable")
        else:
            print(f"⚠️  ServiceNow instance responded with status {resp.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot reach ServiceNow instance: {e}")

if __name__ == "__main__":
    print("ServiceNow Connection Test")
    print("=" * 50)
    
    # Test basic connectivity first
    test_simple_endpoint()
    
    # Test authenticated endpoints
    success = test_snow_connection()
    
    if success:
        print("\n🎉 All tests passed! ServiceNow API is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
