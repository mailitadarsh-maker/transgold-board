# index.html
c = open('index.html').read(); orig = c
c = c.replace("setInterval(fetchLivePrices, 1500);", "setInterval(fetchLivePrices, 1000);")
print("index.html:", "patched" if c != orig else "WARNING no match")
open('index.html', 'w').write(c)

# admin.html
c = open('admin.html').read(); orig = c
c = c.replace("setInterval(fetchPrices, 1500);", "setInterval(fetchPrices, 1000);")
print("admin.html:", "patched" if c != orig else "WARNING no match")
open('admin.html', 'w').write(c)
