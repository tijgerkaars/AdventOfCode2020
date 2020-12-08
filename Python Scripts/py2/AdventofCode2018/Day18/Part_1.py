import Periferals as p
inputs = ["Test_Input.txt","Input.txt", 'state_1.txt']
input = "AdventofCode2018\Day18\\" + inputs[1]
with open(input) as file:
    raw = []
    for line in file:
        raw.append(line.rstrip())
print (raw)

formated = p.format(raw)

print (formated)

forrest = p.forrest(formated)

# keep an archive of forrest arrangements
# if a arrangement has happend already, the forrest formation loops
archive = dict()
# part 2 long term bs
long_term = 1000000000
for i in range(long_term):
    # shows game of life type things
    print (forrest)
    forrest.update()
    # if this arrangement has not yet happend
    # archive it
    if str(forrest) not in archive:
        archive[str(forrest)] = [i]
    else:
        archive[str(forrest)].append(i)
        if len(archive[str(forrest)]) == 2:
            # determine in how many loops the state resets
            loop = archive[str(forrest)]
            # find the difference in minutes since a repeat happend
            loop = max(loop) - min(loop)
            # cut the time that already passed from the total time
            # Then determine the missmatch of the looping time with the total time
            #                     -1 because of the zero index
            #                     THIS FUCKED ME FOR SO LONG
            remainder = (long_term-1) - i
            for j in range(remainder%loop):
                i += j
                forrest.update()
            break
score = forrest.score()
end_score = score[1]*score[2]
print (forrest)

tried = [929628, 192765, 187000, 186238, 137255, 879450]
if end_score not in tried:
    print("New score:", end_score)
else:
    print("WE FOUND THAT ALREADY")

# [606, 634] first rep

# 137255 < answer < 879450
# not 929628, 192765, 187000, 186238
