#---------------------------------------------------------------------------
# implents a linked list
class node:
    def __init__(self,data = None):
        self.data = data
        self.next = None
        self.previous = None
    def prev(self):
        return self.previous

class linked_list:
    def __init__(self):
        self.head = node()
        self.head.data = "head"
        self.tail = node()
        self.tail.data = "tail"
        self.tail.next = self.head
        self.head.previous = self.tail
        self.current = self.tail
        self.size = 0

    def append(self,data):
        new_node = node(data)
        while self.current.next != None:
            self.current = self.current.next
        current_node = self.current.previous
        current_node.next = new_node
        new_node.previous = current_node
        new_node.next = self.head
        self.head.previous = new_node
        self.current = new_node

        self.size += 1

    def cycle(self,index):
        if index > 0:
            for i in range(index):
                if self.current.next == self.head:
                    self.current = self.tail.next
                else:
                    self.current = self.current.next
        elif index < 0:
            for i in range(abs(index)):
                if self.current.previous == self.tail:
                    self.current = self.head.previous
                else:
                    self.current = self.current.previous
        else:
            print "useless cylce"

    def insert(self,data):
        new_node = node(data)
        current_node = self.current
        next_node = self.current.next
        current_node.next = new_node
        new_node.previous = current_node
        new_node.next = next_node
        next_node.previous = new_node

        self.size += 1

    def erase(self):
        self.cycle(1)
        value = self.current.data
        previous_node = self.current.previous
        next_node = self.current.next
        previous_node.next = next_node
        next_node.previous = previous_node
        self.current = previous_node
        self.size -= 1
        return value

    def get(self,index):
        if index >= self.size or index < 0:
            print "Index out of range"
            return None
        current_index = 0
        current_node = self.head
        while True:
            current_node = current_node.next
            if current_index == index:
                return current_node.data
            current_index += 1

    def display(self):
        elements = []
        current_node = self.tail
        while current_node.next != None and current_node.next != self.head:
            current_node = current_node.next
            elements.append(current_node.data)
        print elements

    def check(self):
        current = self.current
        s = ""
        while self.current.next != self.head:
            self.cycle(1)
        self.cycle(1)
        for i in range(self.size):
            s += str(self.current.data) + " "
            self.cycle(1)
        print s
        s = ""
        while self.current.previous != self.tail:
            self.cycle(-1)
        self.cycle(-1)
        for i in range(self.size):
            s += str(self.current.data) + " "
            self.cycle(-1)
        print s
        self.current = current

    def __getitem__(self,index):
        return self.get(index)

#---------------------------------------------------------------------------
# inputs
"""
test inputs
09 players; last marble is worth 0025 points: high score is 0032
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""
"""
puzzel input
412 players; last marble is worth 71646 points
"""
#---------------------------------------------------------------------------
elves = 412
gamelength = 71646*100
players = dict()

for i in range(elves):
    players[i] = 0


circle = linked_list()
circle.append(0)

temp = False

for i in range(0,gamelength):
    if (i+1)%23 != 0:
        circle.cycle(2)
        circle.insert(i+1)
    else:
        score = i+1
        circle.cycle(-7)
        marble = circle.erase()
        players[i%elves] += score + marble

# circle.check()

largest = 0
bestPlayer = 0
for each in players:
    print each, players[each]
    if players[each] > largest:
        largest = players[each]
        bestPlayer = each
print "winner", bestPlayer, largest
