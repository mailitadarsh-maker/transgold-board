#!/usr/bin/env python3
"""
unified_table.py
------------------
Replaces the right-side price table with a SINGLE combined table showing
only these 5 rows, in this exact order (matching the reference photo):

  GOLD  24 CARAT   1 GM
  GOLD  9999       1 KG
  GOLD  TTB        1 TTB
  SILVER           1 KG
  GOLD  995        1 KG

Styled with a gold gradient header bar ("COMMODITY / WEIGHT / BUY AED /
SELL AED") and dark rows with blue value text, like the photo.

Reuses your existing price-calculation engine (PRICES.gold / PRICES.silver,
calcPrices(), MASTER, etc.) — only the rendering/display changes.

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 unified_table.py

Backs up current index.html as index.html.bak6 first.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak6")
print(f"Backup saved as {FILE}.bak6")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# ──────────────────────────────────────────────
# 1. CSS for the unified table (gold header bar + dark blue-text rows)
# ──────────────────────────────────────────────
unified_css = """
/* ===== UNIFIED TABLE — single 5-row board (photo reference) ===== */
.ut-wrap{flex:1;display:flex;flex-direction:column;padding:10px 0}
.ut-head{display:grid;grid-template-columns:1.6fr 1fr 1.1fr 1.1fr;
  background:linear-gradient(90deg,var(--gold),#9c7a2a);border-radius:8px;
  padding:14px 20px;margin-bottom:10px}
.ut-head span{font-weight:800;font-size:15px;letter-spacing:.12em;color:#1a1505;text-transform:uppercase}
.ut-head span small{font-size:10px;font-weight:700;opacity:.75;margin-left:4px}
.ut-row{display:grid;grid-template-columns:1.6fr 1fr 1.1fr 1.1fr;align-items:center;
  background:var(--bg3);border:1px solid var(--border-blue,rgba(63,169,224,.3));
  border-radius:8px;padding:16px 20px;margin-bottom:10px}
.ut-name{font-size:22px;font-weight:800;color:var(--text)}
.ut-name small{font-size:13px;font-weight:700;color:var(--gold);margin-left:8px}
.ut-name.silver small{color:var(--silver)}
.ut-weight{font-size:18px;font-weight:700;color:var(--blue,#3FA9E0)}
.ut-buy{font-size:22px;font-weight:800;color:var(--blue,#3FA9E0);font-variant-numeric:tabular-nums}
.ut-sell{font-size:22px;font-weight:800;color:var(--blue,#3FA9E0);font-variant-numeric:tabular-nums}
"""
html = html.replace("</style>", unified_css + "\n</style>", 1)

# ──────────────────────────────────────────────
# 2. Replace the .prices HTML block (two separate Gold/Silver tables)
#    with a single unified container
# ──────────────────────────────────────────────
prices_pattern = re.compile(r'<div class="prices">.*?</div>\s*(?=<div class="right")', re.DOTALL)

new_prices_html = '''<div class="prices ut-wrap">
    <div class="ut-head">
      <span>Commodity</span>
      <span>Weight</span>
      <span>Buy <small>AED</small></span>
      <span>Sell <small>AED</small></span>
    </div>
    <div id="unifiedRows"></div>
  </div>
  '''

if prices_pattern.search(html):
    html = prices_pattern.sub(new_prices_html, html, count=1)
    print("Replaced price table markup with unified single-table container.")
else:
    print("WARNING: could not find .prices block to replace — table structure may differ.")

# ──────────────────────────────────────────────
# 3. Inject JS that renders the 5 specific rows in the specified order,
#    reusing the existing PRICES.gold / PRICES.silver computed values.
#    Hooked to run every time calcPrices()+renderRows() would normally run.
# ──────────────────────────────────────────────
unified_js = """
// ── UNIFIED TABLE RENDERER (photo-matched 5-row board) ──────────────
function renderUnifiedTable(){
  const el = document.getElementById('unifiedRows');
  if (!el) return;
  // PRICES.gold index map: 0=9999, 1=995, 2=916, 3=999, 4=TTB
  // PRICES.silver index map: 0=1KG, 1=TTB
  const g = PRICES.gold, s = PRICES.silver;
  if (!g || !s || !g[0]) return;

  const fmt = v => v.toLocaleString('en',{minimumFractionDigits: v < 1000 ? 2 : 0, maximumFractionDigits: v < 1000 ? 2 : 0});

  const rows = [
    { label:'GOLD',   badge:'24 CARAT', weight:'1 GM',  buy:g[2].buy,  sell:g[2].sell, cls:'' },
    { label:'GOLD',   badge:'9999',     weight:'1 KG',  buy:g[0].buy,  sell:g[0].sell, cls:'' },
    { label:'GOLD',   badge:'TTB',      weight:'1 TTB', buy:g[4].buy,  sell:g[4].sell, cls:'' },
    { label:'SILVER', badge:'',         weight:'1 KG',  buy:s[0].buy,  sell:s[0].sell, cls:'silver' },
    { label:'GOLD',   badge:'995',      weight:'1 KG',  buy:g[1].buy,  sell:g[1].sell, cls:'' },
  ];

  el.innerHTML = rows.map(r => `
    <div class="ut-row">
      <div class="ut-name ${r.cls}">${r.label}${r.badge ? ' <small>'+r.badge+'</small>' : ''}</div>
      <div class="ut-weight">${r.weight}</div>
      <div class="ut-buy">${fmt(r.buy)}</div>
      <div class="ut-sell">${fmt(r.sell)}</div>
    </div>`).join('');
}
"""

# Insert the new function right before the closing </script> tag (last one in file)
last_script_close = html.rfind("</script>")
if last_script_close != -1:
    html = html[:last_script_close] + unified_js + "\nrenderUnifiedTable();\n" + html[last_script_close:]
    print("Injected renderUnifiedTable() and called it once on load.")
else:
    print("WARNING: could not find </script> tag to inject renderer JS.")

# ──────────────────────────────────────────────
# 4. Hook renderUnifiedTable() into the existing renderRows() calls so it
#    refreshes whenever live prices update (every 30s) or admin saves.
# ──────────────────────────────────────────────
html = html.replace(
    "renderRows(PRICES.gold,   'goldRows',   'gold');\n      renderRows(PRICES.silver, 'silverRows', 'silver');",
    "renderRows(PRICES.gold,   'goldRows',   'gold');\n      renderRows(PRICES.silver, 'silverRows', 'silver');\n      renderUnifiedTable();"
)
html = html.replace(
    "renderRows(PRICES.gold,'goldRows','gold');\nrenderRows(PRICES.silver,'silverRows','silver');",
    "renderRows(PRICES.gold,'goldRows','gold');\nrenderRows(PRICES.silver,'silverRows','silver');\nrenderUnifiedTable();"
)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak6 index.html")
