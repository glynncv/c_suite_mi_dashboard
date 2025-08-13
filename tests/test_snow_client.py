import responses
from src.snow_client import fetch_incidents, SNOW_BASE, TABLE

@responses.activate
def test_fetch_incidents_paginates():
    url = f"{SNOW_BASE}/{TABLE}"
    # first page
    responses.add(responses.GET, url, json={"result":[{"number":"INC1"}]}, status=200)
    # second (empty) page
    responses.add(responses.GET, url, json={"result":[]}, status=200)
    out = fetch_incidents(query="priority=1")
    assert len(out) == 1 and out[0]["number"] == "INC1"
