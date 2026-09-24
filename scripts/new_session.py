#!/usr/bin/env python3
"""Create a directory for one training event without touching existing sessions."""

import argparse
import re
from datetime import date
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title", help="Training title")
    parser.add_argument("--date", default=date.today().isoformat(), help="Archive date (YYYY-MM-DD)")
    args = parser.parse_args()
    date.fromisoformat(args.date)
    slug = re.sub(r"[^a-z0-9]+", "-", args.title.lower()).strip("-")
    if not slug:
        parser.error("title must contain letters or numbers")
    target = Path(__file__).resolve().parents[1] / "sessions" / f"{args.date}-{slug}"
    if target.exists():
        parser.error(f"session already exists: {target}")
    (target / "source").mkdir(parents=True)
    (target / "README.md").write_text(
        f"# {args.title}\n\n"
        f"- Archive date: {args.date}\n"
        "- Training date: Unknown\n"
        "- Provider / instructor: To add\n\n"
        "## Source links\n\n- Add original URLs here.\n\n"
        "## Materials\n\n- Add files to `source/` and describe them here.\n\n"
        "## Review questions\n\n- Add questions to revisit.\n",
        encoding="utf-8",
    )
    (target / "notes.md").write_text(f"# Notes: {args.title}\n\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
