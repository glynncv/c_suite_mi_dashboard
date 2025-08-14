from __future__ import annotations
import os
import time
from typing import Dict, Any, List
import requests

# Only load environment variables when actually needed
def _load_env():
    """Load environment variables only when needed"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # dotenv not available, use system env vars

def _get_snow_base():
    """Get ServiceNow base URL - only called when needed"""
    _load_env()  # Load env vars when needed
    instance = os.getenv('SNOW_INSTANCE')
    if not instance:
        raise ValueError("SNOW_INSTANCE environment variable not set")
    return f"https://{instance}.service-now.com/api/now/table"

def _get_table():
    """Get ServiceNow table name - only called when needed"""
    _load_env()  # Load env vars when needed
    return os.getenv("SNOW_TABLE", "incident")

def _get_credentials():
    """Get authentication credentials - only called when needed"""
    _load_env()  # Load env vars when needed
    return {
        "username": os.getenv("SNOW_USERNAME", ""),
        "password": os.getenv("SNOW_PASSWORD", ""),
        "client_id": os.getenv("SNOW_CLIENT_ID", ""),
        "client_secret": os.getenv("SNOW_CLIENT_SECRET", "")
    }

DEFAULT_FIELDS = [
    "number", "priority", "opened_at", "u_resolved", "closed_at", "category",
    "short_description", "impact", "urgency", "location", "incident_state"
]

# Default query for MI by priority (P1/P2)
DEFAULT_QUERY = "priorityIN1,2"

def _get_oauth_token() -> str:
    """Placeholder for OAuth token retrieval; return empty to fall back to Basic Auth."""
    return ""

def _get_auth_headers() -> Dict[str, str]:
    """Build headers; only attach Bearer if a non-empty token exists."""
    headers = {"Accept": "application/json"}
    creds = _get_credentials()
    if creds["client_id"] and creds["client_secret"]:
        token = _get_oauth_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
    elif not (creds["username"] and creds["password"]):
        raise ValueError("No authentication provided. Set SNOW_USERNAME/SNOW_PASSWORD or OAuth creds.")
    return headers

def fetch_incidents(query: str, fields: List[str] | None = None, page_size: int = 500) -> List[Dict[str, Any]]:
    """
    Fetch incidents using the ServiceNow Table API with paging and retry/backoff.
    Supports Basic Auth (default) and OAuth (if token provided).
    """
    fields = fields or DEFAULT_FIELDS
    offset = 0
    results: List[Dict[str, Any]] = []
    headers = _get_auth_headers()

    # Prefer Basic Auth unless you actually obtained a Bearer token
    creds = _get_credentials()
    auth = (creds["username"], creds["password"]) if (creds["username"] and creds["password"]) else None

    MAX_RETRIES = 5
    while True:
        params = {
            "sysparm_query": query,
            "sysparm_display_value": "false",
            "sysparm_exclude_reference_link": "true",
            "sysparm_fields": ",".join(fields),
            "sysparm_limit": str(page_size),
            "sysparm_offset": str(offset),
        }

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = requests.get(
                    f"{_get_snow_base()}/{_get_table()}",
                    headers=headers,
                    params=params,
                    auth=auth,
                    timeout=60,
                )
                # Backoff for rate limiting / transient server errors
                if resp.status_code in (429, 500, 502, 503, 504):
                    retry_after = resp.headers.get("Retry-After")
                    wait = int(retry_after) if (retry_after and retry_after.isdigit()) else min(60, 2 ** attempt)
                    time.sleep(wait)
                    if attempt < MAX_RETRIES:
                        continue
                resp.raise_for_status()

                chunk = resp.json().get("result", [])
                results.extend(chunk)
                if len(chunk) < page_size:
                    return results  # no more pages
                offset += page_size
                time.sleep(0.2)  # polite pacing
                break  # success -> next page
            except requests.exceptions.HTTPError as e:
                if e.response is not None and e.response.status_code == 401:
                    raise Exception("Authentication failed (401). Check SNOW creds/roles.") from e
                if attempt >= MAX_RETRIES:
                    raise
                time.sleep(min(60, 2 ** attempt))
            except requests.RequestException:
                if attempt >= MAX_RETRIES:
                    raise
                time.sleep(min(60, 2 ** attempt))
