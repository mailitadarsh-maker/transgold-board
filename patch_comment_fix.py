c = open('index.html').read()
c = c.replace("// refresh every 1.5s (near-live)", "// refresh every 1s (near-live)")
open('index.html', 'w').write(c)
print("done")
