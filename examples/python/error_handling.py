"""Archivist API — Error handling and retry patterns."""

import os
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://api.myarchivist.ai"
API_KEY = os.environ["ARCHIVIST_API_KEY"]
HEADERS = {"x-api-key": API_KEY}


def create_session_with_retries():
    """Create a requests session with automatic retry on transient failures.

    Only idempotent methods (GET, PUT, DELETE) are retried automatically.
    POST and PATCH are never retried by the adapter: a 5xx or a timeout on a
    write does NOT mean the write failed: the
    API may have committed it after the connection dropped, and retrying
    blindly can create a duplicate. See write_with_verification below.
    """
    session = requests.Session()
    idempotent = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "PUT", "DELETE"],
    )
    session.mount("https://", HTTPAdapter(max_retries=idempotent))
    session.headers.update(HEADERS)
    return session


class WriteOutcomeUnknown(Exception):
    """A POST/PATCH timed out or returned 5xx and the change is not visible yet."""


def write_with_verification(method: str, url: str, payload: dict, verify, checks: int = 4):
    """Send a POST/PATCH exactly once; on a timeout or 5xx, find out what happened.

    The request is never resent automatically. A timed-out write may still be
    running on the server, so a read that doesn't see it yet does not prove it
    failed; resending could make both requests commit. Instead, re-read a few
    times with backoff via ``verify()`` (re-read the record you patched, or
    list the collection you appended to; return True if the change is there).
    If it never shows up, raise WriteOutcomeUnknown and let a person (or a
    later reconciliation step) decide whether to send it again.
    """
    try:
        resp = requests.request(method, url, headers=HEADERS, json=payload, timeout=60)
        if resp.status_code < 500:
            return resp
    except requests.Timeout:
        pass
    for attempt in range(checks):
        time.sleep(2 ** attempt)
        if verify():
            print("Write was applied despite the error.")
            return None
    raise WriteOutcomeUnknown(
        f"{method} {url} did not confirm and the change is not visible yet; "
        "check again later before sending it a second time."
    )


def handle_api_error(resp: requests.Response) -> None:
    """Parse and display API error responses."""
    if resp.ok:
        return

    try:
        error = resp.json()
        detail = error.get("detail", resp.text)
    except ValueError:
        detail = resp.text

    if resp.status_code == 401:
        print(f"Authentication failed: {detail}")
        print("Check that your API key is valid and not expired.")
    elif resp.status_code == 403:
        print(f"Access denied: {detail}")
        print("Your API key may not have access to this resource.")
    elif resp.status_code == 404:
        print(f"Not found: {detail}")
    elif resp.status_code == 422:
        print(f"Validation error: {detail}")
    elif resp.status_code == 429:
        print(f"Rate limited. Retry after a brief pause.")
    else:
        print(f"API error ({resp.status_code}): {detail}")


def rate_limit_aware_fetch(url: str, params: dict = None):
    """Fetch with manual rate-limit backoff (alternative to retry adapter)."""
    max_attempts = 3
    for attempt in range(max_attempts):
        resp = requests.get(url, headers=HEADERS, params=params)
        if resp.status_code == 429:
            wait = 2 ** attempt
            print(f"Rate limited, waiting {wait}s before retry...")
            time.sleep(wait)
            continue
        return resp
    return resp


if __name__ == "__main__":
    client = create_session_with_retries()

    resp = client.get(f"{BASE_URL}/v1/campaigns", params={"size": 1})
    handle_api_error(resp)

    if resp.ok:
        data = resp.json()
        print(f"Success: found {data['total']} campaigns")

    print("\n--- Testing error handling ---")
    resp = client.get(f"{BASE_URL}/v1/campaigns/nonexistent-id-12345")
    handle_api_error(resp)
