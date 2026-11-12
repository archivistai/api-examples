"""Archivist API — Read and update structured compendium Properties.

Properties are the structured fields on characters, factions, locations and
items (for PCs: Identity, e.g. class/species/alignment, and Connections, e.g.
allies/memberships/signature_item; other entities have a General table).
"""

import os
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def get_properties(campaign_id: str, entity_type: str, entity_id: str) -> dict:
    """GET /v1/entities/{id}/properties — tables of fields with their values."""
    resp = requests.get(
        f"{BASE_URL}/v1/entities/{entity_id}/properties",
        headers=HEADERS,
        params={"campaign_id": campaign_id, "type": entity_type},
    )
    resp.raise_for_status()
    data = resp.json()
    for table in data["tables"]:
        print(f"\n{table['label']}:")
        for field in table["fields"]:
            if field.get("connections") is not None:
                refs = ", ".join(f"{ref['name']} ({ref['id']})" for ref in field["connections"]) or "—"
                print(f"  {field['key']:<20} {refs}")
            else:
                print(f"  {field['key']:<20} {field['value'] if field['value'] is not None else '—'}")
    return data


def update_properties(campaign_id: str, entity_type: str, entity_id: str, properties: dict) -> dict:
    """PATCH /v1/entities/{id}/properties — only the keys you send change.

    Connection fields accept a list of entity ids or exact names (replaces the
    list), [] to clear, or {"add": [...], "remove": [...]} to edit it.
    """
    resp = requests.patch(
        f"{BASE_URL}/v1/entities/{entity_id}/properties",
        headers=HEADERS,
        params={"campaign_id": campaign_id, "type": entity_type},
        json={"properties": properties},
    )
    if resp.status_code == 422:
        # Unknown keys or references that don't resolve: nothing was written.
        print(f"Rejected: {resp.json()['detail']}")
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    campaign_id = os.environ.get("ARCHIVIST_CAMPAIGN_ID")
    character_id = os.environ.get("ARCHIVIST_CHARACTER_ID")
    if not campaign_id or not character_id:
        print("Set ARCHIVIST_CAMPAIGN_ID and ARCHIVIST_CHARACTER_ID to run this example")
        exit(1)

    get_properties(campaign_id, "characters", character_id)

    faction_id = os.environ.get("ARCHIVIST_FACTION_ID")
    if faction_id:
        # A PC joins a faction: add it to Memberships without resending the list.
        update_properties(campaign_id, "characters", character_id, {"memberships": {"add": [faction_id]}})
        get_properties(campaign_id, "characters", character_id)
