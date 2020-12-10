
recipies = 51589
recipies = 01245
# recipies = 92510
# recipies = 59414
recipies = 580741

recipies = str(recipies)

score = '37'
elf1 = 0
elf2 = 1
while recipies not in score[-7:]:
    score += str(int(score[elf1]) + int(score[elf2]))
    elf1 = (elf1 + int(score[elf1]) + 1) % len(score)
    elf2 = (elf2 + int(score[elf2]) + 1) % len(score)

print('Part 1:', score[int(recipies):int(recipies)+10])
print('Part 2:', score.index(recipies))

fails = [1318132393,3181323935]
