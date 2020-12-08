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
print hold, "\n", tests

operations = ["addr","addi", "mulr", "muli","banr", "bani", "borr", "bori", "setr", "seti", "gtir","gtri","gtrr", "eqir", "eqri", "eqrr"]


# test = [Registers Before, opcode, Registers After]
import opcodes as o

codex = o.opcodes(tests)

cases = 0
for each in tests:
    a,b,c = each
    if codex.try_all(a,b,c) >= 3:
        cases += 1

for keys in codex.codes:
    codex.codes[keys] = list(dict.fromkeys(codex.codes[keys]))
print codex.codes


def assign(dictionary):
    to_remove = []
    for keys in dictionary:
        if len(dictionary[keys]) == 1:
            to_remove.append(dictionary[keys][0])
    for each in to_remove:
        for keys in dictionary:
            if each in dictionary[keys] and len(dictionary[keys]) != 1:
                dictionary[keys].remove(each)
string = str(codex.codes)
new_string = ""

while string != new_string:
    string = str(codex.codes)
    assign(codex.codes)
    new_string = str(codex.codes)

print part_two


tests = part_two.split("\n")

operations = []
for operation in tests:
    parsed_op = operation.split(" ")
    print "operation:", parsed_op
    temp = []
    if len(parsed_op) == 4:
        for each in parsed_op:
            temp.append(int(each))
    if len(temp) == 4:
        operations.append(temp)

print operations
register = [0,0,0,0]






#
