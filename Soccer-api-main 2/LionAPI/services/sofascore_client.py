import os

import requests


DEFAULT_HEADERS = {
    "User-Agent": os.getenv(
        "SOFASCORE_USER_AGENT",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.sofascore.com/",
    "Origin": "https://www.sofascore.com",
}


def fetch_json(url: str, timeout: int = 20):
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

    if response.status_code == 403:
        raise RuntimeError(
            "SofaScore rejected the request with HTTP 403. "
            "The public API appears to be protected against server-side clients."
        )

    response.raise_for_status()
    return response.json()
