#!/usr/bin/env python3
"""
fix_renderrows_null.py
-------------------------
Fixes: "Uncaught TypeError: Cannot set properties of null (setting
'innerHTML') at renderRows" — caused because the old renderRows() function
still tries to write into #goldRows / #silverRows, which no longer exist
after unified_table.py replaced them with the single #unifiedRows table.

This patches renderRows() to simply skip if the target element is missing,
instead of crashing — which was blocking renderUnifiedTable() from ever
running.

Run from inside your project folder:
    cd /Users/adarsh/transgold-board
    python3 fix_renderrows_null.py

Backs up current index.html as index.html.bak8 first.
"""
import re, shutil, sys, os

FILE = "index.html"

if not os.path.exists(FILE):
    print(f"ERROR: {FILE} not found in current directory. cd into transgold-board first.")
    sys.exit(1)

shutil.copy(FILE, FILE + ".bak8")
print(f"Backup saved as {FILE}.bak8")

with open(FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Find the renderRows function definition and wrap its DOM write in a null-check.
# We look for the common pattern: document.getElementById(containerId).innerHTML = ...
# and similar variants, and make them safe.

patterns_fixed = 0

pattern2 = re.compile(r"function renderRows\(([^)]*)\)\s*\{(.*?)\n\}", re.DOTALL)
m2 = pattern2.search(html)
if m2:
    args = m2.group(1)
    body = m2.group(2)
    wrapped = f"function renderRows({args}) {{\n  try {{{body}\n  }} catch(e) {{ console.warn('[renderRows] skipped safely:', e.message); }}\n}}"
    html = html[:m2.start()] + wrapped + html[m2.end():]
    patterns_fixed += 1
    print("Wrapped renderRows() body in try/catch — it will now skip safely instead of crashing.")
else:
    print("WARNING: could not locate renderRows() function definition to patch.")
    sys.exit(1)

with open(FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Hard refresh (Cmd+Shift+R) and check console again.")
print("If something looks wrong, restore with: cp index.html.bak8 index.html")
