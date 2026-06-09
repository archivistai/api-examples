"""Archivist API — Moment list filters and card fieldsets."""

import os
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY}


def list_moments(
    campaign_id: str,
    *,
    search: str | None = None,
    character_ids: list[str] | None = None,
    session_ids: list[str] | None = None,
    fields: str | None = None,
    page: int = 1,
    size: int = 20,
):
    """List moments with optional entity/session filters and fields=card."""
    params: dict = {"campaign_id": campaign_id, "page": page, "size": size}
    if search:
        params["search"] = search
    if character_ids:
        params["character_ids"] = ",".join(character_ids)
    if session_ids:
        params["session_ids"] = ",".join(session_ids)
    if fields:
        params["fields"] = fields

    resp = requests.get(f"{BASE_URL}/v1/moments", headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()

    print(f"Moments ({data['total']} total, page {data['page']}/{data['pages']}):\n")
    for moment in data["data"]:
        if fields == "card":
            print(f"  {moment.get('label', '(untitled)')} — session {moment.get('session_id')}")
        else:
            print(f"  {moment.get('label', '(untitled)')}")
    return data


if __name__ == "__main__":
    campaign_id = os.environ.get("ARCHIVIST_CAMPAIGN_ID")
    if not campaign_id:
        print("Set ARCHIVIST_CAMPAIGN_ID to run this example")
        exit(1)

    list_moments(campaign_id, fields="card", size=5)
