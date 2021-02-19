
test = 0
f = f'test_{test}_' if test else '' + 'input'

with open(rf'Python Scripts\py39\AoC2020\Day6\{f}.txt') as f:
    groups = [[ans for ans in group.splitlines()] for group in f.read().split('\n\n')]
    print(groups)


def part_1(groups):
    groups_answers = []
    for group in groups:
        groups_answers.append( 
            set(each for ans in group for each in ans)
            )
    return sum(map(len, groups_answers))

def part_2(groups):
    groups_answers = []
    for group in groups:
        sets = [set(each) for each in group]
        print(sets)
        combined = sets[0]
        for each in sets:
            combined &= each
        groups_answers.append(combined)
    return sum(map(len, groups_answers))


if __name__ == "__main__":
    print( part_1(groups) )
    print( part_2(groups) )