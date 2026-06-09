"""Archivist API — Pagination patterns for iterating large collections."""

import os
from typing import Generator
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY}


def paginate(endpoint: str, params: dict = None, page_size: int = 50) -> Generator[dict, None, None]:
    """
    Iterate through all pages of a paginated endpoint.

    Yields individual items from each page.

    Note: GET /v1/entities uses a different envelope (results/hasMore/limit).
    Use paginate_entities() for that endpoint.
    """
    params = dict(params or {})
    params["size"] = page_size
    page = 1

    while True:
        params["page"] = page
        resp = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()

        for item in data["data"]:
            yield item

        if page >= data["pages"]:
            break
        page += 1


def get_all_characters(campaign_id: str) -> list[dict]:
    """Fetch every character in a campaign across all pages."""
    characters = list(paginate("/v1/characters", params={"campaign_id": campaign_id}))
    return characters


def get_all_moments(campaign_id: str) -> list[dict]:
    """Fetch every moment in a campaign across all pages."""
    moments = list(paginate("/v1/moments", params={"campaign_id": campaign_id}))
    return moments


def paginate_entities(campaign_id: str, entity_type: str, page_size: int = 50) -> Generator[dict, None, None]:
    """Iterate GET /v1/entities (uses limit and results/hasMore envelope)."""
    page = 1
    while True:
        resp = requests.get(
            f"{BASE_URL}/v1/entities",
            headers=HEADERS,
            params={"campaign_id": campaign_id, "type": entity_type, "page": page, "limit": page_size},
        )
        resp.raise_for_status()
        data = resp.json()
        for item in data["results"]:
            yield item
        if not data["hasMore"]:
            break
        page += 1


def get_all_journals(campaign_id: str) -> list[dict]:
    """Fetch every journal entry in a campaign across all pages."""
    return list(paginate("/v1/journals", params={"campaign_id": campaign_id}))


if __name__ == "__main__":
    campaign_id = os.environ.get("ARCHIVIST_CAMPAIGN_ID")
    if not campaign_id:
        resp = requests.get(f"{BASE_URL}/v1/campaigns", headers=HEADERS, params={"size": 1})
        resp.raise_for_status()
        campaigns = resp.json()["data"]
        if not campaigns:
            print("No campaigns found")
            exit(1)
        campaign_id = campaigns[0]["id"]

    print(f"Fetching all characters for campaign {campaign_id}...")
    characters = get_all_characters(campaign_id)
    print(f"  Total: {len(characters)} characters")

    for char in characters[:5]:
        print(f"    [{char['type']}] {char['character_name']}")
    if len(characters) > 5:
        print(f"    ... and {len(characters) - 5} more")

    print(f"\nFetching all moments for campaign {campaign_id}...")
    moments = get_all_moments(campaign_id)
    print(f"  Total: {len(moments)} moments")
