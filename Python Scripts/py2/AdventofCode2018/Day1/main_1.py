with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day1\imput.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split(","))
print lines
temp = len(lines)
input = []
for i in range(temp):
    print int(lines[i][0])
    input.append(int(lines[i][0]))
print input

freq = 0
for each in input:
    freq += each
print freq
