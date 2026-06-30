#!/usr/bin/env python3
"""
unified_table_whitefit.py
---------------------------
Two tweaks to the unified right-side table:
  1. Buy/Sell numbers: blue -> white
  2. Table stretches to fill the full available width of the screen

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 unified_table_whitefit.py

Backs up current index.html as index.html.bak9 first.
"""
import shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak9")
print(f"Backup saved as {FILE}.bak9")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ── 1. Buy/Sell colors: blue -> white ──────────────────────────────
html = html.replace(
    ".ut-weight{font-size:18px;font-weight:700;color:var(--blue,#3FA9E0);}",
    ".ut-weight{font-size:18px;font-weight:700;color:var(--text);}"
)
html = html.replace(
    ".ut-weight{font-size:18px;font-weight:700;color:var(--blue,#3FA9E0)}",
    ".ut-weight{font-size:18px;font-weight:700;color:var(--text)}"
)
html = html.replace(
    ".ut-buy{font-size:22px;font-weight:800;color:var(--blue,#3FA9E0);font-variant-numeric:tabular-nums}",
    ".ut-buy{font-size:22px;font-weight:800;color:var(--text);font-variant-numeric:tabular-nums}"
)
html = html.replace(
    ".ut-sell{font-size:22px;font-weight:800;color:var(--blue,#3FA9E0);font-variant-numeric:tabular-nums}",
    ".ut-sell{font-size:22px;font-weight:800;color:var(--text);font-variant-numeric:tabular-nums}"
)

# ── 2. Make the table fill the full available width ────────────────
# .prices already has flex:1 in most layouts, but ensure ut-wrap/rows
# stretch fully and don't leave dead space on the right edge.
html = html.replace(
    ".ut-wrap{flex:1;display:flex;flex-direction:column;padding:10px 0}",
    ".ut-wrap{flex:1;display:flex;flex-direction:column;padding:10px 24px 10px 0;width:100%}"
)
html = html.replace(
    ".ut-head{display:grid;grid-template-columns:1.6fr 1fr 1.1fr 1.1fr;",
    ".ut-head{width:100%;display:grid;grid-template-columns:1.6fr 1fr 1.1fr 1.1fr;"
)
html = html.replace(
    ".ut-row{display:grid;grid-template-columns:1.6fr 1fr 1.1fr 1.1fr;align-items:center;",
    ".ut-row{width:100%;display:grid;grid-template-columns:1.6fr 1fr 1.1fr 1.1fr;align-items:center;"
)

# Also ensure the parent .prices flex grows to take all remaining space
html = html.replace(
    '<div class="prices ut-wrap">',
    '<div class="prices ut-wrap" style="flex:1 1 auto;width:100%">'
)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Buy/Sell text changed to white, table widened to fill the display.")
print("Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak9 index.html")
