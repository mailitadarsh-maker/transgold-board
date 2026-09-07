c = open('api/live_price.php').read(); orig = c
c = c.replace("$ttl = 2; // seconds", "$ttl = 1; // seconds")
print("live_price.php:", "patched" if c != orig else "WARNING no match")
open('api/live_price.php', 'w').write(c)
