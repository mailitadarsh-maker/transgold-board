content = open('api/live_price.php').read()
orig = content

content = content.replace(
    "https://api.goldvaultapp.example/latest",
    "https://metalprice.goldvaultapp.com/getprice/XAUUSD"  # placeholder, real merge logic still pending prices.php shape
)

if content == orig:
    print("WARNING: placeholder URL not found, check file contents")
else:
    open('api/live_price.php', 'w').write(content)
    print("Patched endpoint URL")
