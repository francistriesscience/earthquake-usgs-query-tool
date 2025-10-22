import requests
import sys


def create_session():
    return requests.Session()


def query_earthquakes(base_url, params, session=None):
    from urllib.parse import urlencode

    if session is None:
        session = create_session()

    url = f"{base_url}?{urlencode(params)}"
    print(f"Querying: {url}")

    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json() if params.get('format') == 'geojson' else response.text
    except requests.exceptions.RequestException as e:
        print(f"Error querying API: {e}")
        sys.exit(1)