#!/usr/bin/env python3
"""
CLI wrapper for the JotForm downloader.

Usage:
    python download.py --list
    python download.py <form_id>
    python download.py <form_id> --output my_file.xlsx
"""

import argparse
import os
import sys

import openpyxl
from dotenv import load_dotenv

import jotform

load_dotenv()


def get_api_key() -> str:
    key = os.environ.get("JOTFORM_API_KEY", "").strip()
    if not key:
        sys.exit(
            "Error: JOTFORM_API_KEY environment variable is not set.\n"
            "Copy .env.example to .env and add your API key."
        )
    return key


def cmd_list(api_key: str) -> None:
    print("Fetching forms…")
    forms = jotform.get_forms(api_key)
    if not forms:
        print("No forms found for this account.")
        return
    id_width = max(len(f["id"]) for f in forms)
    print(f"\n{'ID':<{id_width}}  Title")
    print("-" * (id_width + 2 + 40))
    for f in forms:
        print(f"{f['id']:<{id_width}}  {f['title']}")
    print(f"\n{len(forms)} form(s) found.")


def cmd_download(api_key: str, form_id: str, output_path: str) -> None:
    print(f"Fetching submissions for form {form_id}…")
    submissions = jotform.get_submissions(api_key, form_id)
    if not submissions:
        print("No submissions found.")
        return

    headers, rows = jotform.submissions_to_rows(submissions)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Submissions"
    ws.append(headers)

    # Bold header row
    from openpyxl.styles import Font
    for cell in ws[1]:
        cell.font = Font(bold=True)

    for row in rows:
        ws.append(row)

    # Auto-size columns (capped at 60 chars wide)
    for col in ws.columns:
        max_len = max((len(str(cell.value or "")) for cell in col), default=0)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 60)

    wb.save(output_path)
    print(f"Saved {len(rows)} submission(s) to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download JotForm submissions to an Excel file."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all forms with their IDs and names, then exit.",
    )
    parser.add_argument(
        "form_id",
        nargs="?",
        help="The JotForm form ID to download submissions from.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output .xlsx filename (default: submissions_<form_id>.xlsx).",
    )
    args = parser.parse_args()

    api_key = get_api_key()

    if args.list:
        cmd_list(api_key)
        return

    if not args.form_id:
        parser.error("A form_id is required unless --list is used.")

    output = args.output or os.path.join(
        os.path.expanduser("~"), "Downloads", f"submissions_{args.form_id}.xlsx"
    )
    cmd_download(api_key, args.form_id, output)


if __name__ == "__main__":
    main()
