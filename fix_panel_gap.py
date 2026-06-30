#!/usr/bin/env python3
"""
fix_panel_gap.py
-------------------
Fixes the awkward thin seam/line between the left Spot Rate panel and the
right Commodity table panel by adding proper spacing (gap + padding)
between them, instead of them touching edge-to-edge.

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 fix_panel_gap.py

Backs up current index.html as index.html.bak12 first.
"""
import shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak12")
print(f"Backup saved as {FILE}.bak12")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

gap_css = """
/* ===== FIX: proper spacing/gap between left and right panels ===== */
.body{gap:24px !important}
.right{
  border-right:none !important;
  margin-right:0;
  padding-right:8px;
}
.prices{
  padding-left:8px;
  border-left:none !important;
}
.ut-wrap{padding-left:0 !important}
/* Replace the harsh seam line with a soft green divider with breathing room */
.right::after{
  content:'';
  position:absolute;
  top:0; right:-12px; bottom:0;
  width:2px;
  background:linear-gradient(180deg, rgba(34,197,94,0.9), rgba(34,197,94,0.15));
}
.right{position:relative}
"""

html = html.replace("</style>", gap_css + "\n</style>", 1)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Added proper gap/spacing between panels, replaced seam with soft divider.")
print("Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak12 index.html")
