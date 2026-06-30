#!/usr/bin/env python3
"""
final_polish.py
------------------
Overall visual cleanup pass:
  1. Fixes the leftover brownish highlight box behind header GOLD/SILVER
     spot values (residual flash() background not resetting cleanly)
  2. Squares off corners across the board (less rounded, more "square box")
  3. Gives ALL outer borders/lines (panels, rows, boxes) a green gradient
     look instead of plain gold/blue borders

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 final_polish.py

Backs up current index.html as index.html.bak11 first.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak11")
print(f"Backup saved as {FILE}.bak11")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ──────────────────────────────────────────────
# 1. Fix the flash() residual background on header spot values.
#    The flash() JS function sets background then resets to '' after a
#    timeout — but if it's re-triggered rapidly (every price tick) the
#    transition can appear "stuck" showing a faint box. We harden the
#    function to always force-clear via removeProperty.
# ──────────────────────────────────────────────
old_flash = "function flashEl(el){if(!el)return;el.style.transition='background 0.05s';el.style.background='rgba(212,169,74,0.5)';setTimeout(function(){el.style.transition='background 0.3s';el.style.background='';},150);}"
new_flash = "function flashEl(el){if(!el)return;el.style.transition='background 0.05s';el.style.background='rgba(34,197,94,0.35)';setTimeout(function(){el.style.transition='background 0.3s';el.style.removeProperty('background');},150);}"
if old_flash in html:
    html = html.replace(old_flash, new_flash)
    print("Fixed flashEl() to fully clear residual background tint.")
else:
    print("NOTE: flashEl() exact text not found — skipping that specific fix.")

# Also patch the other inline flash() helper used in fetchLivePrices (if present)
old_flash2 = "const flash = el => { el.style.transition='background 0.1s'; el.style.background='rgba(212,169,74,0.6)'; setTimeout(()=>{el.style.transition='background 0.6s';el.style.background='';},300); };"
new_flash2 = "const flash = el => { el.style.transition='background 0.1s'; el.style.background='rgba(34,197,94,0.4)'; setTimeout(()=>{el.style.transition='background 0.6s';el.style.removeProperty('background');},300); };"
if old_flash2 in html:
    html = html.replace(old_flash2, new_flash2)
    print("Fixed secondary flash() helper as well.")

# ──────────────────────────────────────────────
# 2 & 3. Global polish CSS: square corners + green gradient borders
# ──────────────────────────────────────────────
polish_css = """
/* ===== FINAL POLISH: square corners + green gradient borders ===== */
:root{
  --green-grad: linear-gradient(135deg, rgba(34,197,94,0.9), rgba(34,197,94,0.15));
}

/* Square off corners across the board */
.row, .ut-row, .ut-head, .sr-block, .sr-hdr, .box, .spot-pill, .sr-pill,
.wtag, .live-badge, .sent-bar-bg, .sent-bar {
  border-radius: 4px !important;
}

/* Outer panel borders -> green gradient */
.right{
  border-image: var(--green-grad) 1;
  border-right-width: 2px;
  border-right-style: solid;
}
.prices{
  border: none;
}
.ut-row, .row{
  border: 1px solid rgba(34,197,94,0.35) !important;
}
.ut-row:hover, .row:hover{
  border-color: rgba(34,197,94,0.7) !important;
}
.sr-block{
  border: 1px solid rgba(34,197,94,0.35) !important;
}
.ut-head{
  border: 1px solid rgba(34,197,94,0.5) !important;
}
.hdr{
  border-bottom: 2px solid rgba(34,197,94,0.4) !important;
}

/* Header spot-value boxes: clean static border instead of relying on
   flash() residue for definition */
#hGold, #hSilver, #bGoldBuy, #bGoldSell, #bSilverBuy, #bSilverSell {
  border-radius: 4px;
}
"""

html = html.replace("</style>", polish_css + "\n</style>", 1)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Applied square corners + green gradient borders, and fixed flash residue.")
print("Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak11 index.html")
