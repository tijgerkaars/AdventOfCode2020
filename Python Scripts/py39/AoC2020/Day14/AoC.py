#-*-coding:utf8;-*-
#qpy:3
#qpy:console



inp="""

"""

inp1="""
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
"""



def get_mask(mask):
    _,mask = mask.split(' = ')
    return {int(i):int(c) for i,c in enumerate(reversed(mask)) if c !='X'}
        
def set_bit(value, bit_index):
    return value | (1 << bit_index)

def clear_bit(value, bit_index):
    return value & ~(1 << bit_index)





command = [line for line in inp.strip().splitlines()]
# print(command)
mask = {}
mem  = {}
for instr in command:
    if 'mask' in instr:
        mask = get_mask(instr)
        continue
    index,write=instr.split('] = ')
    index = int(index[4:])
    write = int(write)
    # print(write, index)
    for mask_index,mask_value in mask.items():
        # print(repr(mask_index),repr(mask_value))
        if   mask_value == 1:
            write = set_bit(write, mask_index)
        elif mask_value == 0:
            write = clear_bit(write, mask_index)
        # print(write)
    mem[index] = write
print(sum(mem.values()))
print(17765746710228)





# ans < 17765746710288