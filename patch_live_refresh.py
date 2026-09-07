import re

for fname in ['index.html', 'admin.html']:
    with open(fname) as f:
        content = f.read()

    orig = content

    # point fetch at the new live endpoint instead of prices.php
    content = content.replace(
        "fetch('prices.php')" if fname == 'index.html' else "fetch('api/prices.php')",
        "fetch('api/live_price.php')"
    )

    # tighten the poll interval — adjust the literal number below to match
    # whatever fetchLivePrices() actually uses (8000 per your notes)
    content = content.replace("setInterval(fetchLivePrices, 8000)", "setInterval(fetchLivePrices, 1500)")

    if content == orig:
        print(f"WARNING: no changes made to {fname} — check the exact strings match")
    else:
        with open(fname, 'w') as f:
            f.write(content)
        print(f"Patched {fname}")
