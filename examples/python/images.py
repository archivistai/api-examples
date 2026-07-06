#!/usr/bin/env python3
"""Entity image quota, AI generation, and direct upload examples.

Requires ARCHIVIST_API_KEY and a campaign where you have manage access.
Set CAMPAIGN_ID and (for generation/upload) CHARACTER_ID before running.
"""

import os
import sys

import requests

API_BASE = os.environ.get("ARCHIVIST_API_BASE", "https://api.myarchivist.ai")
API_KEY = os.environ.get("ARCHIVIST_API_KEY")
CAMPAIGN_ID = os.environ.get("CAMPAIGN_ID", "")
CHARACTER_ID = os.environ.get("CHARACTER_ID", "")

if not API_KEY:
    sys.exit("Set ARCHIVIST_API_KEY")


def headers():
    return {"x-api-key": API_KEY, "Content-Type": "application/json"}


def get_image_usage(campaign_id: str):
    response = requests.get(
        f"{API_BASE}/v1/images/usage",
        params={"campaign_id": campaign_id},
        headers={"x-api-key": API_KEY},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def generate_image(campaign_id: str, character_id: str, user_input: str | None = None):
    payload = {
        "campaign_id": campaign_id,
        "type": "character",
        "entity_id": character_id,
    }
    if user_input:
        payload["user_input"] = user_input
    response = requests.post(
        f"{API_BASE}/v1/images/generate",
        json=payload,
        headers=headers(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def init_upload(campaign_id: str, entity_type: str, entity_id: str, file_name: str, content_type: str):
    response = requests.post(
        f"{API_BASE}/v1/campaigns/{campaign_id}/images/init",
        json={
            "entity_type": entity_type,
            "entity_id": entity_id,
            "file_name": file_name,
            "content_type": content_type,
        },
        headers=headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def complete_upload(
    campaign_id: str,
    object_key: str,
    entity_type: str,
    entity_id: str,
    attach: bool = True,
):
    response = requests.post(
        f"{API_BASE}/v1/campaigns/{campaign_id}/images/complete",
        json={
            "object_key": object_key,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "attach": attach,
        },
        headers=headers(),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def delete_entity_image(campaign_id: str, entity_type: str, entity_id: str):
    response = requests.delete(
        f"{API_BASE}/v1/campaigns/{campaign_id}/images",
        json={"entity_type": entity_type, "entity_id": entity_id},
        headers=headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main():
    if not CAMPAIGN_ID:
        sys.exit("Set CAMPAIGN_ID")

    usage = get_image_usage(CAMPAIGN_ID)
    print("Image quota:", usage)

    if not usage.get("can_access"):
        print("Image features are not available for this account/campaign.")
        return

    if not CHARACTER_ID:
        print("Set CHARACTER_ID to run generation or upload examples.")
        return

    # AI generation returns a URL — attach it via PATCH /v1/characters/{id} if desired.
    generated = generate_image(CAMPAIGN_ID, CHARACTER_ID)
    print("Generated URL:", generated.get("url"))

    # Direct upload is a two-step flow; step 2 assumes bytes were PUT to upload_url.
    init = init_upload(CAMPAIGN_ID, "character", CHARACTER_ID, "portrait.png", "image/png")
    print("Upload init:", {k: init[k] for k in ("object_key", "public_url", "expires_in_seconds")})
    print("PUT image bytes to upload_url before calling complete_upload().")

    # Example complete call (uncomment after uploading):
    # completed = complete_upload(CAMPAIGN_ID, init["object_key"], "character", CHARACTER_ID)
    # print("Attached:", completed)


if __name__ == "__main__":
    main()
