import Periferals as p
import Functions  as f

inputs = ["Test_Input.txt","Input.txt"]
input = "AdventofCode2018\Day20\\" + inputs[0]

with open(input) as file:
    raw = []
    for line in file:
        raw.append(line.rstrip())

print("raw:", raw)

regex = raw[3]

complex_map = p.complex(regex)
result = complex_map.find_longest_path()
print ("result", result)
print (complex_map)


"""
    def build_map(self):
        current = self.starting_node
        branch = self.start
        for each in branch:
            if each == "$":
                print("done Building")
                return
            else:
                current = self.step(each, current)

    def step(self, direction, current):
        if direction == "N":
            y,x = current.coord
            return self.create_new_node((y-1,x),current)
        elif direction == "S":
            y,x = current.coord
            return self.create_new_node((y+1,x),current)
        elif direction == "E":
            y,x = current.coord
            return self.create_new_node((y,x+1),current)
        elif direction == "W":
            y,x = current.coord
            return self.create_new_node((y,x-1),current)






###########
#.|.#.|.#.#
#-###-#-#-#
#.|.|.#.#.#
#-#####-#-#
#.#.#X|.#.#
#-#-#####-#
#.#.|.|.|.#
#-###-###-#
#.|.|.#.|.#
###########










"""
