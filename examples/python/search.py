"""Archivist API — unified campaign search."""

import os
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY}


def search_campaign(campaign_id: str, q: str, types: str | None = None):
    """Search a campaign. Omit types to query every bucket (max 10 hits each)."""
    params = {"q": q}
    if types:
        params["types"] = types

    resp = requests.get(
        f"{BASE_URL}/v1/campaigns/{campaign_id}/search",
        headers=HEADERS,
        params=params,
    )
    resp.raise_for_status()
    return resp.json()


def print_hits(data: dict) -> None:
    for bucket, hits in data.items():
        if not hits:
            continue
        print(f"{bucket} ({len(hits)})")
        for hit in hits:
            label = (
                hit.get("characterName")
                or hit.get("questName")
                or hit.get("name")
                or hit.get("title")
                or hit.get("id")
            )
            print(f"  - {label} ({hit.get('id')})")


if __name__ == "__main__":
    campaign_id = os.environ.get("ARCHIVIST_CAMPAIGN_ID")
    if not campaign_id:
        print("Set ARCHIVIST_CAMPAIGN_ID to run this example")
        raise SystemExit(1)

    query = os.environ.get("ARCHIVIST_SEARCH_Q", "the")
    print(f"Searching {campaign_id!r} for {query!r}\n")
    print_hits(search_campaign(campaign_id, query))
