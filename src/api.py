import requests


class APIError(Exception):
    pass


class QueryLimitExceededError(APIError):
    pass


def create_session():
    return requests.Session()


def query_earthquakes(base_url, params, session=None):
    from urllib.parse import urlencode

    if session is None:
        session = create_session()

    url = f"{base_url}?{urlencode(params)}"

    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json() if params.get("format") == "geojson" else response.text
    except requests.exceptions.HTTPError as e:
        if (
            response.status_code == 400
            and "exceeds search limit of 20000" in response.text
        ):
            raise QueryLimitExceededError(f"Query limit exceeded: {response.text}")
        else:
            raise APIError(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        raise APIError(f"Request error: {e}")
