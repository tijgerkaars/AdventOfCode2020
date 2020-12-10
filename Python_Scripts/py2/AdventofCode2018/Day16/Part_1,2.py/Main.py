with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day16\Input.txt") as file:
    lines = ""
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines += line
    lines = lines.split("\n\n\n")

part_one = lines[0]
part_two = lines[1]

tests = part_one.split("\n\n")
for i,each in enumerate(tests):
    temp = each.split("\n")
    temp[0] = (temp[0].split("Before: ")[1])
    temp[2] = temp[2].split("After:  ")[1]
    tests[i] = temp
hold = str(tests)
for i,test in enumerate(tests):
    exp = []
    for each in test:
        a = each.split(" ")
        temp = []
        for number in a:
            temp2 = ""
            for letter in number:
                if letter not in "[], ":
                    temp2 += letter
            temp.append(int(temp2))
        exp.append(temp)
    tests[i] = exp

operations = ["addr","addi", "mulr", "muli","banr", "bani", "borr", "bori", "setr", "seti", "gtir","gtri","gtrr", "eqir", "eqri", "eqrr"]


# test = [Registers Before, opcode, Registers After]
import opcodes as o

codex = o.opcodes(tests)

counter = 0
missed = []
succeded = []
for test in tests:
    o,a,b,c = test[1]
    matches = 0
    for operation in codex.operations:
        output = operation(test[0],a,b,c)
        if output == test[2]:
            if operation not in succeded:
                succeded.append(operation)
            matches += 1
    if matches >= 3:
        counter += 1

print counter
