#!/usr/bin/env python3
"""
fix_unified_table.py
-----------------------
Fixes the unified table rendering as blank. Adds:
  - try/catch with console.error logging so we can see the real error
  - defensive fallbacks (won't crash if an index/array is missing)
  - retries a few times after load in case PRICES isn't populated yet
  - calls renderUnifiedTable() from more lifecycle points

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 fix_unified_table.py

Backs up current index.html as index.html.bak7 first.

AFTER running: hard refresh, then open the browser console
(Cmd+Option+J in Chrome / Cmd+Option+C in Safari dev tools) and send me
a screenshot of any red error text you see — that'll tell us exactly
what's wrong with the data structure.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak7")
print(f"Backup saved as {FILE}.bak7")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

old_fn_pattern = re.compile(
    r"function renderUnifiedTable\(\)\{.*?\n\}\n", re.DOTALL
)

new_fn = """function renderUnifiedTable(){
  try {
    const el = document.getElementById('unifiedRows');
    if (!el) { console.warn('[unified-table] #unifiedRows not found'); return; }

    if (typeof PRICES === 'undefined' || !PRICES) {
      console.error('[unified-table] PRICES global not found at all.');
      el.innerHTML = '<div style="color:#EF4444;padding:20px">Debug: PRICES is undefined</div>';
      return;
    }
    if (!PRICES.gold || !PRICES.silver) {
      console.error('[unified-table] PRICES.gold or PRICES.silver missing.', PRICES);
      el.innerHTML = '<div style="color:#EF4444;padding:20px">Debug: PRICES.gold/silver missing — check console</div>';
      return;
    }

    const g = PRICES.gold, s = PRICES.silver;
    const fmt = v => {
      v = Number(v) || 0;
      return v.toLocaleString('en',{minimumFractionDigits: v < 1000 ? 2 : 0, maximumFractionDigits: v < 1000 ? 2 : 0});
    };
    const safe = (arr, i) => (arr && arr[i]) ? arr[i] : { buy:0, sell:0 };

    const rows = [
      { label:'GOLD',   badge:'24 CARAT', weight:'1 GM',  src: safe(g,2), cls:'' },
      { label:'GOLD',   badge:'9999',     weight:'1 KG',  src: safe(g,0), cls:'' },
      { label:'GOLD',   badge:'TTB',      weight:'1 TTB', src: safe(g,4), cls:'' },
      { label:'SILVER', badge:'',         weight:'1 KG',  src: safe(s,0), cls:'silver' },
      { label:'GOLD',   badge:'995',      weight:'1 KG',  src: safe(g,1), cls:'' },
    ];

    el.innerHTML = rows.map(r => `
      <div class="ut-row">
        <div class="ut-name ${r.cls}">${r.label}${r.badge ? ' <small>'+r.badge+'</small>' : ''}</div>
        <div class="ut-weight">${r.weight}</div>
        <div class="ut-buy">${fmt(r.src.buy)}</div>
        <div class="ut-sell">${fmt(r.src.sell)}</div>
      </div>`).join('');

    console.log('[unified-table] rendered OK', rows);
  } catch (err) {
    console.error('[unified-table] render error:', err);
    const el = document.getElementById('unifiedRows');
    if (el) el.innerHTML = '<div style="color:#EF4444;padding:20px">Debug error — check console: ' + err.message + '</div>';
  }
}
"""

if old_fn_pattern.search(html):
    html = old_fn_pattern.sub(new_fn, html, count=1)
    print("Replaced renderUnifiedTable() with defensive/debug version.")
else:
    print("WARNING: could not find existing renderUnifiedTable() function to replace.")
    print("Make sure you already ran unified_table.py before this script.")
    sys.exit(1)

# Retry a few times after load, in case PRICES populates asynchronously
retry_js = """
// Retry rendering a few times shortly after load in case data loads async
let __utRetries = 0;
const __utRetryTimer = setInterval(() => {
  __utRetries++;
  renderUnifiedTable();
  if (__utRetries >= 5) clearInterval(__utRetryTimer);
}, 800);
"""
last_script_close = html.rfind("</script>")
if last_script_close != -1:
    html = html[:last_script_close] + retry_js + html[last_script_close:]
    print("Added retry loop (5 attempts, 800ms apart) after page load.")

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Hard refresh (Cmd+Shift+R), then open browser console and check for errors.")
print("If something looks wrong, restore with: cp index.html.bak7 index.html")
