from time import time

h,w = 100,100

array = [[i for i in range(w)] for _ in range(h)]

t0 = time()
for _ in range(1000):
    new_array = []
    for y,row in enumerate(array):
        new_array.append([])
        for x,square in enumerate(array):
            if x >= 0:
                new_array[y].append(square)
    array = new_array
print(time()-t0)

array2 = [row[:] for row in array]

t0 = time()
for _ in range(1000):
    for y,row in enumerate(array):
        for x,square in enumerate(array):
            if x >= 0:
                array2[y][x] = square
    t = array
    array = array2
    array2=t
print(time()-t0)
