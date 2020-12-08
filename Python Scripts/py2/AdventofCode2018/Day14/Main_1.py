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

new_r = []
recipies += create_new_recipies(recipies[elves[0]],recipies[elves[1]])
while len(recipies) < 580741+12:
    for i in range(len(elves)):
        elves[i] += (1 + recipies[elves[i]])
        elves[i] %= len(recipies)
    recipies += create_new_recipies(recipies[elves[0]],recipies[elves[1]])

score = recipies[580741:]
print score
score = score[:10]
print score

string = ""
for i in range(10):
    string += str(score[i])
print string

#580741

fails = [1318132393,3181323935]
