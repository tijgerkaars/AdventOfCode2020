
from time import time


t0 = time()
for _ in range(10**6):
    exec('a=5')
print(time()-t0)


t0 = time()
for _ in range(10**6):
    a=5
print(time()-t0)