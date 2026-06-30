#!/usr/bin/env python3
"""
clean_all_broken_symbols.py
-------------------------------
TradingView's embedded ticker-tape widget can't be made to auto-hide
broken symbols via JS (it's a cross-origin iframe, so we can't detect
errors from outside). The reliable fix is to remove every symbol that
has shown a red error icon so far:
    Gold, Silver, Platinum, Palladium, S&P 500

This keeps only the confirmed-working symbols (Bitcoin, EUR/USD,
GBP/USD, USD/JPY, Crude Oil, etc.) across ALL ticker-tape widgets in
the file (in case there's more than one, e.g. header + footer).

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 clean_all_broken_symbols.py

Backs up current index.html as index.html.bak16 first.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak16")
print(f"Backup saved as {FILE}.bak16")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

BROKEN_TITLES = ["Gold", "Silver", "Platinum", "Palladium", "S&P 500", "Copper"]

total_removed = 0
for title in BROKEN_TITLES:
    pattern = re.compile(
        r'\s*\{\s*"proName"\s*:\s*"[^"]*"\s*,\s*"title"\s*:\s*"' + re.escape(title) + r'"\s*\}\s*,?'
    )
    matches = pattern.findall(html)
    if matches:
        html = pattern.sub("", html)
        total_removed += len(matches)
        print(f"Removed {len(matches)} '{title}' entr(y/ies).")

if total_removed == 0:
    print("No broken-symbol entries found — they may already be removed.")

# Clean up any resulting stray commas / empty array issues
html = re.sub(r',\s*,', ',', html)
html = re.sub(r'\[\s*,', '[', html)
html = re.sub(r',\s*\]', ']', html)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done. Removed {total_removed} broken symbol entries total.")
print("Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak16 index.html")
