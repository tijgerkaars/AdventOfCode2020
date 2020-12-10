



d = {i:{j:[] for j in range(4)} for i in range(5)}
d={}


excep = [0,0]

for y in range(5):
    for x in range(5):
        data = y*x
        try:
            d[y][x].append(data)
        except:
            try:
                d[y][x] = [data]
            except:
                d[y] = {x:[data]}

print(d)