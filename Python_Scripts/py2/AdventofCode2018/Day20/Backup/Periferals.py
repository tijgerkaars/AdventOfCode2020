class complex():
    def __init__(self,regex):
        print ("regex:", regex)
        self.nodes = dict()
        self.visited_nodes = set()
        self.starting_node = node((0,0), state = "X")
        self.add_node(self.starting_node)
        print("Building Map")
        self.build_map(regex,self.starting_node)


    def build_map(self,branches,current):

        branch, remainder = self.parse(branches, "(")

        for each in branch:
            if each == "$":
                print("done Building")
                return
            else:
                current = self.step(each, current)

        if remainder != None:
            remainders = self.parse(remainder,"|")
            for each in remainders:
                if each != None:
                    self.build_map(each,current)
        return

    def step(self, direction, current):
        if direction == "N":
            y,x = current.coord
            current = self.create_new_node((y-1,x),current)
            return current
        elif direction == "S":
            y,x = current.coord
            current = self.create_new_node((y+1,x),current)
            return current
        elif direction == "E":
            y,x = current.coord
            current = self.create_new_node((y,x+1),current)
            return current
        elif direction == "W":
            y,x = current.coord
            current = self.create_new_node((y,x-1),current)
            return current
        else:
            return current

    def create_new_node(self,coord,old_node):
        _y,_x = coord
        y,x = old_node.coord
        new_node = node(coord, state = ".")

        if _y < y:
            new_node.S = old_node
            old_node.N = new_node
            old_node.next.append(new_node)
        elif _y > y:
            new_node.N = old_node
            old_node.S = new_node
            old_node.next.append(new_node)
        elif _x < x:
            new_node.E = old_node
            old_node.W = new_node
            old_node.next.append(new_node)
        elif _x > x:
            new_node.W = old_node
            old_node.E = new_node
            old_node.next.append(new_node)
        self.add_node(new_node)
        return new_node

    def add_node(self,new_node):
        y,x = new_node.coord
        if y not in self.nodes:
            self.nodes[y] = dict()
        if x not in self.nodes[y]:
            self.nodes[y][x] = new_node


    def find_longest_path(self, current = None, last_node = None):

        if current == None:
            # only happens when the Function is first called
            current = self.starting_node
            current.steps = 0
        else:
            # in all other cases increment the step by 1
            current.steps = last_node.steps + 1
        # add the current node to an archive to prefent backtracking
        self.visited_nodes.add(current)
        # find all the neighbours, including those that have been visited already
        neighbours = current.find_neighbours()
        # remove already visited neighbours
        for each in reversed(neighbours):
            if each in self.visited_nodes:
                neighbours.remove(each)
        if neighbours != []:
            path_len = []
            for each in neighbours:
                path_len.append(self.find_longest_path(each, current))
            return max(path_len)
        else:
            return current.steps













    def clean_string(self,regex):
        counter = 0
        print (regex)
        start = 0
        old = regex
        new = ""
        while old != new:
            new = old
            for i in range(start + 1,len(old)):
                if old[i] == "E" and "W" == old[i-1]:
                    old = old[:i-1] +old[i+1:]
                    break
                elif old[i] == "W" and "E" == old[i-1]:
                    old = old[:i-1] +old[i+1:]
                    break
                elif old[i] == "S" and "N" == old[i-1]:
                    old = old[:i-1] +old[i+1:]
                    break
                elif old[i] == "N" and "S" == old[i-1]:
                    old = old[:i-1] +old[i+1:]
                    break
            start = i - 2
            print (old)
        new = ""
        temp = old.split("(|)")
        old = new
        print (temp)
        new = ""
        for each in temp:
            print ("each:", each)
            new += each
        print (new)

        return new



    def dd_to_ll(self):
        y_min,y_max,x_min,x_max = [0 for _ in range(4)]
        for y, value in self.nodes.items():
            y_min = min(y_min, y)
            y_max = max(y_max, y)
            for each in value.keys():
                x_min = min(x_min,each)
                x_max = max(x_max,each)
        y_range = abs(y_max-y_min) + 1
        x_range = abs(x_max-x_min) + 1
        ll = []
        for y in range(y_range):
            _y = y + y_min
            ll.append([])
            for x in range(x_range):
                _x = x + x_min
                if _y in self.nodes and _x in self.nodes[_y]:
                    ll[y].append(self.nodes[_y][_x])
                else:
                    ll[y].append(node(_y,_x, state = "#"))
        return ll

    def parse(self, regex,symbol):
        new_string = ""
        rest_string = ""
        for i,each in enumerate(regex):
            if each == symbol:
                new_string = regex[:i]
                if symbol == "(":
                    rest_string = regex[(i+1):len(regex)]
                elif symbol == "|":
                    rest_string = regex[(i+1):]
                break
        if new_string != "" and rest_string != None:
            return new_string, rest_string
        else:
            return regex, None

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
