"""Archivist API — Unified compendium entity picker."""

import os
from typing import Generator
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY}

ENTITY_TYPES = ("characters", "factions", "locations", "items")


def paginate_entities(
    campaign_id: str,
    entity_type: str,
    search: str | None = None,
    limit: int = 50,
) -> Generator[dict, None, None]:
    """Iterate all pages of GET /v1/entities (uses limit, not size)."""
    if entity_type not in ENTITY_TYPES:
        raise ValueError(f"type must be one of {ENTITY_TYPES}")

    page = 1
    while True:
        params = {
            "campaign_id": campaign_id,
            "type": entity_type,
            "page": page,
            "limit": limit,
        }
        if search:
            params["search"] = search

        resp = requests.get(f"{BASE_URL}/v1/entities", headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()

        for item in data["results"]:
            yield item

        if not data["hasMore"]:
            break
        page += 1


def search_characters(campaign_id: str, query: str):
    """Search characters by name using the entities endpoint."""
    results = list(
        paginate_entities(campaign_id, "characters", search=query, limit=20)
    )
    print(f"Characters matching '{query}' ({len(results)}):\n")
    for item in results:
        print(f"  [{item.get('type', 'PC')}] {item['name']} ({item['id']})")
    return results


if __name__ == "__main__":
    campaign_id = os.environ.get("ARCHIVIST_CAMPAIGN_ID")
    if not campaign_id:
        print("Set ARCHIVIST_CAMPAIGN_ID to run this example")
        exit(1)
    search_characters(campaign_id, os.environ.get("ARCHIVIST_SEARCH", ""))
