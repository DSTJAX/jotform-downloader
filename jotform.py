"""
JotForm API client — reusable module for fetching forms and submissions.
"""

import os
import requests

BASE_URL = "https://api.jotform.com"


def _get(endpoint: str, api_key: str, params: dict = None) -> dict:
    url = f"{BASE_URL}{endpoint}"
    p = {"apiKey": api_key}
    if params:
        p.update(params)
    resp = requests.get(url, params=p, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if data.get("responseCode") != 200:
        raise RuntimeError(f"JotForm API error: {data.get('message', data)}")
    return data


def get_forms(api_key: str) -> list[dict]:
    """Return a list of all forms for the account."""
    results = []
    offset = 0
    limit = 100
    while True:
        data = _get("/user/forms", api_key, {"offset": offset, "limit": limit})
        batch = data.get("content", [])
        results.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
    return results


def get_submissions(api_key: str, form_id: str) -> list[dict]:
    """Return all submissions for the given form ID."""
    results = []
    offset = 0
    limit = 1000
    while True:
        data = _get(
            f"/form/{form_id}/submissions",
            api_key,
            {"offset": offset, "limit": limit},
        )
        batch = data.get("content", [])
        results.extend(batch)
        if len(batch) < limit:
            break
        offset += limit
    return results


def submissions_to_rows(submissions: list[dict]) -> tuple[list[str], list[list]]:
    """
    Convert raw submission dicts into (headers, rows) ready for writing to Excel.

    The JotForm submission payload stores answers under the 'answers' key, keyed
    by question order. Each answer has a 'text' label and a 'answer' value.
    """
    if not submissions:
        return [], []

    # Collect all question labels, preserving insertion order
    label_map: dict[str, str] = {}  # order -> label
    for sub in submissions:
        for order, ans in sub.get("answers", {}).items():
            label = ans.get("text", f"Question {order}")
            if order not in label_map:
                label_map[order] = label

    # Sort by question order (numeric)
    sorted_orders = sorted(label_map.keys(), key=lambda x: int(x))
    headers = ["Submission ID", "Created At"] + [label_map[o] for o in sorted_orders]

    rows = []
    for sub in submissions:
        row = [sub.get("id", ""), sub.get("created_at", "")]
        answers = sub.get("answers", {})
        for order in sorted_orders:
            ans = answers.get(order, {})
            value = ans.get("answer", "")
            # Some answers are dicts (e.g. name, address) — flatten to string
            if isinstance(value, dict):
                value = " ".join(str(v) for v in value.values() if v)
            elif isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            row.append(value)
        rows.append(row)

    return headers, rows
