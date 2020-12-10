k = [0]

b = dict()
b["a"] = dict()
b["c"] = dict()

b["a"]["d"] = k
b["c"]["e"] = k

print b

k[0] += 1

print b
