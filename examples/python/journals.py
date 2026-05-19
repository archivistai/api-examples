"""Archivist API — Journal entry examples."""

import os
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def list_journal_entries(campaign_id: str):
    """List journal entries in a campaign (content excluded from list)."""
    resp = requests.get(
        f"{BASE_URL}/v1/journals",
        headers=HEADERS,
        params={"campaign_id": campaign_id},
    )
    resp.raise_for_status()
    data = resp.json()

    print(f"Journal entries ({data['total']} total):\n")
    for entry in data["data"]:
        status_badge = f"[{entry.get('status', 'draft')}]"
        print(f"  {status_badge} {entry['title']} (tokens: {entry.get('token_count', 0)})")

    return data["data"]


def get_journal_entry(entry_id: str):
    """Get a full journal entry including content."""
    resp = requests.get(f"{BASE_URL}/v1/journals/{entry_id}", headers=HEADERS)
    resp.raise_for_status()
    entry = resp.json()

    print(f"\n{'='*60}")
    print(f"Title: {entry['title']}")
    print(f"Status: {entry.get('status', 'draft')}")
    print(f"Tags: {', '.join(entry.get('tags', []))}")
    print(f"Permission: {entry.get('permission_level', 'N/A')}")
    print(f"{'='*60}")
    print(f"\n{entry.get('content', '(no content)')[:500]}")


def create_journal_entry(campaign_id: str):
    """Create a new journal entry."""
    payload = {
        "campaign_id": campaign_id,
        "title": "Session 12 — The Battle of Thornwall",
        "content": "The party finally reached Thornwall at dusk...",
        "tags": ["session-recap", "battle", "thornwall"],
        "is_public": False,
        "status": "draft",
    }

    resp = requests.post(f"{BASE_URL}/v1/journals", headers=HEADERS, json=payload)
    resp.raise_for_status()
    result = resp.json()

    print(f"\nCreated journal entry: {result['id']}")
    return result


def list_journal_folders(campaign_id: str):
    """List journal folders for organizing entries."""
    resp = requests.get(
        f"{BASE_URL}/v1/journal-folders",
        headers=HEADERS,
        params={"campaign_id": campaign_id},
    )
    resp.raise_for_status()
    data = resp.json()

    print(f"\nJournal folders ({len(data['data'])} total):\n")
    for folder in data["data"]:
        indent = "  " * folder["path"].count("/")
        print(f"  {indent}{folder['name']} (path: {folder['path']})")


if __name__ == "__main__":
    campaign_id = os.environ.get("ARCHIVIST_CAMPAIGN_ID")
    if not campaign_id:
        print("Set ARCHIVIST_CAMPAIGN_ID to run this example")
        exit(1)

    entries = list_journal_entries(campaign_id)
    if entries:
        get_journal_entry(entries[0]["id"])
    list_journal_folders(campaign_id)
