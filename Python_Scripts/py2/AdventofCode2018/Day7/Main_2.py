with open("C:\Users\Jobber\Documents\Python Scripts\AdventofCode2018\Day7\input.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split("."))
    for i in range(len(lines)):
        lines[i] = lines[i][0]
    addedCost = 60
    workForce = 5
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
    addedCost = 0
    workForce = 2
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
        self.time = self.setTime()

    def setTime(self):
        return ord(self.node.lower()) - 96 + addedCost
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
print "compactNodes:", compactNodes
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
            temp.req.append(compactNodes[each][i].req[0])
        temp.time = temp.setTime()
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
    startNode.time = startNode.setTime()
    nodes.append(startNode)

print "unsorted nodes:", nodes
for each in nodes:
    print each.node
## sort the nodes alphabetically
nodes.sort(key=lambda x: x.node)
print "sorted nodes:"
for each in nodes:
    print each.node, each.req

#---------------------------------------------------------------------------------------
# worker class

class worker():
    def __init__(self,tag = -1):
        self.tag = tag
        self.state = True
        self.project = ""
        self.time = 0

#---------------------------------------------------------------------------------------
# find the order
print "\nstart puzzel"
comments = False
order = ""
time = 0
workers = []
for i in range(workForce):
    workers.append(worker(i+1))
print "workers:", workers

# start process
while True:
    # give workers jobs
    for worker in workers:
        if worker.state:
            for node in nodes:
                if node.req == "start" or node.req == "available" :
                    worker.state = False
                    worker.project = node.node
                    worker.time = node.time
                    nodes.remove(node)
                    break


    #-------------------------------------------
    if time == 0:
        text = "second  "
        for worker in workers:
            text = text + str(worker.tag) + "  "
        text = text + "Order"
        print text
    text = ""
    if time < 10:
        text = "     " + text + str(time) + "  "
    elif time >= 10 and time < 100:
        text = "    " + text + str(time) + "  "
    elif time >= 100 and time < 1000:
        text = "   " + text + str(time) + "  "
    else:
        text = "  " + text + str(time) + "  "


    for each in workers:
        if each.project != "":
            text = text + str(each.project) + "  "
        else:
            text = text + "." + "  "
    text = text + str(order)
    print text
    time += 1
    #-------------------------------------------
    # process the worker jobs
    for worker in workers:
        if worker.state == False:
            worker.time = worker.time - 1
            if worker.time == 0:
                order = order + worker.project
                worker.state = True
                for node in nodes:
                    if worker.project in node.req:
                        node.req.remove(worker.project)
                    if len(node.req) == 0:
                        node.req = "available"
                worker.project = ""

    workersFinished = True
    if len(nodes) == 0:
        for worker in workers:
            if worker.project != "":
                workersFinished = False
        if workersFinished:
            text = ""
            if time < 10:
                text = "     " + text + str(time) + "  "
            elif time >= 10 and time < 100:
                text = "    " + text + str(time) + "  "
            elif time >= 100 and time < 1000:
                text = "   " + text + str(time) + "  "
            else:
                text = "  " + text + str(time) + "  "
            for each in workers:
                if each.project != "":
                    text = text + str(each.project) + "  "
                else:
                    text = text + "." + "  "
            text = text + str(order)
            print text
            break

    if time == -1:
        break

#---------------------------------------------------------------------------------------
print "order:", order
# result: time = 975; order = JRHSBCKUTVWDQAIGYOPXMFNZEL
