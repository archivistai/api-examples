"""Archivist API — RAG chat (Ask) examples."""

import os
import requests
import json

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def ask_question(campaign_id: str, question: str):
    """Ask a question about your campaign using RAG."""
    payload = {
        "campaign_id": campaign_id,
        "messages": [{"role": "user", "content": question}],
        "stream": False,
    }

    resp = requests.post(f"{BASE_URL}/v1/ask", headers=HEADERS, json=payload)
    resp.raise_for_status()
    data = resp.json()

    print(f"Q: {question}")
    print(f"A: {data['answer']}")

    citations = data.get("citations", [])
    if citations:
        print(f"\nCitations ({len(citations)}):")
        for c in citations:
            label = c.get("title") or c.get("source_type", "unknown")
            if c.get("session_number"):
                label += f" (Session {c['session_number']})"
            print(f"  - [{c.get('citation_id')}] {label}")
    print()

    return data


def ask_streaming(campaign_id: str, question: str):
    """Ask a question with streaming response (SSE)."""
    payload = {
        "campaign_id": campaign_id,
        "messages": [{"role": "user", "content": question}],
        "stream": True,
    }

    resp = requests.post(
        f"{BASE_URL}/v1/ask",
        headers=HEADERS,
        json=payload,
        stream=True,
    )
    resp.raise_for_status()

    print(f"Q: {question}")
    print("A: ", end="", flush=True)

    for line in resp.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data: "):
            continue
        chunk_str = line[6:]
        if chunk_str == "[DONE]":
            break
        try:
            chunk = json.loads(chunk_str)
            token = chunk.get("token", "")
            print(token, end="", flush=True)
        except json.JSONDecodeError:
            continue

    print("\n")


if __name__ == "__main__":
    campaign_id = os.environ.get("ARCHIVIST_CAMPAIGN_ID")
    if not campaign_id:
        print("Set ARCHIVIST_CAMPAIGN_ID to run this example")
        exit(1)

    ask_question(campaign_id, "Who are the main characters in this campaign?")
    ask_question(campaign_id, "What happened in the last session?")
