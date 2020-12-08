with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day16\Input.txt") as file:
    lines = ""
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines += line
    lines = lines.split("\n\n\n")

part_one = lines[0]
part_two = lines[1]

# parse part 1
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

# parse part 2

part_two = part_two.split("\n")

new_parsed = []
for operation in part_two:
    _parsed = operation.split(" ")
    if len(_parsed) == 4:
        temp = []
        for each in _parsed:
            temp.append(int(each))
        new_parsed.append(temp)
part_two = new_parsed

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

print "part 1:", counter


dictionary = {}
for test in tests:
    o,a,b,c = test[1]
    matches = 0
    for operation in codex.operations:
        output = operation(test[0],a,b,c)
        if output == test[2]:
            if o not in dictionary:
                dictionary[o] = []
            dictionary[o].append(operation)

# remove doubles from lists
for key in dictionary:
    dictionary[key] = list(dict.fromkeys(dictionary[key]))


assigned = []
string = str(dictionary)
string_2 = ""

counter = 0

while string != string_2 or counter > 100:
    counter += 1
    string = str(dictionary)
    # for each of the numbers for operators
    for key in dictionary:
        # if that number has only one operation assigned to it
        if len(dictionary[key]) == 1:
            assigned.append(dictionary[key][0])
    for each in assigned:
        for key in dictionary:
            if len(dictionary[key]) != 1 and each in dictionary[key]:
                dictionary[key].remove(each)
    string_2 = str(dictionary)

for key in dictionary:
    dictionary[key] = dictionary[key][0]
    print key, dictionary[key]

register = [0,0,0,0]
print register

for each in part_two:
    o,a,b,c = each
    register = dictionary[o](register,a,b,c)
    print register










#
