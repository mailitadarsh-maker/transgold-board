#!/usr/bin/env python3
"""
patch_fetch_url.py

One-time fix: points fetchLivePrices() in index.html at the new local
live_prices.json file (written by update_spot.py) instead of the old,
non-existent /api/prices.php.

Run once from your terminal:

    cd /Users/adarsh/transgold-board
    python3 patch_fetch_url.py
"""

import sys
from pathlib import Path

HTML_FILE = Path("index.html")
OLD = "fetch('/api/prices.php')"
NEW = "fetch('live_prices.json?t=' + Date.now())"  # cache-bust so the browser always gets the latest write


def main() -> None:
    if not HTML_FILE.exists():
        print("❌  index.html not found — run this from the transgold-board folder.")
        sys.exit(1)

    html = HTML_FILE.read_text()

    if NEW in html:
        print("✅  Already patched — nothing to do.")
        return

    if OLD not in html:
        print("⚠️  Couldn't find the expected fetch('/api/prices.php') line.")
        print("    Open index.html and search for 'fetchLivePrices' to update it manually:")
        print(f"    replace any  fetch('/api/prices.php')  with  {NEW}")
        sys.exit(1)

    html = html.replace(OLD, NEW)
    HTML_FILE.write_text(html)
    print("✅  Patched! fetchLivePrices() now reads live_prices.json")


if __name__ == "__main__":
    main()
