#!/usr/bin/env python3
"""
sr_header_colors.py
---------------------
Gives the GOLD and SILVER section headers a solid colored background again
(Gold = gold background, Silver = silver background), while keeping
"SPOT RATE" as plain text (no background).

Run from inside your project folder (after spotrate_textonly_headers.py):
    cd /Users/adarsh/transgold-board
    python3 sr_header_colors.py

Backs up current index.html as index.html.bak5 first.
"""
import shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak5")
print(f"Backup saved as {FILE}.bak5")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ──────────────────────────────────────────────
# Update .sr-hdr base + gold-hdr / silver-hdr to have solid backgrounds
# ──────────────────────────────────────────────
old_block = """.sr-hdr{background:none;color:var(--text);text-align:center;
  font-weight:800;font-size:16px;letter-spacing:.2em;padding:10px 0 6px;text-transform:uppercase}
.sr-hdr.gold-hdr{color:var(--gold)}
.sr-hdr.silver-hdr{color:var(--silver)}"""

new_block = """.sr-hdr{color:#fff;text-align:center;
  font-weight:800;font-size:15px;letter-spacing:.18em;padding:10px 0;text-transform:uppercase;border-radius:8px 8px 0 0}
.sr-hdr.gold-hdr{background:linear-gradient(90deg,var(--gold),#8a6a1f);color:#1a1505}
.sr-hdr.silver-hdr{background:linear-gradient(90deg,var(--silver),#7c8694);color:#15191f}"""

if old_block in html:
    html = html.replace(old_block, new_block)
    print("GOLD/SILVER header backgrounds restored.")
else:
    print("WARNING: expected .sr-hdr CSS block not found exactly — trying fallback patch.")
    # Fallback: try patching just the gold-hdr/silver-hdr rules if base header rule differs
    html = html.replace(
        ".sr-hdr.gold-hdr{color:var(--gold)}",
        ".sr-hdr.gold-hdr{background:linear-gradient(90deg,var(--gold),#8a6a1f);color:#1a1505;border-radius:8px 8px 0 0;padding:10px 0}"
    )
    html = html.replace(
        ".sr-hdr.silver-hdr{color:var(--silver)}",
        ".sr-hdr.silver-hdr{background:linear-gradient(90deg,var(--silver),#7c8694);color:#15191f;border-radius:8px 8px 0 0;padding:10px 0}"
    )

# Since sr-block padding/border might clip the new rounded header corners,
# make sure sr-block itself doesn't double-pad at top
html = html.replace(
    ".sr-body{padding:14px 16px}",
    ".sr-body{padding:14px 16px 16px}"
)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak5 index.html")
