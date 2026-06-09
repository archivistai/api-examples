"""Archivist API — Session beat list and hierarchy examples."""

import os
import requests

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY}


def list_session_beats(session_id: str, page: int = 1, size: int = 20, with_links: bool = False):
    """Fetch a paginated flat list of beats linked to a session."""
    resp = requests.get(
        f"{BASE_URL}/v1/beats",
        headers=HEADERS,
        params={
            "session_id": session_id,
            "page": page,
            "size": size,
            "with_links": with_links,
        },
    )
    resp.raise_for_status()
    payload = resp.json()
    print(f"Session beats (page {payload['page']}/{payload['pages']}, total {payload['total']}):\n")
    for beat in payload["data"]:
        print(f"  - [{beat['type']}] {beat['label']} (index {beat['index']})")
    return payload


def list_session_beat_tree(session_id: str, with_links: bool = False):
    """Fetch nested beat hierarchy for a session."""
    resp = requests.get(
        f"{BASE_URL}/v1/beats",
        headers=HEADERS,
        params={
            "session_id": session_id,
            "include_hierarchy": True,
            "with_links": with_links,
        },
    )
    resp.raise_for_status()
    beats = resp.json()

    def print_tree(nodes, indent=0):
        for beat in nodes:
            prefix = "  " * indent
            print(f"{prefix}- [{beat['type']}] {beat['label']}")
            children = beat.get("children") or []
            if children:
                print_tree(children, indent + 1)

    print(f"Beat tree for session {session_id}:\n")
    print_tree(beats)
    return beats


if __name__ == "__main__":
    session_id = os.environ.get("ARCHIVIST_SESSION_ID")
    if not session_id:
        print("Set ARCHIVIST_SESSION_ID to run this example")
        exit(1)
    list_session_beats(session_id)
    print()
    list_session_beat_tree(session_id)
