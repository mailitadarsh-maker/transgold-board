#!/usr/bin/env python3
"""
spotrate_bigbox.py
-------------------
Restyles the left-side Spot Rate panel to look like the reference board:
  - Big "SPOT RATE" gold title bar
  - "GOLD" / "SILVER" blue section headers
  - BUY OZ / SELL OZ pill labels
  - Large green/blue value pills
  - Low / High badges underneath

Keeps the SAME element IDs (bGoldBuy, bGoldSell, bSilverBuy, bSilverSell,
bGoldChg, bSilverChg) so your existing live-price JS keeps working with
zero changes.

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 spotrate_bigbox.py

Backs up current index.html as index.html.bak3 first.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak3")
print(f"Backup saved as {FILE}.bak3")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ──────────────────────────────────────────────
# 1. Widen the left panel further to fit the bigger boxes
# ──────────────────────────────────────────────
html = html.replace(
    '.right{order:1; width:420px !important; border-left:none; border-right:2px solid var(--border-gold)}',
    '.right{order:1; width:480px !important; border-left:none; border-right:2px solid var(--border-gold)}'
)

# ──────────────────────────────────────────────
# 2. New CSS for the big spot-rate boxes
# ──────────────────────────────────────────────
spotrate_css = """
/* ===== SPOT RATE — big box style (Boonway reference) ===== */
.sr-wrap{padding:14px 16px;display:flex;flex-direction:column;gap:14px;flex:1;overflow-y:auto}
.sr-title{background:linear-gradient(90deg,var(--gold),#8a6a1f);color:#1a1505;font-weight:800;
  font-size:15px;letter-spacing:.18em;text-align:center;padding:12px;border-radius:8px;text-transform:uppercase}
.sr-block{border-radius:10px;overflow:hidden;border:1px solid var(--border-gold);background:var(--bg2)}
.sr-hdr{background:linear-gradient(90deg,#3FA9E0,#2C7AAE);color:#fff;text-align:center;
  font-weight:800;font-size:14px;letter-spacing:.16em;padding:8px;text-transform:uppercase}
.sr-body{padding:14px 16px}
.sr-cols{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:8px}
.sr-lbl{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:700;color:var(--gold);margin-bottom:6px}
.sr-lbl .dollar{background:var(--gold);color:#1a1505;width:20px;height:20px;border-radius:5px;
  display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800}
.sr-pill{background:linear-gradient(180deg,#2EBE6E,#1FA85C);color:#fff;font-weight:800;
  font-size:clamp(22px,3vw,30px);text-align:center;padding:10px 6px;border-radius:8px;font-variant-numeric:tabular-nums}
.sr-hilo{display:flex;justify-content:space-between;align-items:center;margin-top:8px;gap:8px}
.sr-tag{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;color:var(--text)}
.sr-tag .badge{font-size:11px;font-weight:800;padding:4px 10px;border-radius:5px;color:#fff}
.sr-tag .low{background:#D64545}
.sr-tag .high{background:#2EBE6E}
"""

html = html.replace("</style>", spotrate_css + "\n</style>", 1)

# ──────────────────────────────────────────────
# 3. Replace the .boxes HTML block with the new structure
#    (keeps the original Gold/Silver/Sentiment boxes, same IDs)
# ──────────────────────────────────────────────
old_boxes_pattern = re.compile(r'<div class="boxes">.*?</div>\s*</div>\s*</div>', re.DOTALL)

new_boxes_html = '''<div class="sr-wrap">
      <div class="sr-title">Spot Rate</div>

      <div class="sr-block">
        <div class="sr-hdr">Gold</div>
        <div class="sr-body">
          <div class="sr-cols">
            <div>
              <div class="sr-lbl"><span class="dollar">$</span>Buy OZ</div>
              <div class="sr-pill" id="bGoldBuy">4,046.73</div>
            </div>
            <div>
              <div class="sr-lbl"><span class="dollar">$</span>Sell OZ</div>
              <div class="sr-pill" id="bGoldSell">4,047.73</div>
            </div>
          </div>
          <div class="sr-hilo">
            <div class="sr-tag"><span class="badge low">Low</span><span id="bGoldLow">4,000.09</span></div>
            <div class="sr-tag"><span class="badge high">High</span><span id="bGoldHigh">4,086.52</span></div>
          </div>
          <div class="chg-line up" id="bGoldChg" style="margin-top:8px;text-align:center">&#9650; 1.55</div>
        </div>
      </div>

      <div class="sr-block">
        <div class="sr-hdr">Silver</div>
        <div class="sr-body">
          <div class="sr-cols">
            <div>
              <div class="sr-lbl"><span class="dollar">$</span>Buy OZ</div>
              <div class="sr-pill" id="bSilverBuy">58.08</div>
            </div>
            <div>
              <div class="sr-lbl"><span class="dollar">$</span>Sell OZ</div>
              <div class="sr-pill" id="bSilverSell">58.11</div>
            </div>
          </div>
          <div class="sr-hilo">
            <div class="sr-tag"><span class="badge low">Low</span><span id="bSilverLow">57.41</span></div>
            <div class="sr-tag"><span class="badge high">High</span><span id="bSilverHigh">59.49</span></div>
          </div>
          <div class="chg-line up" id="bSilverChg" style="margin-top:8px;text-align:center">&#9650; 0.03</div>
        </div>
      </div>

      <div class="sr-block">
        <div class="sr-hdr">Market Sentiment</div>
        <div class="sr-body">
          <div class="sent-bar-bg"><div class="sent-bar" id="sentBar" style="width:65%"></div></div>
          <div class="sent-lbls" style="margin-top:8px"><span class="b" id="sentBuyers">BUYERS 65%</span><span class="s" id="sentSellers">SELLERS 35%</span></div>
        </div>
      </div>
    </div>
  </div>
</div>'''

if old_boxes_pattern.search(html):
    html = old_boxes_pattern.sub(new_boxes_html, html, count=1)
    print("Spot-rate panel restyled to big-box layout.")
else:
    print("WARNING: could not find .boxes block to replace — structure may differ from expected.")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak3 index.html")
