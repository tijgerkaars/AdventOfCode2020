import opcodes as o

inputs = ["Test_Input.txt","Input.txt"]
input = "AdventofCode2018\Day19\\" + inputs[1]

with open(input) as file:
    raw = []
    for line in file:
        raw.append(line.rstrip())

print(raw)

inpo = None
operations = []
for i,each in enumerate(raw):
    # find the instruction pointer
    if "#" in each:
        trash,inpo = each.split(" ")
        inpo = int(inpo)
    # find the operation specifications
    else:
        holder = each.split(" ")
        temp = []
        temp.append(holder[0])
        for j in range(1,len(holder)):
            temp.append(int(holder[j]))
        operations.append(temp)

print ("inpo:", inpo)
print("operations:", len(operations), operations)

reg = [0 for _ in range(6)]
reg[0] = 1
codes = o.opcodes()
counter = 0
archive = set()
while reg[inpo] < len(operations):
    instruction = reg[inpo]
    string = "ip=" + str(instruction) + " " + str(reg) + " "
    for each in operations[instruction]:
        string += str(each) + " "
    reg = codes.execute(operations[instruction],reg)
    string += str(reg)
    if string not in archive:
        archive.add(string)
    else:
        print("repeating")
        break
    if counter%100000 == 0:
        print (counter,string)
    reg[inpo] += 1
    counter +=1
    if counter >= 100000000:
        print(i, "reached counter")
        break
print (string)
print ("reg:", reg)
# 2223

# this can suck a monkey dick
#
# part 2
# not 0
