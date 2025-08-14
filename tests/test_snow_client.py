import responses
import os
from src.snow_client import fetch_incidents

@responses.activate
def test_fetch_incidents_paginates():
    # Mock the environment variables for testing
    os.environ['SNOW_INSTANCE'] = 'test-instance'
    os.environ['SNOW_TABLE'] = 'incident'
    
    url = "https://test-instance.service-now.com/api/now/table/incident"
    # first page
    responses.add(responses.GET, url, json={"result":[{"number":"INC1"}]}, status=200)
    # second (empty) page
    responses.add(responses.GET, url, json={"result":[]}, status=200)
    out = fetch_incidents(query="priority=1")
    assert len(out) == 1 and out[0]["number"] == "INC1"
