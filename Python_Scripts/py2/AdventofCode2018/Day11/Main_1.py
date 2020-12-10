serial = 9995
serial = 8
size = [300,300]
cell_size_y = 3
cell_size_x = 3

def get_power(x,y):
    rack_id = 10 + x
    power_start = rack_id * y
    power = power_start + serial
    power = power * rack_id
    if power >= 100:
        s = str(power)
        power = int(s[-3])
    else:
        power = 0
    power -= 5
    return power

def get_grid(x,y):
    square_power = 0
    if y + cell_size_y <= size[1] and x + cell_size_x <= size[0]:
        for y1 in range(cell_size_y):
            y_coord = y + y1
            for x1 in range(cell_size_y):
                x_coord = x + x1
                square_power += get_power(x_coord,y_coord)
    return square_power


serial = 9995
print get_grid(297,1)

largest_grid = None
largest_power = 0

for y in range(1,size[1]+1 - cell_size_y):
    for x in range(1,size[0]+1 - cell_size_x):
        power = get_grid(x,y)
        if power > largest_power:
            largest_power = power
            largest_grid = (x,y)
        #print get_grid(x,y)

print largest_grid, largest_power

#--------------------------------------------------------------------------------------
# test cases
"""
serial = 8
print get_power(3,5)
serial = 57
print get_power(122,79)
serial = 39
print get_power(217,196)
serial = 71
print get_power(101,153)
serial = 42
print get_power(21,61)
"""
#--------------------------------------------------------------------------------------
