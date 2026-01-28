import logging
from typing import List
import requests
from . import config


def fetch_page(page: int) -> List[dict]:
    """
    Fetch a single page of internships from the API.
    Requires API_BASE_URL set in the .env file. Returns [] on error.
    """
    if not config.API_BASE_URL:
        logging.warning("API_BASE_URL not set; returning no results.")
        return []

    params = {
        "page": page,
        "per_page": config.API_PER_PAGE,
        "hours_lookback": config.HOURS_LOOKBACK,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        resp = requests.get(config.API_BASE_URL, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            # Handle nested data.data structure from Unstop API
            raw_data = data.get("data")
            if isinstance(raw_data, dict) and "data" in raw_data:
                items = raw_data["data"]
            else:
                items = raw_data or data.get("items") or data.get("results") or []
        elif isinstance(data, list):
            items = data
        else:
            items = []
        return items
    except Exception as e:
        logging.error(f"API request failed: {e}")
        return []
