d = dict()

d[(1,3)] = 0
d[(2,1)] = 0
d[(1,4)] = 0
d[(3,1000)] = 0

l = d.keys()
print l
l.sort()

print l
l.remove((1,3))
print l
print dir(l)
