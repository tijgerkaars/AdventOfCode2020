with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day1\imput.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split(","))
print lines
temp = len(lines)
input = []
for i in range(temp):
    input.append(int(lines[i][0]))

freq = 0
archive = set()
archive.add(freq)
counter = -1
while not (str(freq) in archive) or counter == -1:
    if counter == -1:
        counter = 0
    archive.add(str(freq))
    freq = freq + input[counter]
    counter += 1
    print len(input), counter, freq
    if counter == len(input):
        counter = counter%len(input)
print freq
