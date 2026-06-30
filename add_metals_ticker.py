#!/usr/bin/env python3
"""
add_metals_ticker.py
-----------------------
Adds a SECOND ticker-tape strip below your existing TradingView ticker,
showing other available metal prices (Platinum, Palladium, Copper) —
Gold and Silver are excluded since they're already shown in your
Spot Rate panel.

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 add_metals_ticker.py

Backs up current index.html as index.html.bak13 first.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak13")
print(f"Backup saved as {FILE}.bak13")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Find the existing TradingView ticker tape block using a robust regex
# that doesn't depend on exact whitespace/indentation.
pattern = re.compile(
    r'(<div style="height:46px;flex-shrink:0">.*?embed-widget-ticker-tape\.js"[^>]*>.*?</script>\s*</div>\s*</div>)',
    re.DOTALL
)
m = pattern.search(html)

if not m:
    print("WARNING: could not locate the existing ticker tape block via regex — aborting.")
    sys.exit(1)

insert_point = m.end()

metals_ticker_html = '''

<!-- Second ticker: other metals only (Gold/Silver excluded, shown elsewhere) -->
<div style="height:40px;flex-shrink:0;border-top:1px solid rgba(34,197,94,0.25)">
  <div class="tradingview-widget-container" style="height:40px">
    <div class="tradingview-widget-container__widget"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" async>
    {
      "symbols": [
        {"proName":"COMEX:PL1!","title":"Platinum"},
        {"proName":"COMEX:PA1!","title":"Palladium"},
        {"proName":"COMEX:HG1!","title":"Copper"}
      ],
      "showSymbolLogo": false,
      "isTransparent": true,
      "displayMode": "compact",
      "colorTheme": "dark",
      "locale": "en"
    }
    </script>
  </div>
</div>
'''

html = html[:insert_point] + metals_ticker_html + html[insert_point:]

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Added second metals-only ticker strip (Platinum, Palladium, Copper) below the existing one.")
print("Refresh your browser (hard refresh: Cmd+Shift+R) to see changes.")
print("If something looks wrong, restore with: cp index.html.bak13 index.html")
