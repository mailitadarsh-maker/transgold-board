#!/usr/bin/env python3
"""
update_spot.py

Polls the Arakkal Markets terminal feed for Gold + Silver every 30 seconds
and writes a clean live_prices.json file that index.html reads from.

This replaces the old hardcoded fallback / broken /api/prices.php call.
Run it from your terminal, in the same folder as index.html:

    cd /Users/adarsh/transgold-board
    python3 update_spot.py

Leave it running (it loops forever, printing each update). To run it in
the background so it keeps going after you close the terminal:

    nohup python3 update_spot.py > update_spot.log 2>&1 &

Stop it later with:  pkill -f update_spot.py
"""

import html
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

GOLD_URL   = "https://portal.arakkalmarkets.com/getprice/GOLD"
SILVER_URL = "https://portal.arakkalmarkets.com/getprice/SILVER"
OUTPUT_FILE = Path(__file__).parent / "live_prices.json"
HILO_FILE = Path(__file__).parent / "daily_hilo.json"
POLL_SECONDS = 30
REQUEST_TIMEOUT = 8


def load_hilo() -> dict:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if HILO_FILE.exists():
        try:
            data = json.loads(HILO_FILE.read_text())
            if data.get("date") == today:
                return data
        except (json.JSONDecodeError, OSError):
            pass
    # New day or missing/corrupt file -> fresh tracker
    return {"date": today, "gold_low": None, "gold_high": None,
            "silver_low": None, "silver_high": None}


def update_hilo(gold_mid: float, silver_mid: float) -> dict:
    hilo = load_hilo()
    if hilo["gold_low"] is None or gold_mid < hilo["gold_low"]:
        hilo["gold_low"] = gold_mid
    if hilo["gold_high"] is None or gold_mid > hilo["gold_high"]:
        hilo["gold_high"] = gold_mid
    if hilo["silver_low"] is None or silver_mid < hilo["silver_low"]:
        hilo["silver_low"] = silver_mid
    if hilo["silver_high"] is None or silver_mid > hilo["silver_high"]:
        hilo["silver_high"] = silver_mid
    HILO_FILE.write_text(json.dumps(hilo, indent=2))
    return hilo

BID_RE = re.compile(r'"Bid"\s*=>\s*([0-9]+(?:\.[0-9]+)?)', re.DOTALL)
ASK_RE = re.compile(r'"Ask"\s*=>\s*([0-9]+(?:\.[0-9]+)?)', re.DOTALL)


def fetch_mid(url: str) -> float:
    """Fetch a metal's page and return the midpoint of Bid/Ask."""
    req = urllib.request.Request(url, headers={"User-Agent": "TransgoldBoard/1.0"})
    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
        raw_body = resp.read().decode("utf-8", errors="replace")

    # The endpoint can return either plain text OR a Laravel/Symfony debug-dump
    # HTML page (each value wrapped in <span> tags). Strip any HTML tags and
    # unescape entities so "Bid" => <span...>3978.48</span> becomes
    # "Bid" => 3978.48 either way.
    body = html.unescape(re.sub(r"<[^>]+>", "", raw_body))

    bid_match = BID_RE.search(body)
    ask_match = ASK_RE.search(body)
    if not bid_match or not ask_match:
        raise ValueError(f"Could not parse Bid/Ask from response: {body[:200]!r}")

    bid = float(bid_match.group(1))
    ask = float(ask_match.group(1))
    return round((bid + ask) / 2, 3)


def write_output(gold_mid: float, silver_mid: float, source: str) -> None:
    hilo = update_hilo(gold_mid, silver_mid)
    payload = {
        "ok": True,
        "gold": gold_mid,
        "silver": silver_mid,
        "goldLow": hilo["gold_low"],
        "goldHigh": hilo["gold_high"],
        "silverLow": hilo["silver_low"],
        "silverHigh": hilo["silver_high"],
        "source": source,
        "updated": datetime.now(timezone.utc).isoformat(),
    }
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2))


def read_last_good() -> dict | None:
    if not OUTPUT_FILE.exists():
        return None
    try:
        return json.loads(OUTPUT_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def run_once() -> None:
    try:
        gold_mid = fetch_mid(GOLD_URL)
        silver_mid = fetch_mid(SILVER_URL)
        write_output(gold_mid, silver_mid, source="live")
        stamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{stamp}] OK  gold={gold_mid:>10,.3f}  silver={silver_mid:>10,.3f}")
    except Exception as exc:
        stamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{stamp}] FAIL  {exc}")
        last = read_last_good()
        if last:
            last["source"] = "cache"
            OUTPUT_FILE.write_text(json.dumps(last, indent=2))
            print(f"          -> serving last known good prices instead")


def main() -> None:
    print(f"Writing live prices to: {OUTPUT_FILE}")
    print(f"Polling every {POLL_SECONDS}s. Press Ctrl+C to stop.\n")
    try:
        while True:
            run_once()
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
