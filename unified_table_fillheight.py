#!/usr/bin/env python3
"""
unified_table_fillheight.py
------------------------------
Stretches the unified table rows vertically so they fill the full height
of the right-side panel (matching the left Spot Rate panel's height),
instead of leaving empty black space below the last row.

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 unified_table_fillheight.py

Backs up current index.html as index.html.bak10 first.
"""
import shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak10")
print(f"Backup saved as {FILE}.bak10")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Make the rows-container flex and grow, with each row sharing equal space
old_css = """.ut-wrap{flex:1;display:flex;flex-direction:column;padding:10px 24px 10px 0;width:100%}"""
new_css = """.ut-wrap{flex:1;display:flex;flex-direction:column;padding:10px 24px 10px 0;width:100%;height:100%}
#unifiedRows{flex:1;display:flex;flex-direction:column;gap:10px}
#unifiedRows .ut-row{flex:1;margin-bottom:0}"""

if old_css in html:
    html = html.replace(old_css, new_css)
    print("Patched .ut-wrap and added flex-grow rules for #unifiedRows rows.")
else:
    print("WARNING: exact .ut-wrap rule not found — trying fallback append.")
    html = html.replace(
        "</style>",
        "#unifiedRows{flex:1;display:flex;flex-direction:column;gap:10px}\n#unifiedRows .ut-row{flex:1;margin-bottom:0}\n</style>",
        1
    )

# Ensure .ut-row text scales up a bit since rows will be taller now
html = html.replace(
    ".ut-name{font-size:22px;font-weight:800;color:var(--text)}",
    ".ut-name{font-size:26px;font-weight:800;color:var(--text)}"
)
html = html.replace(
    ".ut-buy{font-size:22px;font-weight:800;color:var(--text);font-variant-numeric:tabular-nums}",
    ".ut-buy{font-size:28px;font-weight:800;color:var(--text);font-variant-numeric:tabular-nums}"
)
html = html.replace(
    ".ut-sell{font-size:22px;font-weight:800;color:var(--text);font-variant-numeric:tabular-nums}",
    ".ut-sell{font-size:28px;font-weight:800;color:var(--text);font-variant-numeric:tabular-nums}"
)
html = html.replace(
    ".ut-weight{font-size:18px;font-weight:700;color:var(--text)}",
    ".ut-weight{font-size:20px;font-weight:700;color:var(--text)}"
)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Rows will now stretch to fill the full panel height.")
print("Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak10 index.html")
