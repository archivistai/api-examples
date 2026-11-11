"""Archivist API — Read, fix and review a PC's Character Arc.

After a session is processed, proposed arc changes are stored as *pending*
facets (the web app's Character Arc Changes dialog). This example lists them,
shows what each update would replace, and approves the run.
"""

import os
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def get_arc(character_id: str, status: str = "approved") -> dict:
    """status: approved (canon), pending (awaiting review) or all."""
    resp = requests.get(f"{BASE_URL}/v1/characters/{character_id}/arc", headers=HEADERS, params={"status": status})
    resp.raise_for_status()
    return resp.json()


def print_pending(character_id: str) -> set[str]:
    """Print pending changes like the review dialog; return their run ids."""
    arc = get_arc(character_id, status="pending")
    run_ids = set()
    for theme in arc["themes"]:
        for facet in theme["facets"]:
            run_ids.add(facet["run_id"])
            kind = "UPDATED" if facet["replaces_id"] else "NEW"
            print(f"[{kind}] {theme['title']} / {facet['title']} (session {facet['session_number']})")
            if facet["previous_description"]:
                print(f"    before: {facet['previous_description']}")
            print(f"    after:  {facet['description']}")
    return run_ids


def fix_facet(character_id: str, facet_id: str, **changes) -> dict:
    """Edit a facet. A title/description change returns a NEW facet id."""
    resp = requests.patch(
        f"{BASE_URL}/v1/characters/{character_id}/arc/facets/{facet_id}",
        headers=HEADERS,
        json=changes,
    )
    resp.raise_for_status()
    return resp.json()


def review_run(character_id: str, run_id: str, action: str = "approve") -> dict:
    """Approve or decline every pending change from one processing run."""
    resp = requests.post(
        f"{BASE_URL}/v1/characters/{character_id}/arc/runs/{run_id}/review",
        headers=HEADERS,
        json={"action": action},
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    character_id = os.environ.get("ARCHIVIST_CHARACTER_ID")
    if not character_id:
        print("Set ARCHIVIST_CHARACTER_ID (a PC) to run this example")
        exit(1)

    run_ids = print_pending(character_id)
    if not run_ids:
        print("No pending Character Arc changes.")
    elif os.environ.get("ARCHIVIST_APPROVE") == "1":
        for run_id in run_ids:
            print(review_run(character_id, run_id, "approve"))
    else:
        print("\nSet ARCHIVIST_APPROVE=1 to approve these runs.")
