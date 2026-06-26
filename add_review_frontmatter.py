#!/usr/bin/env python3
"""Add score, date, date_display, meeting_date fields to review HTML front matter."""
import os
import re

REVIEWS_DIR = os.path.join(os.path.dirname(__file__), "reviews")

UPDATES = {
    "bellevue-sd-may-2026.html": {
        "score": 76,
        "date": "2026-06-19",
        "date_display": "June 19, 2026",
        "meeting_date": "June 3, 2026",
    },
    "cleveland-metro-sd-may-2026.html": {
        "score": 37,
        "date": "2026-06-01",
        "date_display": "June 2026",
        "meeting_date": "May 27, 2026",
    },
    "fairview-isd-may-2026.html": {
        "score": 82,
        "date": "2026-06-01",
        "date_display": "June 2026",
        "meeting_date": "May 11, 2026",
    },
    "jefferson-city-sd-may-2026.html": {
        "score": 42,
        "date": "2026-06-17",
        "date_display": "June 17, 2026",
        "meeting_date": "May 20, 2026",
    },
    "mesa-usd-may-2026.html": {
        "score": 63,
        "date": "2026-06-01",
        "date_display": "June 2026",
        "meeting_date": "May 14, 2026",
    },
}

def process_file(fname, fields):
    path = os.path.join(REVIEWS_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        print(f"  SKIP (no front matter): {fname}")
        return

    end = content.index("---", 3)
    front = content[3:end]
    rest = content[end:]

    # Build the new fields to append (before closing ---)
    additions = ""
    for key, val in fields.items():
        if re.search(rf'^{key}:', front, re.MULTILINE):
            print(f"  SKIP {key} (already present): {fname}")
            continue
        if isinstance(val, str):
            additions += f'{key}: "{val}"\n'
        else:
            additions += f'{key}: {val}\n'

    if not additions:
        print(f"  SKIP (all fields already present): {fname}")
        return

    new_front = front.rstrip('\n') + '\n' + additions
    new_content = "---" + new_front + rest
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  UPDATED: {fname}")

if __name__ == "__main__":
    for fname, fields in UPDATES.items():
        process_file(fname, fields)
    print("Done.")
