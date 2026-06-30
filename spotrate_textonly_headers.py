#!/usr/bin/env python3
"""
spotrate_textonly_headers.py
------------------------------
Removes the solid background bars on "SPOT RATE", "GOLD", "SILVER", and
"MARKET SENTIMENT" headers inside the spot-rate panel, turning them into
plain text labels instead:
  - "Spot Rate" -> plain gold text, no background
  - "Gold"      -> plain gold-colored text, no background
  - "Silver"    -> plain silver-colored text, no background
  - "Market Sentiment" -> plain text, no background

Run from inside your project folder (after spotrate_bigbox.py has already
been run):
    cd /Users/adarsh/transgold-board
    python3 spotrate_textonly_headers.py

Backs up current index.html as index.html.bak4 first.
"""
import shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak4")
print(f"Backup saved as {FILE}.bak4")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ──────────────────────────────────────────────
# Replace .sr-title (SPOT RATE bar) -> plain text
# ──────────────────────────────────────────────
old_sr_title = """.sr-title{background:linear-gradient(90deg,var(--gold),#8a6a1f);color:#1a1505;font-weight:800;
  font-size:15px;letter-spacing:.18em;text-align:center;padding:12px;border-radius:8px;text-transform:uppercase}"""
new_sr_title = """.sr-title{background:none;color:var(--gold);font-weight:800;
  font-size:18px;letter-spacing:.22em;text-align:center;padding:8px 0 4px;text-transform:uppercase;border-bottom:1px solid var(--border-gold)}"""
html = html.replace(old_sr_title, new_sr_title)

# ──────────────────────────────────────────────
# Replace .sr-hdr (GOLD / SILVER / MARKET SENTIMENT bars) -> plain text
# Gold = gold color, Silver = silver color (handled by added classes below)
# ──────────────────────────────────────────────
old_sr_hdr = """.sr-hdr{background:linear-gradient(90deg,#3FA9E0,#2C7AAE);color:#fff;text-align:center;
  font-weight:800;font-size:14px;letter-spacing:.16em;padding:8px;text-transform:uppercase}"""
new_sr_hdr = """.sr-hdr{background:none;color:var(--text);text-align:center;
  font-weight:800;font-size:16px;letter-spacing:.2em;padding:10px 0 6px;text-transform:uppercase}
.sr-hdr.gold-hdr{color:var(--gold)}
.sr-hdr.silver-hdr{color:var(--silver)}"""
html = html.replace(old_sr_hdr, new_sr_hdr)

# ──────────────────────────────────────────────
# sr-block: remove the boxed border/background look so it reads as plain
# sections rather than boxed cards (optional - keeps spacing only)
# ──────────────────────────────────────────────
old_sr_block = """.sr-block{border-radius:10px;overflow:hidden;border:1px solid var(--border-gold);background:var(--bg2)}"""
new_sr_block = """.sr-block{border-radius:10px;overflow:hidden;border:1px solid var(--border-gold);background:transparent}"""
html = html.replace(old_sr_block, new_sr_block)

# ──────────────────────────────────────────────
# Tag the GOLD / SILVER / MARKET SENTIMENT header divs with classes
# so the CSS above can color them correctly
# ──────────────────────────────────────────────
html = html.replace('<div class="sr-hdr">Gold</div>', '<div class="sr-hdr gold-hdr">Gold</div>')
html = html.replace('<div class="sr-hdr">Silver</div>', '<div class="sr-hdr silver-hdr">Silver</div>')
# Market Sentiment header stays neutral (var(--text)), no class needed

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Headers converted to plain colored text (no background bars).")
print("Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak4 index.html")
