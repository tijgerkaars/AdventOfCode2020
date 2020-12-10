import Periferals as p

inputs = ["Test_Input.txt","Input.txt"]
input = "AdventofCode2018\Day20\\" + inputs[1]

with open(input) as file:
    raw = []
    for line in file:
        raw.append(line.rstrip())

regex = raw[0]


"""
print("regex:", regex)

complex = p.complex(regex)
print (complex)

print (complex.longest_path)


"""
def parse(regex):
    symbol = "("
    print("\nparse:", regex)

    path, branches = None, None
    for i,letter in enumerate(regex):
        if letter == "(" and regex[len(regex)-1] == ")":
            path, branches = (regex[:regex.index("(")], regex[regex.index("(")+1:len(regex)-1])
            print ("Here 1", path, " ", branches)
            break
        elif letter == "|" and regex[i+1] == ")" and regex[len(regex)-1] != ")":
            print ("Here 2")
            path = regex[:regex.index("(")]
            branches =  regex[regex.index("("):]
            loop, branch = branches[1:branches.index("|)")] , branches[branches.index("|)")+2:]
            loop = loop[:int(len(loop)/2)]
            return path, (loop,branch)
    if branches:
        for i,letter in enumerate(branches):
            if letter == "|" and branches[i+1] != ")" and branches[:i].count("(") == branches[:i].count(")"):
                branches = branches[:i], branches[i+1:]
                return path, branches
            elif letter == "|" and branches[i+1] != ")":
                branches = branches[:i], branches[i+1:]
                return path, branches
    else:
        return False
        pass




regex = regex[1:len(regex)-1]
path,branches = parse(regex)
print ("1:", path,branches)


#
