from __future__ import annotations
import os
import time
from typing import Iterator, Dict, Any, List
import requests
from dotenv import load_dotenv

load_dotenv()

SNOW_BASE = f"https://{os.getenv('SNOW_INSTANCE')}.service-now.com/api/now/table"
TABLE = os.getenv("SNOW_TABLE", "incident")

# Authentication configuration
SNOW_USERNAME = os.getenv("SNOW_USERNAME", "")
SNOW_PASSWORD = os.getenv("SNOW_PASSWORD", "")
SNOW_CLIENT_ID = os.getenv("SNOW_CLIENT_ID", "")
SNOW_CLIENT_SECRET = os.getenv("SNOW_CLIENT_SECRET", "")

DEFAULT_FIELDS = [
    "number","priority","opened_at","u_resolved","closed_at","category",
    "short_description","impact","urgency","location","incident_state"
]

# Default query for high priority incidents (using IN operator which works in this ServiceNow instance)
DEFAULT_QUERY = "priorityIN1,2"

def _get_auth_headers() -> Dict[str, str]:
    """Get authentication headers based on available credentials"""
    headers = {"Accept": "application/json"}
    
    # If OAuth credentials are available, use them
    if SNOW_CLIENT_ID and SNOW_CLIENT_SECRET:
        # For OAuth, we'll need to get a token first
        # This is a simplified version - you may need to implement full OAuth flow
        headers["Authorization"] = f"Bearer {_get_oauth_token()}"
    elif SNOW_USERNAME and SNOW_PASSWORD:
        # Basic auth - credentials will be passed to requests.get()
        pass
    else:
        raise ValueError("No authentication credentials provided. Set either SNOW_USERNAME/SNOW_PASSWORD or SNOW_CLIENT_ID/SNOW_CLIENT_SECRET")
    
    return headers

def _get_oauth_token() -> str:
    """Get OAuth token from ServiceNow (simplified implementation)"""
    # This is a placeholder - you'll need to implement the full OAuth flow
    # For now, return empty string to fall back to basic auth
    return ""

def fetch_incidents(query: str, fields: List[str] | None = None, page_size: int = 500) -> List[Dict[str, Any]]:
    """Pull incidents matching an encoded query (sysparm_query).
    Supports both Basic Auth and OAuth 2.0."""
    fields = fields or DEFAULT_FIELDS
    offset = 0
    results: List[Dict[str, Any]] = []
    
    # Get authentication headers
    headers = _get_auth_headers()
    
    # Prepare authentication
    auth = None
    if SNOW_USERNAME and SNOW_PASSWORD:
        # Use basic auth if OAuth credentials are not properly configured
        if not (SNOW_CLIENT_ID and SNOW_CLIENT_SECRET and SNOW_CLIENT_ID != "your_client_id" and SNOW_CLIENT_SECRET != "your_client_secret"):
            auth = (SNOW_USERNAME, SNOW_PASSWORD)
    
    while True:
        params = {
            "sysparm_query": query,
            "sysparm_display_value": "false",
            "sysparm_exclude_reference_link": "true",
            "sysparm_fields": ",".join(fields),
            "sysparm_limit": str(page_size),
            "sysparm_offset": str(offset),
        }
        
        try:
            resp = requests.get(
                f"{SNOW_BASE}/{TABLE}", 
                headers=headers, 
                params=params, 
                auth=auth, 
                timeout=60
            )
            
            resp.raise_for_status()
            chunk = resp.json().get("result", [])
            
            results.extend(chunk)
            if len(chunk) < page_size:
                break
            offset += page_size
            time.sleep(0.2)  # polite rate limiting
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception(f"Authentication failed. Check your ServiceNow credentials and user permissions. Error: {e}")
            else:
                raise e
        except Exception as e:
            raise e
    
    return results
