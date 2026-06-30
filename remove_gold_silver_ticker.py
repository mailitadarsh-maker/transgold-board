#!/usr/bin/env python3
"""
remove_gold_silver_ticker.py
-------------------------------
Removes "Gold" and "Silver" entries from the original ticker tape symbols
list, since they're redundant — already shown live in the Spot Rate panel.

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 remove_gold_silver_ticker.py

Backs up current index.html as index.html.bak15 first.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak15")
print(f"Backup saved as {FILE}.bak15")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Remove entries like {"proName":"FOREXCOM:XAUUSD","title":"Gold"},
# and {"proName":"FOREXCOM:XAGUSD","title":"Silver"},
pattern = re.compile(
    r'\s*\{\s*"proName"\s*:\s*"[^"]*"\s*,\s*"title"\s*:\s*"(Gold|Silver)"\s*\}\s*,?'
)
count = len(pattern.findall(html))
if count:
    html = pattern.sub("", html)
    print(f"Removed {count} Gold/Silver entr(y/ies) from the ticker tape.")
else:
    print("NOTE: no Gold/Silver entries found in ticker JSON — skipping.")

# Clean up any resulting stray commas
html = re.sub(r',\s*,', ',', html)
html = re.sub(r'\[\s*,', '[', html)
html = re.sub(r',\s*\]', ']', html)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak15 index.html")
