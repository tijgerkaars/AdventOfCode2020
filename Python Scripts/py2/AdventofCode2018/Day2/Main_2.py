with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day2\input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split(","))
    for i in range(len(lines)):
        lines[i] = lines[i][0]
print lines

holder_1 = lines[0]
holder_2 = lines[1]

print holder_1
print holder_2

def find_differences(str1,str2):
    dif = 0
    if len(str1) != len(str2):
        print "strings not compatible"
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            dif += 1
    str = ""
    if dif == 1:
        for i in range(len(str1)):
            if str1[i] == str2[i]:
                str += str1[i]
        return [dif,str]
    return [dif]


print find_differences(holder_1,holder_2)

codes = []

for i in range(len(lines)):
    if i == len(lines):
        break
    for j in range(i+1,len(lines)):
        if find_differences(lines[i],lines[j])[0] == 1:
            codes.append([(i,j),find_differences(lines[i],lines[j])])

print codes
