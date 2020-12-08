class row():
    def __init__ (self):
        self.plants = None
        self.left_boundary = 0
        self.gen = 0

    def __str__(self):
        string = str(self.gen) + ": " + self.plants
        return string


    def grow(self):
        self.gen += 1
        self.pad()

        new_plants = ".."

        for i in range(len(self.plants)-4):
            temp = ""
            for j in range(5):
                temp += self.plants[i+j]
            if temp in self.grow_conditions:
                new_plants += "#"
            else:
                new_plants += "."
        self.plants = new_plants

    def pad(self):
        for i in range(5):
            if self.plants[i] == "#":
                temp = ""
                for j in range(5-i):
                    temp += "."
                j += 1
                self.plants = temp + self.plants
                self.left_boundary -= j
                break
        for i in range(5):
            if self.plants[len(self.plants)-i-1] == "#":
                temp = ""
                for j in range(5-i):
                    temp += "."
                self.plants += temp
                break

    def score(self):
        product = 0
        for i in range(len(self.plants)):
            if self.plants[i] == "#":
                product += (self.left_boundary + i)
        return product
