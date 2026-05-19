"""Archivist API — Quest management examples."""

import os
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def list_quests(campaign_id: str, status: str = None):
    """List quests in a campaign, optionally filtered by status."""
    params = {"campaign_id": campaign_id, "size": 20}
    if status:
        params["status"] = status

    resp = requests.get(f"{BASE_URL}/v1/quests", headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()

    print(f"Quests ({data['total']} total):\n")
    for quest in data["data"]:
        objectives = f"{quest['completed_objective_count']}/{quest['objective_count']} objectives"
        print(f"  [{quest['status']}] {quest['quest_name']} — {objectives}")

    return data["data"]


def get_quest_detail(quest_id: str):
    """Get full quest detail including objectives and progress."""
    resp = requests.get(f"{BASE_URL}/v1/quests/{quest_id}", headers=HEADERS)
    resp.raise_for_status()
    quest = resp.json()

    print(f"\nQuest: {quest['quest_name']}")
    print(f"  Category: {quest['quest_category']}")
    print(f"  Status: {quest['status']}")
    print(f"  Quest Giver: {quest.get('quest_giver', 'Unknown')}")

    if quest.get("objectives"):
        print("\n  Objectives:")
        for obj in quest["objectives"]:
            marker = "✓" if obj["status"] == "completed" else "○"
            print(f"    {marker} {obj['text']}")

    if quest.get("progress_log_entries"):
        print("\n  Progress Log:")
        for entry in quest["progress_log_entries"][:5]:
            session_info = f" (Session: {entry.get('session_title', 'N/A')})" if entry.get("session_title") else ""
            print(f"    • {entry['text']}{session_info}")


def create_quest(campaign_id: str):
    """Create a new quest."""
    payload = {
        "campaign_id": campaign_id,
        "quest_name": "Find the Lost Artifact",
        "quest_category": "main",
        "status": "in-progress",
        "quest_giver": "Elder Moonshadow",
        "success_definition": "Return the Sunstone to the Temple of Dawn",
        "objectives": [
            {"text": "Locate the entrance to the Sunken Vault", "status": "completed"},
            {"text": "Retrieve the Sunstone from the vault guardian", "status": "in-progress"},
            {"text": "Return the Sunstone to Elder Moonshadow", "status": "pending"},
        ],
        "related_characters": ["Elder Moonshadow", "Vault Guardian"],
        "related_locations": ["Sunken Vault", "Temple of Dawn"],
    }

    resp = requests.post(f"{BASE_URL}/v1/quests", headers=HEADERS, json=payload)
    resp.raise_for_status()
    quest = resp.json()

    print(f"\nCreated quest: {quest['quest_name']} (id: {quest['id']})")
    return quest


if __name__ == "__main__":
    campaign_id = os.environ.get("ARCHIVIST_CAMPAIGN_ID")
    if not campaign_id:
        print("Set ARCHIVIST_CAMPAIGN_ID to run this example")
        exit(1)

    quests = list_quests(campaign_id)
    if quests:
        get_quest_detail(quests[0]["id"])
