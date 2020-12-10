class complex():
    def __init__ (self, regex):
        regex = regex[1:]
        self.regex = regex[:len(regex)-1]
        self.nodes = dict()
        self.starting_node = node((0,0), state = "X", steps = 0)
        self.nodes[(0,0)] = self.starting_node

        self.longest_path = 0
        self.shortest_path = len(regex)

        self.build(self.regex,self.starting_node)

    def build(self,regex,current_node):
        # test breaking appart
        print ("og", regex)

        if "|" in regex:
            path,branches = (self.parse(regex))
            current_node = self.steps(path,current_node)
            print ("branches:", branches)
            for each in branches:
                self.build(each,current_node)
        else:
            current_node = self.steps(regex,current_node)
            print (current_node.steps)
            self.longest_path = max(self.longest_path,current_node.steps)
            self.shortest_path = min(self.shortest_path,current_node.steps)





    def steps(self,path,starting_node):
        current = starting_node
        traveled = ""
        for direction in path:
            traveled += direction
            current = self.next_node(direction,current)
        return current


    def next_node(self,direction,current_node):
        y,x = current_node.coord
        print (current_node.coord, direction)
        if direction == "N":
            if (y-1,x) not in self.nodes:
                new_node = node((y-1,x),steps = current_node.steps + 1, state = ".")
                current_node.next = new_node
                current_node.N = new_node
                new_node.S = current_node
                self.nodes[(y-1,x)] = new_node
                return new_node
            else:
                current_node.next = self.nodes[(y-1,x)]
                return self.nodes[(y-1,x)]
        elif direction == "S":
            if (y+1,x) not in self.nodes:
                new_node = node((y+1,x),steps = current_node.steps + 1, state = ".")
                current_node.next = new_node
                current_node.S = new_node
                new_node.N = current_node
                self.nodes[(y+1,x)] = new_node
                return new_node
            else:
                current_node.next = self.nodes[(y+1,x)]
                return self.nodes[(y+1,x)]
        elif direction == "E":
            if (y,x+1) not in self.nodes:
                new_node = node((y,x+1),steps = current_node.steps + 1, state = ".")
                current_node.next = new_node
                current_node.E = new_node
                new_node.W = current_node
                self.nodes[(y,x+1)] = new_node
                return new_node
            else:
                current_node.next = self.nodes[(y,x-1)]
                return self.nodes[(y,x-1)]
        elif direction == "W":
            if (y,x-1) not in self.nodes:
                new_node = node((y,x-1),steps = current_node.steps + 1, state = ".")
                current_node.next = new_node
                current_node.W = new_node
                new_node.E = current_node
                self.nodes[(y,x-1)] = new_node
                return new_node
            else:
                current_node.next = self.nodes[(y,x-1)]
                return self.nodes[(y,x-1)]
        pass












    def dd_to_ll(self):
        y_range,x_range = [],[]
        for coord, value in self.nodes.items():
            y_range.append(coord[0])
            x_range.append(coord[1])

        y_min,y_max = min(y_range), max(y_range)
        x_min,x_max = min(x_range), max(x_range)

        y_range = abs(y_max-y_min) + 1
        x_range = abs(x_max-x_min) + 1

        ll = []
        for y in range(y_range):
            _y = y + y_min
            ll.append([])
            for x in range(x_range):
                _x = x + x_min
                if (_y,_x) in self.nodes:
                    ll[y].append(self.nodes[(_y,_x)])
                else:
                    ll[y].append(node((_y,_x), state = "#"))
        return ll

    def __str__(self):
        ll = self.dd_to_ll()
        string = ""
        for y,row in enumerate(ll):
            row1 = "#"
            row2 = "#"
            row3 = "#"
            for x,tile in enumerate(row):
                cube = ll[y][x]

                if cube.state == "#":
                        row1, row2, row3 = row1 + "##", row2 + "##", row3 + "##"
                else:
                    if cube.S == None:
                        row1, row2, row3 = row1 + "#", row2 + str(cube), row3 + "#"
                    else:
                        row1, row2, row3 = row1 + "#", row2 + str(cube), row3 + "-"
                    if cube.E == None:
                        row1, row2, row3 = row1 + "#", row2 + "#", row3 + "#"
                    else:
                        row1, row2, row3 = row1 + "#", row2 + "|", row3 + "#"
            string += row2 + "\n" + row3 + "\n"

        return row3 + "\n" + string

    def parse(self,regex):
        symbol = "("
        print("\nparse:", regex)

        path, branches = None, None
        for i,letter in enumerate(regex):
            if letter == "(" and regex[len(regex)-1] == ")":
                path, branches = (regex[:regex.index("(")], regex[regex.index("(")+1:len(regex)-1])
                break
            elif letter == "|" and regex[i+1] == ")" and regex[len(regex)-1] != ")":
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
        else:
            return False
            pass

class node():
    def __init__(self,coord, steps = None, state = None):
        self.coord = coord
        self.next = []
        self.state = state
        self.N = None
        self.E = None
        self.S = None
        self.W = None

        self.steps = steps

    def find_neighbours(self):
        neighbours = [
        self.N,
        self.E,
        self.S,
        self.W
        ]
        for each in reversed(neighbours):
            if each == None:
                neighbours.remove(each)
        return neighbours


    def __str__(self):
        return self.state
