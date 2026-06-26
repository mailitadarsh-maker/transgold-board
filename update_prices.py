#!/usr/bin/env python3
"""
Transgold Markets — Price Updater
Usage:
  python update_prices.py                  # interactive menu
  python update_prices.py --list           # show current prices
"""

import re, json, sys, os

HTML_FILE = "index.html"

# ── read / write helpers ──────────────────────────────────────────────────────
def read_html():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()

def write_html(html):
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅  Saved {HTML_FILE}")

# ── extract current PRICES block ──────────────────────────────────────────────
def get_prices(html):
    m = re.search(r'const PRICES=(\{.*?\});', html, re.DOTALL)
    if not m:
        raise ValueError("Could not find PRICES block in index.html")
    # convert JS object literals to valid JSON
    js = m.group(1)
    js = re.sub(r"'", '"', js)                      # single → double quotes
    js = re.sub(r'(\w+):', r'"\1":', js)            # unquoted keys → quoted
    js = re.sub(r',\s*\}', '}', js)                 # trailing commas
    js = re.sub(r',\s*\]', ']', js)
    return json.loads(js)

def set_prices(html, prices):
    gold_js  = json.dumps(prices["gold"],   indent=4)
    silver_js = json.dumps(prices["silver"], indent=4)
    # rebuild JS-style (single-quoted strings look nicer but double is fine)
    new_block = (
        "const PRICES={\n"
        f"  gold:{gold_js},\n"
        f"  silver:{silver_js}\n"
        "};"
    )
    return re.sub(r'const PRICES=\{.*?\};', new_block, html, flags=re.DOTALL)

# ── display helpers ───────────────────────────────────────────────────────────
LABELS = {
    "gold":   ["9999 · 1 KG", "995 · 1 KG", "916 · 1 GM", "1TB · 1 TTB"],
    "silver": ["999 · 1 KG",  "999 · 1 TTB"],
}

def show_prices(prices):
    for metal in ("gold", "silver"):
        print(f"\n  {'GOLD' if metal=='gold' else 'SILVER'}")
        print(f"  {'#':<4}  {'ITEM':<18}  {'BUY':>12}  {'SELL':>12}")
        print("  " + "─" * 52)
        for i, item in enumerate(prices[metal]):
            lbl = LABELS[metal][i] if i < len(LABELS[metal]) else f"row {i}"
            print(f"  {i+1:<4}  {lbl:<18}  {item['buy']:>12,.2f}  {item['sell']:>12,.2f}")

# ── interactive update ────────────────────────────────────────────────────────
def update_interactive():
    html   = read_html()
    prices = get_prices(html)

    show_prices(prices)

    print("\n  Which metal?  (1) Gold   (2) Silver   (q) Quit")
    ch = input("  > ").strip().lower()
    if ch == "q":
        return
    metal = "gold" if ch == "1" else "silver" if ch == "2" else None
    if not metal:
        print("  Invalid choice."); return

    rows = prices[metal]
    print(f"\n  Which row to update? (1–{len(rows)})  or 'a' to update all")
    ch = input("  > ").strip().lower()

    indices = list(range(len(rows))) if ch == "a" else [int(ch) - 1]

    for idx in indices:
        lbl = LABELS[metal][idx] if idx < len(LABELS[metal]) else f"row {idx}"
        print(f"\n  [{lbl}]  current buy={rows[idx]['buy']:,.2f}  sell={rows[idx]['sell']:,.2f}")

        raw_buy  = input("  New BUY  (Enter to keep): ").strip()
        raw_sell = input("  New SELL (Enter to keep): ").strip()

        if raw_buy:
            rows[idx]["buy"]  = float(raw_buy.replace(",", ""))
        if raw_sell:
            rows[idx]["sell"] = float(raw_sell.replace(",", ""))

    html = set_prices(html, prices)
    write_html(html)
    print("\n  Updated prices:")
    show_prices(get_prices(read_html()))

# ── CLI entry ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not os.path.exists(HTML_FILE):
        print(f"❌  {HTML_FILE} not found — run this script from the same folder.")
        sys.exit(1)

    if "--list" in sys.argv or "-l" in sys.argv:
        show_prices(get_prices(read_html()))
    else:
        update_interactive()
