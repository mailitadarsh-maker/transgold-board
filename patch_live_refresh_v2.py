# index.html
c = open('index.html').read(); orig = c
c = c.replace(
    "const r = await fetch('prices.php?t=' + Date.now());",
    "const r = await fetch('api/live_price.php?t=' + Date.now());"
)
c = c.replace(
    "setInterval(fetchLivePrices, 8*1000); // refresh every 8s",
    "setInterval(fetchLivePrices, 1500); // refresh every 1.5s (near-live)"
)
print("index.html:", "patched" if c != orig else "WARNING no match")
open('index.html', 'w').write(c)

# admin.html
c = open('admin.html').read(); orig = c
c = c.replace(
    "const r = await fetch('/api/prices.php');",
    "const r = await fetch('/api/live_price.php');"
)
c = c.replace(
    "setInterval(fetchPrices, 10000);",
    "setInterval(fetchPrices, 1500);"
)
print("admin.html:", "patched" if c != orig else "WARNING no match")
open('admin.html', 'w').write(c)
