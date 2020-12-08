#---------------------------------------------------------------------------
# implents a linked list
class node:
    def __init__(self,data = None):
        self.data = data
        self.next = None
        self.previous = None

class linked_list:
    def __init__(self):
        self.head = node()
        self.tail = self.head

    def append(self,data):
        new_node = node(data)
        current_node = self.head
        while current_node.next != None:
            current_node = current_node.next
        current_node.next = new_node

    def get(self,index):
        if index >= self.length() or index < 0:
            print "Index out of range"
            return None
        current_index = 0
        current_node = self.head
        while True:
            current_node = current_node.next
            if current_index == index:
                return current_node.data
            current_index += 1

    def insert(self,index,data):
        if index >= self.length() or index< 0:
            print "Index out of range"
            return None
        current_node = self.head
        prior_node = self.head
        current_index = 0
        while True:
            current_node = current_node.next
            if current_index == index:
                new_node = node(data)
                prior_node.next = new_node
                new_node.next = current_node
                return
            prior_node = current_node
            current_index += 1

    def erase(self,index):
        if index >= self.length() or index < 0:
            print "Index out of range"
            return None
        current_index = 0
        current_node = self.head
        while True:
            last_node = current_node
            current_node = current_node.next
            if current_index == index:
                last_node.next = current_node.next
                return
            current_index += 1

    def length(self):
        current_node = self.head
        total = 0
        while current_node.next != None:
            total += 1
            current_node = current_node.next
        return total

    def display(self):
        elements = []
        current_node = self.head
        while current_node.next != None:
            current_node = current_node.next
            elements.append(current_node.data)
        print elements

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
circle = linked_list()
circle.append(0), circle.append(2), circle.append(1)
circle.display()

elves = 10
gamelength = 1618
players = dict()

for i in range(elves):
    players[i] = 0

active = 1

for number in range(3,gamelength+1):
    if number%23:
        if (active+2)%circle.length() == 0:
            circle.append(number)
        else:
            circle.insert((active+2)%circle.length(),number)
        for i in range(circle.length()):
            if circle[i] == number:
                active = i
    elif number%23 == 0 and number != 0:
        score = number
        active = active-7
        if active < 0:
            active = circle.length() + active
        score += circle[active]
        players[number%elves] += score
        circle.erase(active)

largest = 0
bestPlayer = 0
for each in players:
    print each, players[each]
    if players[each] > largest:
        largest = players[each]
        bestPlayer = each
print "winner", bestPlayer, largest
