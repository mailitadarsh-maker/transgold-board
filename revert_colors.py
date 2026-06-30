#!/usr/bin/env python3
"""
revert_colors.py
-----------------
Reverts the color theme changes made by restyle_board.py back to the
ORIGINAL gold/dark theme, while KEEPING the new layout
(spot-rate panel left & wider, commodity table right, second logo slot).

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 revert_colors.py

Backs up current index.html as index.html.bak2 first.
"""
import shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak2")
print(f"Backup saved as {FILE}.bak2")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ──────────────────────────────────────────────
# Revert theme colors back to ORIGINAL values
# ──────────────────────────────────────────────
html = html.replace(
    "--gold:#D8B45A;--gold-dim:#9C7A2A;",
    "--gold:#D4A94A;--gold-dim:#8A6A1F;"
)
html = html.replace(
    "--bg:#070B14;--bg2:#0C1626;--bg3:#13213A;",
    "--bg:#090909;--bg2:#0F0F0F;--bg3:#161616;"
)
html = html.replace(
    "--border-gold:rgba(216,180,90,0.25);\n  --blue:#3FA9E0;\n  --border-blue:rgba(63,169,224,0.35);",
    "--border-gold:rgba(212,169,74,0.18);"
)
html = html.replace(
    "--text:#EAF3FB;--muted:#7C8BA0;",
    "--text:#F0EBE0;--muted:#6B6660;"
)

# Revert row / wtag styling back to original (gold/green look)
html = html.replace(
    ".row{display:grid;grid-template-columns:1.6fr 130px 1fr 1fr;align-items:center;padding:16px 18px;background:var(--bg3);border:1px solid var(--border-blue);border-radius:10px;margin-bottom:10px;position:relative;overflow:hidden;transition:border-color .2s}",
    ".row{display:grid;grid-template-columns:1.6fr 130px 1fr 1fr;align-items:center;padding:14px 16px;background:var(--bg2);border:1px solid var(--border-green);border-radius:8px;margin-bottom:8px;position:relative;overflow:hidden;box-shadow:var(--glow);transition:border-color .2s,box-shadow .2s}"
)
html = html.replace(
    ".wtag{display:inline-flex;align-items:center;justify-content:center;font-size:17px;font-weight:800;padding:9px 20px;border:2px solid var(--blue);border-radius:6px;color:var(--blue);letter-spacing:.1em;background:rgba(63,169,224,.12);min-width:104px}",
    ".wtag{display:inline-flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;padding:8px 18px;border:2px solid var(--gold);border-radius:6px;color:var(--gold);letter-spacing:.1em;background:rgba(212,169,74,.1);min-width:100px}"
)

# Revert the blue accents added in the layout block (box-title / spot pill)
html = html.replace(
    ".box-title{color:var(--blue)}\n.spot-pill.gpill{background:rgba(63,169,224,.15);color:var(--blue);border:1px solid rgba(63,169,224,.4)}",
    ".box-title{color:var(--gold)}\n.spot-pill.gpill{background:rgba(212,169,74,.15);color:var(--gold);border:1px solid rgba(212,169,74,.4)}"
)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Colors reverted to original gold/dark theme.")
print("Layout (spot-rate left/wider, table right, second logo slot) is UNCHANGED.")
print("Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak2 index.html")
