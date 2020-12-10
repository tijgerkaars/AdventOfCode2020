with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day8\input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split("."))
    for i in range(len(lines)):
        lines[i] = lines[i][0]
        splitLines = []
        for each in lines[0].split(" "):
            splitLines.append(int(each))
    lines = splitLines
print lines

#---------------------------------------------------------------------------------------
# get test input
if False:
    with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day8\input_test.txt") as file:
        lines = []
        for line in file:
            # The rstrip method gets rid of the "\n" at the end of each line
            lines.append(line.rstrip().split("."))
        for i in range(len(lines)):
            lines[i] = lines[i][0]
        splitLines = []
        for each in lines[0].split(" "):
            splitLines.append(int(each))
    lines = splitLines
    print lines
#---------------------------------------------------------------------------------------
# define a node class

counter = 1
class Tree():
    def __init__(self,lines):
        self.data             = lines[:]
        self.numberOfChildren = lines[0]
        self.metaEntrys       = lines[1]
        self.metadata         = []
        self.data             = self.data[2:]
        self.children         = self.findChildren()
        self.node             = 0

    def info(self):
        print "node:", self.node
        print "Number of children:", self.numberOfChildren
        print "children:", self.children
        print "metaEntrys:", self.metaEntrys
        print "metadata:", self.metadata
        print "data:", self.data, "\n"

    def findChildren(self):
        global counter
        children = []
        for i in range(self.numberOfChildren):
            counter += 1
            child = Tree(self.data)
            self.data = self.data[2:]
            if child.numberOfChildren == 0:
                for j in range(child.metaEntrys):
                    child.metadata.append(child.data[j])
                self.data = self.data[child.metaEntrys:]
                child.data = child.data[self.metaEntrys:]
            elif child.numberOfChildren > 0:
                child.metadata = child.data[:child.metaEntrys]
                self.data = child.data[child.metaEntrys:]
            children.append(child)
        if len(self.data) == self.metaEntrys:
            self.metadata = self.data
        return children

    def getMeta(self):
        meta = []
        for each in self.metadata:
            meta.append(each)
        for each in self.children:
            for point in each.getMeta():
                meta.append(point)
        return meta

    def getValue(self):
        self.value = 0
        children = dict()
        for i in range(len(self.children)):
            children[i+1] = self.children[i]
        if len(self.children) == 0:
            self.value = sum(self.metadata)
        else:
            for each in self.metadata:
                if each in children:
                    self.value = self.value + children[each].getValue()
        return self.value
#---------------------------------------------------------------------------------------
# function to recursively find children

#---------------------------------------------------------------------------------------
# call function
root = Tree(lines)
print "root value:", root.getValue()

print "sum of metaEntrys", sum(root.getMeta())
