with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day7\input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split("."))
    for i in range(len(lines)):
        lines[i] = lines[i][0]
print lines

#---------------------------------------------------------------------------------------
# get test input
if False:
    with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day7\input_test.txt") as file:
        lines = []
        for line in file:
            # The rstrip method gets rid of the "\n" at the end of each line
            lines.append(line.rstrip().split("."))
        for i in range(len(lines)):
            lines[i] = lines[i][0]
    print lines
#---------------------------------------------------------------------------------------
# class to determine order and dependencies

class node():
    def __init__(self,string = "Step C must be finished before step A can begin"):
        self.string = string
        req,rest = self.string.split(" must")
        trash, req = req.split(" ")
        self.req = [req]
        trash,node = rest.split("step ")
        node,trash = node.split(" can")
        self.node = node
#---------------------------------------------------------------------------------------
# creat a node for each entry
nodes = []
for each in lines:
    nodes.append(node(each))
print nodes

#---------------------------------------------------------------------------------------
# if multiple nodes have been made with the same sign but different requierments
# make them into 1 node

## find the duplicate nodes
compactNodes = dict()
for i in range(len(nodes)):
    print "node:", nodes[i].node, "requiers:", nodes[i]. req
    if nodes[i].node not in compactNodes:
        compactNodes[nodes[i].node] = [nodes[i]]
    else:
        compactNodes[nodes[i].node].append(nodes[i])
print compactNodes
#---------------------------------------------------------------------------------------
## make a single node out of them
nodes = []

for each in compactNodes:
    if len(compactNodes[each]) == 1:
        nodes.append(compactNodes[each][0])
    else:
        temp = node()
        temp.node = each
        temp.req = [compactNodes[each][0].req[0]]
        for i in range(1,len(compactNodes[each])):
            print i
            temp.req.append(compactNodes[each][i].req[0])
        nodes.append(temp)

#--------------------------------------------------------------------------------------
# add a starting node

names = []
for each in nodes:
    for temp in each.req:
        if temp not in names:
            names.append(temp)
for each in nodes:
    if each.node in names:
        names.remove(each.node)
for each in names:
    startNode = node()
    startNode.node = each
    startNode.req = "start"
    nodes.append(startNode)


## sort the nodes alphabetically
nodes.sort(key=lambda x: x.node)

for each in nodes:
    print each.node

#---------------------------------------------------------------------------------------
# find the order
print "start puzzel"
order = ""

while True:
    if len(nodes) == 0:
        break
    for node in nodes:
        nextNode = False
        if node.req == "start" or node.req == "available":
            order = order + node.node
            print order
            nodes.remove(node)
            for rest in nodes:
                print rest.node, rest.req
                if node.node in rest.req:
                    nextNode = True
                    rest.req.remove(node.node)
                if len(rest.req) == 0:
                    nextNode = True
                    rest.req = "available"
                print rest.node, rest.req
        if nextNode:
            break
#---------------------------------------------------------------------------------------
print order
# result = JRHSBCKUTVWDQAIGYOPXMFNZEL
