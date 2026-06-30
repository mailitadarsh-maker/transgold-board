#!/usr/bin/env python3
"""
restyle_board.py
-----------------
Patches transgold-board/index.html:
  1. Swaps layout: Spot Rate panel -> LEFT (wider), Commodity table -> RIGHT
  2. Switches color theme to blue/gold (like Boonway Gold reference board)
  3. Adds a second logo slot in the header (next to existing logo)

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 restyle_board.py

It edits index.html directly. A backup is saved as index.html.bak first.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak")
print(f"Backup saved as {FILE}.bak")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ──────────────────────────────────────────────
# 1. THEME COLORS -> blue/gold (Boonway-style)
# ──────────────────────────────────────────────
html = html.replace(
    "--gold:#D4A94A;--gold-dim:#8A6A1F;",
    "--gold:#D8B45A;--gold-dim:#9C7A2A;"
)
html = html.replace(
    "--bg:#090909;--bg2:#0F0F0F;--bg3:#161616;",
    "--bg:#070B14;--bg2:#0C1626;--bg3:#13213A;"
)
html = html.replace(
    "--border-gold:rgba(212,169,74,0.18);",
    "--border-gold:rgba(216,180,90,0.25);\n  --blue:#3FA9E0;\n  --border-blue:rgba(63,169,224,0.35);"
)
html = html.replace(
    "--text:#F0EBE0;--muted:#6B6660;",
    "--text:#EAF3FB;--muted:#7C8BA0;"
)

# Row borders / buy-sell tiles -> blue accent instead of plain green/gold lines
html = html.replace(
    ".row{display:grid;grid-template-columns:1.6fr 130px 1fr 1fr;align-items:center;padding:14px 16px;background:var(--bg2);border:1px solid var(--border-green);border-radius:8px;margin-bottom:8px;position:relative;overflow:hidden;box-shadow:var(--glow);transition:border-color .2s,box-shadow .2s}",
    ".row{display:grid;grid-template-columns:1.6fr 130px 1fr 1fr;align-items:center;padding:16px 18px;background:var(--bg3);border:1px solid var(--border-blue);border-radius:10px;margin-bottom:10px;position:relative;overflow:hidden;transition:border-color .2s}"
)
html = html.replace(
    ".wtag{display:inline-flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;padding:8px 18px;border:2px solid var(--gold);border-radius:6px;color:var(--gold);letter-spacing:.1em;background:rgba(212,169,74,.1);min-width:100px}",
    ".wtag{display:inline-flex;align-items:center;justify-content:center;font-size:17px;font-weight:800;padding:9px 20px;border:2px solid var(--blue);border-radius:6px;color:var(--blue);letter-spacing:.1em;background:rgba(63,169,224,.12);min-width:104px}"
)

# ──────────────────────────────────────────────
# 2. LAYOUT SWAP — spot-rate panel left (wider), table right
#    Uses flex 'order' so we don't need to touch the HTML markup order.
# ──────────────────────────────────────────────
layout_css = """
/* ===== RESTYLE: swap panels, widen spot-rate side ===== */
.body{flex-direction:row}
.prices{order:2; flex:1.3}
.right{order:1; width:420px !important; border-left:none; border-right:2px solid var(--border-gold)}
@media(max-width:900px){
  .right{order:1; width:100% !important}
  .prices{order:2}
}
.box-title{color:var(--blue)}
.spot-pill.gpill{background:rgba(63,169,224,.15);color:var(--blue);border:1px solid rgba(63,169,224,.4)}
"""

html = html.replace("</style>", layout_css + "\n</style>", 1)

# ──────────────────────────────────────────────
# 3. SECOND LOGO SLOT in header (next to existing logo)
# ──────────────────────────────────────────────
old_logo_block = '''<div class="logo" onclick="window.location.href='/admin.html'" style="cursor:pointer">
    <img src="/logo.png" alt="Transgold Markets"
         onerror="this.style.display='none';document.getElementById('fallbackLogo').style.display='flex'">'''

new_logo_block = '''<div class="logo" onclick="window.location.href='/admin.html'" style="cursor:pointer;gap:18px;display:flex;align-items:center">
    <img src="/logo.png" alt="Transgold Markets" style="height:44px;width:auto"
         onerror="this.style.display='none';document.getElementById('fallbackLogo').style.display='flex'">
    <div style="width:1px;height:34px;background:var(--border-gold)"></div>
    <img src="/logo2.png" alt="Partner Logo" style="height:40px;width:auto"
         onerror="this.style.display='none'">'''

if old_logo_block in html:
    html = html.replace(old_logo_block, new_logo_block)
    print("Second logo slot added (will show /logo2.png if present).")
else:
    print("WARNING: could not find exact logo block to patch — header logo left unchanged.")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak index.html")
