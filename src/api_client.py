"""
HTTP client for connecting to your backend API.

Configure BASE_URL and API_KEY via environment variables.
All tools in server.py call through this module.
"""

import os
import httpx

BASE_URL = os.environ.get("MY_API_URL", "https://api.example.com")
API_KEY = os.environ.get("MY_API_KEY", "")

_headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
_client = httpx.Client(base_url=BASE_URL, headers=_headers, timeout=15)


def api_get(path: str, params: dict | None = None) -> dict:
    """GET request to the backend API. Raises on HTTP errors."""
    resp = _client.get(path, params=params)
    resp.raise_for_status()
    return resp.json()


def api_post(path: str, data: dict | None = None) -> dict:
    """POST request to the backend API. Raises on HTTP errors."""
    resp = _client.post(path, json=data)
    resp.raise_for_status()
    return resp.json()
