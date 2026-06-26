#!/usr/bin/env python3
"""
patch.py — surgically edits index.html without rewriting the whole file.
Usage:
  python3 patch.py --password admin123   # change admin password
  python3 patch.py --apply               # apply all patches to index.html
"""

import re, sys, argparse

FILE = 'index.html'

def read():
    with open(FILE, encoding='utf-8') as f:
        return f.read()

def write(html):
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'✅  Saved {FILE}')

# ── PATCH 1: Add password protection to openAdmin() ─────────────────────────
def patch_password(html, password='admin2024'):
    old = 'function openAdmin(){'
    new = f'''function openAdmin(){{
  const pw=prompt('Enter admin password:');
  if(pw!=='{password}'){{toast('Wrong password','err');return;}}'''
    if old not in html:
        print('⚠️  openAdmin already patched or not found — skipping')
        return html
    return html.replace(old, new, 1)

# ── PATCH 2: Change a specific price value ──────────────────────────────────
def patch_price(html, metal, row, field, value):
    """metal='gold'|'silver', row=0-based index, field='buy'|'sell', value=float"""
    pattern = re.compile(
        r'(const PRICES\s*=\s*\{.*?"' + metal + r'"\s*:\s*\[)(.*?)(\])',
        re.DOTALL
    )
    m = pattern.search(html)
    if not m:
        print(f'⚠️  Could not find PRICES.{metal}'); return html
    block = m.group(2)
    rows = re.findall(r'\{[^}]+\}', block)
    if row >= len(rows):
        print(f'⚠️  Row {row} not found in {metal}'); return html
    updated_row = re.sub(
        rf'"{field}"\s*:\s*[\d.]+',
        f'"{field}":{value:.2f}',
        rows[row]
    )
    rows[row] = updated_row
    new_block = m.group(1) + ','.join(rows) + m.group(3)
    return pattern.sub(new_block, html, count=1)

# ── CLI ──────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description='Patch index.html')
    p.add_argument('--password', help='Set admin password (default: admin2024)')
    p.add_argument('--metal',    help='gold or silver')
    p.add_argument('--row',      type=int, help='Row index (0-based)')
    p.add_argument('--field',    help='buy or sell')
    p.add_argument('--value',    type=float, help='New price value')
    p.add_argument('--list',     action='store_true', help='List current prices')
    args = p.parse_args()

    html = read()

    # List prices
    if args.list:
        m = re.search(r'const PRICES\s*=\s*(\{.*?\}\s*\})', html, re.DOTALL)
        if m:
            import json
            try:
                data = json.loads(m.group(1))
                for metal, rows in data.items():
                    print(f'\n  {metal.upper()}')
                    print(f'  {"#":<4} {"ITEM":<28} {"BUY":>12} {"SELL":>12}')
                    print('  ' + '─'*58)
                    for i,r in enumerate(rows):
                        item = f'{r["purity"]} · {r["weight"]}'
                        print(f'  {i+1:<4} {item:<28} {r["buy"]:>12,.2f} {r["sell"]:>12,.2f}')
            except: print('Could not parse prices')
        return

    changed = False

    if args.password:
        html = patch_password(html, args.password)
        print(f'🔑  Password set to: {args.password}')
        changed = True

    if args.metal and args.row is not None and args.field and args.value is not None:
        html = patch_price(html, args.metal, args.row - 1, args.field, args.value)
        print(f'💰  {args.metal} row {args.row} {args.field} → {args.value}')
        changed = True

    if not changed:
        print('No changes specified. Use --help to see options.')
        return

    write(html)

if __name__ == '__main__':
    main()
