serial = 9995
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

def get_grid_from_cells(x,y):
    square_power = 0
    if y + cell_size_y < size[1] and x + cell_size_x <= size[0]:
        for y1 in range(1,cell_size_y +1):
            y_coord = y + y1
            for x1 in range(1,cell_size_x +1):
                x_coord = x + x1
                square_power += cells[(x_coord,y_coord)]
    return square_power


cells = dict()
serial = 9995

for y in range(size[1]):
    for x in range(size[0]):
        cells[(x+1,y+1)] = get_power(x+1,y+1)


largest_grid = None
largest_power = 0
largest_size = 3


for i in range(3,size[0]+1):
    cell_size_y = i
    cell_size_x = i
    for y in range(size[1] - cell_size_y+1):
        for x in range(size[0] - cell_size_x+1):
            power = get_grid_from_cells(x,y)
            if power > largest_power:
                largest_power = power
                largest_grid = (x+1,y+1)
                largest_size = i
    print i, "best:", largest_size, largest_grid, largest_power

print largest_size, largest_grid, largest_power

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
