#!/usr/bin/env python3
"""
Transgold Board — USD Spread Patch
Run this from inside your cloned repo root:
    python3 patch.py

It will patch: spread.json, prices.php, api/prices.php, admin.html, index.html
It makes a .bak backup of every file it touches before editing.
If a expected old_str isn't found in a file (because your local copy differs
from what was pasted into chat), that specific edit is SKIPPED and printed
clearly so nothing silently fails.
"""
import json, os, shutil, sys

def backup(path):
    if os.path.exists(path) and not os.path.exists(path + ".bak"):
        shutil.copy(path, path + ".bak")
        print(f"  [backup] {path} -> {path}.bak")

def replace_once(path, old, new, label):
    if not os.path.exists(path):
        print(f"  [SKIP] {path} not found.")
        return False
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if old not in content:
        print(f"  [SKIP] '{label}' marker not found in {path} — file may already be patched, or differs from expected. Check manually.")
        return False
    if content.count(old) > 1:
        print(f"  [WARN] '{label}' marker appears {content.count(old)} times in {path} — replacing FIRST occurrence only.")
    backup(path)
    content = content.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {label} patched in {path}")
    return True

def main():
    print("== Transgold USD Spread Patch ==\n")

    # ── 1. spread.json — full overwrite, preserves nothing custom, so confirm first
    sj_path = "spread.json"
    if os.path.exists(sj_path):
        with open(sj_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = {}
    else:
        data = {}
    data.setdefault("master", {"goldBid": 0, "goldAsk": 0, "silverBid": 0, "silverAsk": 0})
    data.setdefault("override", {"gold": [None]*5, "silver": [None]*2})
    if "usd" not in data:
        data["usd"] = {"goldBuy": 0, "goldSell": 0, "silverBuy": 0, "silverSell": 0}
        backup(sj_path)
        with open(sj_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"  [OK] usd block added to {sj_path}")
    else:
        print(f"  [SKIP] {sj_path} already has a 'usd' block.")

    print()

    # ── 2. prices.php
    old_prices_php = """if (file_exists($spreadFile)) {
    $spread = json_decode(file_get_contents($spreadFile), true);
    $json['spread'] = [
        'goldBid'   => $spread['goldBid']   ?? 0,
        'goldAsk'   => $spread['goldAsk']   ?? 0,
        'silverBid' => $spread['silverBid'] ?? 0,
        'silverAsk' => $spread['silverAsk'] ?? 0,
    ];
} else {
    $json['spread'] = ['goldBid'=>0,'goldAsk'=>0,'silverBid'=>0,'silverAsk'=>0];
}

echo json_encode($json);"""
    new_prices_php = """if (file_exists($spreadFile)) {
    $spread = json_decode(file_get_contents($spreadFile), true);
    $json['spread'] = [
        'goldBid'   => $spread['goldBid']   ?? 0,
        'goldAsk'   => $spread['goldAsk']   ?? 0,
        'silverBid' => $spread['silverBid'] ?? 0,
        'silverAsk' => $spread['silverAsk'] ?? 0,
    ];
    $json['usdSpread'] = [
        'goldBuy'    => $spread['usd']['goldBuy']    ?? 0,
        'goldSell'   => $spread['usd']['goldSell']   ?? 0,
        'silverBuy'  => $spread['usd']['silverBuy']  ?? 0,
        'silverSell' => $spread['usd']['silverSell'] ?? 0,
    ];
} else {
    $json['spread'] = ['goldBid'=>0,'goldAsk'=>0,'silverBid'=>0,'silverAsk'=>0];
    $json['usdSpread'] = ['goldBuy'=>0,'goldSell'=>0,'silverBuy'=>0,'silverSell'=>0];
}

echo json_encode($json);"""
    replace_once("prices.php", old_prices_php, new_prices_php, "prices.php usdSpread block")

    # ── 3. api/prices.php
    old_api_prices_php = """if (file_exists($spreadFile)) {
    $spread = json_decode(file_get_contents($spreadFile), true);
    $json['spread'] = [
        'goldBid'   => $spread['master']['goldBid']   ?? 0,
        'goldAsk'   => $spread['master']['goldAsk']   ?? 0,
        'silverBid' => $spread['master']['silverBid'] ?? 0,
        'silverAsk' => $spread['master']['silverAsk'] ?? 0,
    ];
} else {
    $json['spread'] = ['goldBid'=>0,'goldAsk'=>0,'silverBid'=>0,'silverAsk'=>0];
}

echo json_encode($json);"""
    new_api_prices_php = """if (file_exists($spreadFile)) {
    $spread = json_decode(file_get_contents($spreadFile), true);
    $json['spread'] = [
        'goldBid'   => $spread['master']['goldBid']   ?? 0,
        'goldAsk'   => $spread['master']['goldAsk']   ?? 0,
        'silverBid' => $spread['master']['silverBid'] ?? 0,
        'silverAsk' => $spread['master']['silverAsk'] ?? 0,
    ];
    $json['usdSpread'] = [
        'goldBuy'    => $spread['usd']['goldBuy']    ?? 0,
        'goldSell'   => $spread['usd']['goldSell']   ?? 0,
        'silverBuy'  => $spread['usd']['silverBuy']  ?? 0,
        'silverSell' => $spread['usd']['silverSell'] ?? 0,
    ];
} else {
    $json['spread'] = ['goldBid'=>0,'goldAsk'=>0,'silverBid'=>0,'silverAsk'=>0];
    $json['usdSpread'] = ['goldBuy'=>0,'goldSell'=>0,'silverBuy'=>0,'silverSell'=>0];
}

echo json_encode($json);"""
    replace_once("api/prices.php", old_api_prices_php, new_api_prices_php, "api/prices.php usdSpread block")

    print()

    # ── 4. admin.html — 5 edits
    a = "admin.html"

    replace_once(a,
        "let MASTER  = { goldBid:-5, goldAsk:5, silverBid:0, silverAsk:0 };",
        "let MASTER  = { goldBid:-5, goldAsk:5, silverBid:0, silverAsk:0 };\nlet USD_SPREAD = { goldBuy:0, goldSell:0, silverBuy:0, silverSell:0 };",
        "admin.html: USD_SPREAD state variable")

    old_save = """function saveSpread(){
  MASTER.goldBid   = parseFloat(document.getElementById('masterGoldBid').value)||0;
  MASTER.goldAsk   = parseFloat(document.getElementById('masterGoldAsk').value)||0;
  MASTER.silverBid = parseFloat(document.getElementById('masterSilverBid').value)||0;
  MASTER.silverAsk = parseFloat(document.getElementById('masterSilverAsk').value)||0;
  ['gold','silver'].forEach(type=>{
    const count = type==='gold'?5:2;
    for(let i=0;i<count;i++){
      const chk = document.getElementById('ovr_'+type+'_'+i);
      if(chk && chk.checked){
        OVERRIDE[type][i] = {
          bid: parseFloat(document.getElementById('ovrBid_'+type+'_'+i).value),
          ask: parseFloat(document.getElementById('ovrAsk_'+type+'_'+i).value)
        };
      } else { OVERRIDE[type][i] = null; }
    }
  });
  fetch('/save_spread.php',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({master:MASTER, override:OVERRIDE})
  }).then(r=>r.json()).then(d=>toast(d.ok?'✓ Saved — all devices updated':'⚠ Save failed','ok'))
    .catch(()=>toast('⚠ Could not reach server','err'));
}"""
    new_save = """function saveSpread(){
  MASTER.goldBid   = parseFloat(document.getElementById('masterGoldBid').value)||0;
  MASTER.goldAsk   = parseFloat(document.getElementById('masterGoldAsk').value)||0;
  MASTER.silverBid = parseFloat(document.getElementById('masterSilverBid').value)||0;
  MASTER.silverAsk = parseFloat(document.getElementById('masterSilverAsk').value)||0;
  USD_SPREAD.goldBuy    = parseFloat(document.getElementById('usdGoldBuy').value)||0;
  USD_SPREAD.goldSell   = parseFloat(document.getElementById('usdGoldSell').value)||0;
  USD_SPREAD.silverBuy  = parseFloat(document.getElementById('usdSilverBuy').value)||0;
  USD_SPREAD.silverSell = parseFloat(document.getElementById('usdSilverSell').value)||0;
  ['gold','silver'].forEach(type=>{
    const count = type==='gold'?5:2;
    for(let i=0;i<count;i++){
      const chk = document.getElementById('ovr_'+type+'_'+i);
      if(chk && chk.checked){
        OVERRIDE[type][i] = {
          bid: parseFloat(document.getElementById('ovrBid_'+type+'_'+i).value),
          ask: parseFloat(document.getElementById('ovrAsk_'+type+'_'+i).value)
        };
      } else { OVERRIDE[type][i] = null; }
    }
  });
  fetch('/save_spread.php',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({master:MASTER, override:OVERRIDE, usd:USD_SPREAD})
  }).then(r=>r.json()).then(d=>toast(d.ok?'✓ Saved — all devices updated':'⚠ Save failed','ok'))
    .catch(()=>toast('⚠ Could not reach server','err'));
}"""
    replace_once(a, old_save, new_save, "admin.html saveSpread() USD_SPREAD")

    old_load = """    if(d.master){
      MASTER = {...MASTER,...d.master};
      document.getElementById('masterGoldBid').value   = d.master.goldBid;
      document.getElementById('masterGoldAsk').value   = d.master.goldAsk;
      document.getElementById('masterSilverBid').value = d.master.silverBid;
      document.getElementById('masterSilverAsk').value = d.master.silverAsk;
    }"""
    new_load = """    if(d.master){
      MASTER = {...MASTER,...d.master};
      document.getElementById('masterGoldBid').value   = d.master.goldBid;
      document.getElementById('masterGoldAsk').value   = d.master.goldAsk;
      document.getElementById('masterSilverBid').value = d.master.silverBid;
      document.getElementById('masterSilverAsk').value = d.master.silverAsk;
    }
    if(d.usd){
      USD_SPREAD = {...USD_SPREAD, ...d.usd};
      document.getElementById('usdGoldBuy').value    = d.usd.goldBuy;
      document.getElementById('usdGoldSell').value   = d.usd.goldSell;
      document.getElementById('usdSilverBuy').value  = d.usd.silverBuy;
      document.getElementById('usdSilverSell').value = d.usd.silverSell;
    }"""
    replace_once(a, old_load, new_load, "admin.html loadSpread() USD_SPREAD")

    old_preview_end = """      if(pb) pb.textContent = fmt(mid+ask);
      if(ps) ps.textContent = fmt(mid+bid);
    }
  });
  updateDashboard();
}"""
    new_preview_end = """      if(pb) pb.textContent = fmt(mid+ask);
      if(ps) ps.textContent = fmt(mid+bid);
    }
  });
  const ugb = parseFloat(document.getElementById('usdGoldBuy')?.value)||0;
  const ugs = parseFloat(document.getElementById('usdGoldSell')?.value)||0;
  const usb = parseFloat(document.getElementById('usdSilverBuy')?.value)||0;
  const uss = parseFloat(document.getElementById('usdSilverSell')?.value)||0;
  const goldLine = document.getElementById('usdGoldLiveLine');
  const silverLine = document.getElementById('usdSilverLiveLine');
  if (goldLine) goldLine.innerHTML = `Live: $${spotUSD.gold.toFixed(2)} &nbsp;|&nbsp; Buy: $${(spotUSD.gold+ugb).toFixed(2)} &nbsp;|&nbsp; Sell: $${(spotUSD.gold+ugs).toFixed(2)}`;
  if (silverLine) silverLine.innerHTML = `Live: $${spotUSD.silver.toFixed(2)} &nbsp;|&nbsp; Buy: $${(spotUSD.silver+usb).toFixed(2)} &nbsp;|&nbsp; Sell: $${(spotUSD.silver+uss).toFixed(2)}`;
  updateDashboard();
}"""
    replace_once(a, old_preview_end, new_preview_end, "admin.html updatePreviews() USD live/spread line")

    old_media_page = """      <!-- ── MEDIA PAGE ── -->"""
    new_media_page = """      <div class="page" id="page-prices-usd-injected-marker" style="display:none"></div>
      <!-- ── MEDIA PAGE ── -->"""
    # Instead of guessing exact location of the prices page markup (we don't have
    # full HTML certainty), inject the USD spread card via JS at runtime instead —
    # safer than blind HTML insertion. See injected <script> block below.
    print("  [INFO] Skipping raw HTML card insertion (location uncertain) — using JS-injected card instead (see below).")

    # Inject a small bootstrap script right before </body> that builds the USD
    # spread card via JS and appends it into page-prices, so we don't need to
    # know exact HTML structure/line numbers.
    inject_marker = "<script>\nconst ADMIN_PASS = 'admin2024';"
    inject_html_js = """<script>
(function(){
  function buildUsdCard(){
    const page = document.getElementById('page-prices');
    if (!page || document.getElementById('usdSpreadCard')) return;
    const card = document.createElement('div');
    card.className = 'card';
    card.id = 'usdSpreadCard';
    card.innerHTML = `
      <div class="card-title">USD Spread (Direct $ Adjustment — independent of AED spread)</div>
      <div class="spread-grid">
        <div><div class="field-lbl">Gold Buy ($)</div><input type="number" step="0.01" class="field-input green" id="usdGoldBuy" value="0" oninput="updatePreviews()"></div>
        <div><div class="field-lbl">Gold Sell ($)</div><input type="number" step="0.01" class="field-input red-c" id="usdGoldSell" value="0" oninput="updatePreviews()"></div>
        <div><div class="field-lbl">Silver Buy ($)</div><input type="number" step="0.01" class="field-input green" id="usdSilverBuy" value="0" oninput="updatePreviews()"></div>
        <div><div class="field-lbl">Silver Sell ($)</div><input type="number" step="0.01" class="field-input red-c" id="usdSilverSell" value="0" oninput="updatePreviews()"></div>
      </div>
      <div class="hint">Adjusts the USD/oz live spot price directly. Used for the public board's USD price display. Separate from the AED commodity table spread above.</div>
      <div class="price-bar" style="margin-top:14px">
        <div class="price-box"><div class="price-box-lbl">Gold — Live vs Spread (USD)</div><div class="price-box-val" id="usdGoldLiveLine" style="font-size:14px;color:var(--text)">Live: — | Buy: — | Sell: —</div></div>
        <div class="price-box"><div class="price-box-lbl">Silver — Live vs Spread (USD)</div><div class="price-box-val" id="usdSilverLiveLine" style="font-size:14px;color:var(--text)">Live: — | Buy: — | Sell: —</div></div>
      </div>
      <div class="save-bar"><button class="btn btn-gold" onclick="saveSpread()">SAVE ALL SPREAD SETTINGS</button></div>`;
    page.appendChild(card);
  }
  document.addEventListener('DOMContentLoaded', function(){ setTimeout(buildUsdCard, 50); });
  if (document.readyState !== 'loading') setTimeout(buildUsdCard, 50);
})();
</script>
"""
    replace_once(a, inject_marker, inject_html_js + inject_marker, "admin.html USD spread card auto-injector")

    print()

    # ── 5. index.html — fetchLivePrices() patch
    ix = "index.html"
    old_fetch_block = """      const hg = document.getElementById('hGold');
      const hs = document.getElementById('hSilver');
      // Header shows spread-adjusted USD/oz (MASTER AED/gram → USD/oz)
      if (hg) hg.textContent = d.gold.toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2});
      if (hs) hs.textContent = d.silver.toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2});
      const gDiff = (d.gold - prevGold).toFixed(2);
      const sDiff = (d.silver - prevSilver).toFixed(2);"""
    new_fetch_block = """      const usp = d.usdSpread || {goldBuy:0,goldSell:0,silverBuy:0,silverSell:0};
      const goldBuyPrice    = d.gold   + (usp.goldBuy   || 0);
      const goldSellPrice   = d.gold   + (usp.goldSell  || 0);
      const silverBuyPrice  = d.silver + (usp.silverBuy || 0);
      const silverSellPrice = d.silver + (usp.silverSell|| 0);
      const hg = document.getElementById('hGold');
      const hs = document.getElementById('hSilver');
      // Header shows USD-spread-adjusted Buy price (public board never shows raw live price)
      if (hg) hg.textContent = goldBuyPrice.toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2});
      if (hs) hs.textContent = silverBuyPrice.toLocaleString('en',{minimumFractionDigits:2,maximumFractionDigits:2});
      const gDiff = (goldBuyPrice - prevGold).toFixed(2);
      const sDiff = (silverBuyPrice - prevSilver).toFixed(2);"""
    replace_once(ix, old_fetch_block, new_fetch_block, "index.html fetchLivePrices() header USD spread")

    old_anim = """      if (hg) { animateNumber(hg, d.gold, 2); glowPulse(hg, goldUp); }
      if (hs) { animateNumber(hs, d.silver, 2); glowPulse(hs, silverUp); }"""
    new_anim = """      if (hg) { animateNumber(hg, goldBuyPrice, 2); glowPulse(hg, goldUp); }
      if (hs) { animateNumber(hs, silverBuyPrice, 2); glowPulse(hs, silverUp); }"""
    replace_once(ix, old_anim, new_anim, "index.html header animateNumber() USD spread")

    old_sidebar = """      // Sidebar shows the clean USD/oz spot price — no AED spread applied here.
      // Spread (MASTER/override) only ever affects the AED commodity table via calcPrices().
      const gBuyUSD  = d.gold;
      const gSellUSD = d.gold;
      const sBuyUSD  = d.silver;
      const sSellUSD = d.silver;"""
    new_sidebar = """      // Sidebar shows USD-spread-adjusted Buy/Sell (separate from AED commodity table spread)
      const gBuyUSD  = goldBuyPrice;
      const gSellUSD = goldSellPrice;
      const sBuyUSD  = silverBuyPrice;
      const sSellUSD = silverSellPrice;"""
    replace_once(ix, old_sidebar, new_sidebar, "index.html sidebar USD spread Buy/Sell")

    print("\n== Patch run complete ==")
    print("Review the [OK]/[SKIP]/[WARN] lines above. If anything was SKIPPED,")
    print("that file differs from what was pasted into chat — tell me and paste")
    print("that section so I can fix the script.")
    print("\nNext steps:")
    print("  git add -A")
    print("  git commit -m 'Add USD spread (Buy/Sell) independent of AED spread'")
    print("  git push origin main")

if __name__ == '__main__':
    main()
