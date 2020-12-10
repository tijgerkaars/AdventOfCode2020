with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day2\input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split(","))
print lines
containsDoubles = 0
containsTriples = 0
# lines = [["abcdef"],["bababc"],["abbcde"],["abcccd"],["aabcdd"],["abcdee"],["ababab"]]
for i in range(len(lines)):
    lines[i] = lines[i][0]


for code in lines:
    archive = dict()
    noTripels = True
    noDoubles = True
    print code
    for letter in code:
        print letter
        if letter not in archive:
            archive[letter] = 1
        else:
            archive[letter] += 1
    print archive
    for each in archive:
        print each
        if archive[each] == 3 and noTripels:
            containsTriples += 1
            noTripels = False
        elif archive[each] == 2 and noDoubles:
            containsDoubles += 1
            noDoubles = False
        if not noDoubles and not noTripels:
            break
print containsDoubles
print containsTriples
print containsDoubles*containsTriples
