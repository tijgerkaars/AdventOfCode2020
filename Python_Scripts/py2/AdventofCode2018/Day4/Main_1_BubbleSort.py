import csv

with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day4\input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split("."))
    for i in range(len(lines)):
        lines[i] = lines[i][0]
print lines

l = len(lines)
sorted = False
while not sorted:
    sorted = True
    for i in range(l):
        trash,time = lines[i].split("[")
        time,trash = time.split("]")
        if i+1 != len(lines):
            trash,time2 = lines[i+1].split("[")
            time2,trash = time2.split("]")
            if time2 < time:
                sorted = False
                temp = lines[i+1]
                lines[i+1] = lines[i]
                lines[i] = temp
print lines
for i in range(len(lines)):
    lines[i] = [lines[i]]


with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day4\sorted_input.csv", mode = 'w') as outfile:
    writer = csv.writer(outfile, delimiter = ",")
    for each in lines:
        writer.writerow(each)
