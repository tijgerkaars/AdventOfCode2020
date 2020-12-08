def create_new_recipies(elf1,elf2):
    new_score = elf1 + elf2
    new_recipie = []
    new_score = str(new_score)
    for each in new_score:
        new_recipie.append(int(each))
    return new_recipie

#-------------------------------------
recipies = [3,7]
elf_1 = 0
elf_2 = 1
elves = [elf_1,elf_2]

goal = [5,1,5,8,9]
goal = [0,1,2,4,5]
# goal = [9,2,5,1,0]
# goal = [5,9,4,1,4]
goal = [5,8,0,7,4,1]

new_r = []
recipies += create_new_recipies(recipies[elves[0]],recipies[elves[1]])
counter = 0
while recipies[-len(goal):] != goal:
    if counter % 500000 == 0:
        print counter, goal,  recipies[-len(goal):]
    counter += 1
    for i in range(len(elves)):
        elves[i] += (1 + recipies[elves[i]])
        elves[i] %= len(recipies)
    recipies += create_new_recipies(recipies[elves[0]],recipies[elves[1]])
    if goal in recipies[-10:]:
        break
print recipies
print counter,  recipies[-len(goal):]
score = len(recipies) - len(goal)
print "score:", score

#580741

fails = [1318132393,3181323935]
