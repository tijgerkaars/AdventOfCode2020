class node:
    def __init__(self,data = None):
        self.data = data
        self.next = None
        self.previous = None
    def prev(self):
        return self.previous
    def next(self):
        return self.next

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

    def _current(self):
        return self.current

    def _start(self):
        return self.tail.next

    def _end(self):
        return self.head.previous

    def _next(self):
        if self.current.next != self.head:
            return self.current.next
        else:
            print "next is head, returning tail.next"
            return self.tail.next

    def _previous(self):
        if self.current.previous != self.tail:
            return self.current.previous
        else:
            print "previous is tail, returning head.previous"
            return self.head.previous

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

    def erase(self,amount):
        previous_node = self.current.previous
        next_node = self.current
        deleted_data = []
        for i in range(amount):
            deleted_data.append(next_node.data)
            next_node = next_node.next
        previous_node.next = next_node
        next_node.previous = previous_node
        self.size -= amount
        return deleted_data

    def get(self):
        return self.current.data

    def get_index(self,index):
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

    def get_neighbours(self):
        return self.current.previous,self.current,self.current.next

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

    def __str__(self, buffer = ""):
        current = self.current
        self.current = self.tail.next
        s = ""
        for i in range(self.size):
            s += str(self.current.data) + buffer
            self.current = self.current.next
        self.current = current
        return s


    def __getitem__(self,index):
        return self.get(index)

    def erase_data(self,input):
        for d in input:
            self.current = self.tail.next
            while self.current.next != None:
                if self.current.data == d:
                    self.current.previous.next = self.current.next
                    self.current.next.previous = self.current.previous
                    self.current = self.current.next
                    self.size -= 1
                else:
                    self.current = self.current.next
        self.current = self.tail.next
