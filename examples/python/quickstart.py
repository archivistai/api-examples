"""Archivist API Quickstart — list campaigns, characters, and sessions."""

import os
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY}


def list_campaigns():
    """List all campaigns accessible to the authenticated user."""
    resp = requests.get(f"{BASE_URL}/v1/campaigns", headers=HEADERS, params={"size": 5})
    resp.raise_for_status()
    data = resp.json()

    print(f"Found {data['total']} campaign(s):\n")
    for campaign in data["data"]:
        print(f"  [{campaign['id']}] {campaign['title']} (system: {campaign['system']})")

    return data["data"]


def list_characters(campaign_id: str):
    """List characters in a campaign."""
    resp = requests.get(
        f"{BASE_URL}/v1/characters",
        headers=HEADERS,
        params={"campaign_id": campaign_id, "size": 10},
    )
    resp.raise_for_status()
    data = resp.json()

    print(f"\nCharacters in campaign ({data['total']} total):\n")
    for char in data["data"]:
        aliases = ", ".join(char.get("character_aliases", []))
        alias_str = f" (aliases: {aliases})" if aliases else ""
        print(f"  [{char['type']}] {char['character_name']}{alias_str}")


def list_sessions(campaign_id: str):
    """List game sessions in a campaign."""
    resp = requests.get(
        f"{BASE_URL}/v1/sessions",
        headers=HEADERS,
        params={"campaign_id": campaign_id, "size": 5},
    )
    resp.raise_for_status()
    data = resp.json()

    print(f"\nSessions ({data['total']} total):\n")
    for session in data["data"]:
        date = session.get("session_date", "unknown date")
        print(f"  [{session['type']}] {session['title']} — {date}")


if __name__ == "__main__":
    campaigns = list_campaigns()
    if campaigns:
        first = campaigns[0]
        list_characters(first["id"])
        list_sessions(first["id"])
