#!/usr/bin/env python3
"""
remove_broken_ticker.py
--------------------------
1. Removes the second "metals" ticker strip added by add_metals_ticker.py
   (Platinum/Palladium/Copper symbols weren't returning valid price data —
   all showed red error icons).
2. Removes "Platinum" from the ORIGINAL ticker tape too, since it also
   shows no data there (red exclamation icon).

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 remove_broken_ticker.py

Backs up current index.html as index.html.bak14 first.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak14")
print(f"Backup saved as {FILE}.bak14")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ──────────────────────────────────────────────
# 1. Remove the second metals ticker block entirely
# ──────────────────────────────────────────────
metals_pattern = re.compile(
    r'\n*<!-- Second ticker: other metals only.*?</div>\s*</div>\s*\n*',
    re.DOTALL
)
if metals_pattern.search(html):
    html = metals_pattern.sub("\n", html, count=1)
    print("Removed the second metals ticker strip.")
else:
    print("NOTE: second metals ticker block not found (maybe already removed) — skipping.")

# ──────────────────────────────────────────────
# 2. Remove "Platinum" entry from the ORIGINAL ticker tape symbols list
#    Matches a JSON-style entry like: {"proName":"...","title":"Platinum"},
# ──────────────────────────────────────────────
platinum_pattern = re.compile(
    r'\s*\{\s*"proName"\s*:\s*"[^"]*"\s*,\s*"title"\s*:\s*"Platinum"\s*\}\s*,?'
)
count = len(platinum_pattern.findall(html))
if count:
    html = platinum_pattern.sub("", html)
    print(f"Removed {count} 'Platinum' entr(y/ies) from the original ticker tape.")
else:
    print("NOTE: no 'Platinum' entry found in original ticker JSON — skipping.")

# Clean up any resulting double commas in the symbols array, just in case
html = re.sub(r',\s*,', ',', html)
html = re.sub(r'\[\s*,', '[', html)
html = re.sub(r',\s*\]', ']', html)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak14 index.html")
