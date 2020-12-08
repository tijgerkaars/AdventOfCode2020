#!/usr/bin/python

import Vizualize
import games as games
import Queue
import random
from datetime import datetime
import sys

#index of games is the board you want, index 0 is a board used for testing
game = games.games[7]
# paste pathway here to see the simulation without calculation
calculate = True
path_sim = []
# 1 = astar,
# 2 = breadth first,
# 3 = depth limited search,
# 4 = random search (loops is amount of attempts at random search)
algorithm = 4

# loops for rs
loops = 100

# depth limit
limit = 40

# defines row of red car
exit = 0
for i in range(len(game)):
	if 1 in game[i]:
		exit = i
		break

# shows info of object
def info(z):
	print "steps:", len(z.pathWay), ", path:", z.pathWay
	for i in range(len(z.start)):
		row = str(z.start[i])
		row.replace(" ", "")
		print z.start[i]
	print "\n"
# returns winning board
def Won(board):
	condition = 0
	for i in range(board.width):
		if board.start[exit][i] != 0:
			condition = 0
		if board.start[exit][i] == 1:
			condition = 1
	if condition == 1:
		return True
	elif condition == 0:
		return False
# returns a vertical move for all cars
def moveVert(board, i, j, ori):
	k = 0
	if ori == "S":
		k = 1
	elif ori == "N":
		k = -1
	empty = ((board.vertical[board.start[i][j]] - 1) * k)
	new_board = board.start[:]
	new_board[i+k] = board.start[i+k][:]
	new_board[i+k][j] = board.start[i][j]
	new_board[i - empty] = board.start[i - empty][:]
	new_board[i - empty][j] = 0
	temp = Board(new_board, board.vertical, board.horizontal)
	temp.pathWay = board.pathWay[:]
	temp.pathWay.append([board.start[i][j], ori])
	return temp
# moves cars horizontally
def moveHor(board, i, j, ori):
	k = 0
	if ori == "E":
		k = 1
	elif ori == "W":
		k = -1
	empty = ((board.horizontal[board.start[i][j]] - 1) * k)
	new_board = board.start[:]
	new_board[i] = board.start[i][:]
	new_board[i][j + k] = board.start[i][j]
	new_board[i][j - empty] = 0
	temp = Board(new_board, board.vertical, board.horizontal)
	temp.pathWay = board.pathWay[:]
	temp.pathWay.append([board.start[i][j], ori])
	return temp
# checks orientation cars where
#key is the car id and the length is the value
def check_cars(board):
	vertical = dict()
	horizontal = dict()
	for i in range(0, len(board)):
		for j in range(0, len(board[0])):
			if board[i][j] != 0:
				if i+1 < len(board):
					if board[i+1][j] == board[i][j]:
						if not board[i][j] in vertical:
							# add the id to the dictionary as key, value is the length (is updated later)
							vertical[board[i][j]] = 0
				if j+1 < len(board[0]):
					# if the space to the right of the car is the same car
					if board[i][j+1] == board[i][j]:
						# if the car is not yet in the horizontal dictionary
						if not board[i][j] in horizontal:
							# add the id to the dictionary as key, value is the length (is updated later)
							horizontal[board[i][j]] = 0
			# every time a car is found on the board the length is increased
			if board[i][j] in vertical:
				vertical[board[i][j]] += 1
			elif board[i][j] in horizontal:
				horizontal[board[i][j]] += 1
	return vertical, horizontal

# checks orientation of crs
orientation = check_cars(game)

# checks if following steps negate eachother
def PathSweep(l):
	length = len(l) - 2
	while True:
		changed = 0
		for i in range(length):
			if length - i > 0 and length - i+1 < len(l):
				if l[length-i][0] == l[length-i+1][0] and not l[length-i][1] == l[length-i+1][1]:
					del l[length - i + 1]
					del l[length - i]
					changed = 1
		if changed == 0:
			return l
			break

def PathSweep2(l):
	print "***", l
	l = [[4, 'S'], [5, 'S'], [4, 'S'], [5, 'N'], [4, 'N'], [5, 'S'], [4, 'S'], [4, 'S'], [3, 'E'], [2, 'S']]
	states = []
	# creat a starting game
	current = Board(game, orientation[0], orientation[1])
	states.append(current.start)
	# perfom al the steps
	for i in l:
		print "i in l:", i
		k = MoveStep(i, current)
		current = k
		states.append(current.start)
	position = 0
	print "l*", l
	for i in states:
		for j in range(position + 1,(len(states)-1)):
			if states[j] == i:
				for k in reversed(range(position+1, j+1)):
					print "you dumbo"
					del states[k]
					del l[k]
				break
		position += 1
	print "l", l
	return l

# s = [car number, ("S", "W", "E", "N")] grid = the board on which to move
def MoveStep(s, grid):
	step = s
	if step[1] == "N":
		for i in range(grid.height):
			for j in range(grid.width):
				if i -1 >= 0:
					if grid.start[i][j] == step[0] and grid.start[i-1][j] == 0:
						grid = moveVert(grid, i, j, step[1])
						break
	elif step[1] == "S":
		stop = 0
		for i in range(grid.height):
			for j in range(grid.width):
				if i +1 < grid.height:
					if grid.start[i][j] == step[0] and grid.start[i+1][j] == 0:
						grid = moveVert(grid, i, j, step[1])
						stop = 1
			if stop:
				break
	elif step[1] == "W":
		for i in range(grid.height):
			for j in range(grid.width):
				if j -1 >= 0:
					if grid.start[i][j] == step[0] and grid.start[i][j-1] == 0:
						grid = moveHor(grid, i, j, step[1])
						break
	elif step[1] == "E":
		for i in range(grid.height):
			for j in range(grid.width):
				if j+1 < grid.width:
					if grid.start[i][j] == step[0] and grid.start[i][j+1] == 0:
						info(grid)
						print grid,i,j,step[1]
						grid = moveHor(grid, i, j, step[1])
						break
	return grid


class Board(object):
	# board opject word gemaakt aan de hand van een grid
	def __init__ (self, board, vertical, horizontal):
		self.start = board
		self.height = len(self.start)
		self.width = len(self.start[0])

		# dictionaries to store info on the cars
		self.vertical = vertical
		self.horizontal = horizontal
		# the pathWay to get to this board
		self.pathWay = []

	def children(self):
		# create an array to store the children
		new_boards = []
		for i in range(self.height):
			for j in range(self.width):
				# if car is vertical
				if self.start[i][j] in self.vertical:
					if i < self.height - 1:
						# move the car down if possible
						if self.start[i+1][j] == 0:
							new_boards.append(moveVert(self, i, j, "S"))
					if i > 0:
						# Works the same as the move down
						if self.start[i-1][j] == 0:
							new_boards.append(moveVert(self, i, j, "N"))
				# if the car found is orientated horizontally
				if self.start[i][j] in self.horizontal:
					# check the length of the car
					if j + 1 < self.width:
						# if the position to the right is empty
						if self.start[i][j+1] == 0:
							new_boards.append(moveHor(self, i, j, "E"))
					if j > 0:
						# works the same as the move right
						if self.start[i][j-1] == 0:
							new_boards.append(moveHor(self, i, j, "W"))
		return new_boards

def simulation(speed, board):
	current_board = Board(game, board.vertical, board.horizontal)
	if board.start == current_board.start:
		path = path_sim
	else:
		path = board.pathWay
	anim_speed = speed
	counter = 1
	anim = Vizualize.RushHourVisualization(current_board, anim_speed)
	for step in path:
		counter += 1
		if step[1] == "N":
			for i in range(current_board.height):
				for j in range(current_board.width):
					if i -1 >= 0:
						if current_board.start[i][j] == step[0] and current_board.start[i-1][j] == 0:
							current_board = moveVert(current_board, i, j, step[1])
							break
		elif step[1] == "S":
			stop = 0
			for i in range(current_board.height):
				for j in range(current_board.width):
					if i +1 < current_board.height:
						if current_board.start[i][j] == step[0] and current_board.start[i+1][j] == 0:
							current_board = moveVert(current_board, i, j, step[1])
							stop = 1
							break
				if stop:
					break
		elif step[1] == "W":
			for i in range(current_board.height):
				for j in range(current_board.width):
					if j -1 >= 0:
						if current_board.start[i][j] == step[0] and current_board.start[i][j-1] == 0:
							current_board = moveHor(current_board, i, j, step[1])
							break
		elif step[1] == "E":
			for i in range(current_board.height):
				for j in range(current_board.width):
					if j+1 < current_board.width:
						if current_board.start[i][j] == step[0] and current_board.start[i][j+1] == 0:
							current_board = moveHor(current_board, i, j, step[1])
							break
		# update current board
		anim.update(current_board)
	anim.done()
	### end

# random search algorithm
def rs(roof):

	# starting grid
	grid = Board(game, orientation[0], orientation[1])
	# see how many cars there are
	maximum = 0
	for each in orientation[0]:
		if each > maximum:
			maximum = each
	for each in orientation[1]:
		if each > maximum:
			maximum = each
	counter = 0
	condition = True
	while condition:
		# stops if pathway exceeds roof
		if len(grid.pathWay) > roof:
			break
		# picks random car
		car = random.randint(1, maximum)
		car = int(car)
		# picks direction random
		direction = random.randint(1, 2)
		if car in orientation[0]:
			if direction == 1:
				direction = "N"
			else:
				direction= "S"
		elif car in orientation[1]:
			if direction== 1:
				direction= "E"
			else:
				direction= "W"
		step = [int(car), direction]
		if step[1] == "N":
			for i in range(grid.height):
				for j in range(grid.width):
					if i -1 >= 0:
						if grid.start[i][j] == step[0] and grid.start[i-1][j] == 0:
							grid = moveVert(grid, i, j, step[1])
							break
		elif step[1] == "S":
			stop = 0
			for i in range(grid.height):
				for j in range(grid.width):
					if i +1 < grid.height:
						if grid.start[i][j] == step[0] and grid.start[i+1][j] == 0:
							grid = moveVert(grid, i, j, step[1])
							stop = 1
							break
				if stop:
					break
		elif step[1] == "W":
			for i in range(grid.height):
				for j in range(grid.width):
					if j -1 >= 0:
						if grid.start[i][j] == step[0] and grid.start[i][j-1] == 0:
							grid = moveHor(grid, i, j, step[1])
							break
		elif step[1] == "E":
			for i in range(grid.height):
				for j in range(grid.width):
					if j+1 < grid.width:
						if grid.start[i][j] == step[0] and grid.start[i][j+1] == 0:
							grid = moveHor(grid, i, j, step[1])
							break
		else:
			continue
		# return grid when won
		if Won(grid):
			condition = False
			return grid
		counter += 1

def bf():

	# create starting board
	parent = Board(game, orientation[0], orientation[1])
	# create archive
	archive = set()
	archive.add(str(parent.start))
	# create queue
	queue = Queue.Queue()
	queue.put(parent)
	# counter for boards
	counter = 1
	while not queue.empty():
		# get first board
		first = queue.get()
		# create children
		children = first.children()
		won = 0
		# check all the children for victors
		for each in children:
			# if the child is not yet in the archive
			if not str(each.start) in archive:
				# put the child in the archive
				archive.add(str(each.start))
				# if no cars are blocking red car
				if Won(each):
					# return the winning board object
					print "\nwon"
					return each
					break
				# if the red cars path is still blocked
				else:
					# put the board in the queue
					queue.put(each)
			counter += 1
			if counter % 50000 == 0:
				print "counter:", counter/1000000.0, "million", ", queue:", queue.qsize(), ", archive size:", len(archive)
			if queue.empty():
				print "queue is empty"
	print "done"

# depth first search
def dls():
	depth = limit
	# create starting board
	parent = Board(game, orientation[0], orientation[1])
	# archive
	archive = dict()
	# archive start board
	archive[str(parent.start)] = str(parent.start)
	# create stack
	stack = []
	# add parent node to stack
	stack.append(parent)
	# until stack empty
	while not len(stack) == 0:
		# grab parent
		first = stack.pop(0)
		# create children
		children = first.children()
		winning_board = 0
		won = 0
		# loop over children
		for each in children:
			# if child not in archive
			if not str(each.start) in archive and len(each.pathWay) < depth + 1:
				archive[str(each.start)] = len(each.pathWay)
				# return child
				if Won(each):
					print "\nwon"
					return each
				else:
					# otherwise at to stack
					stack.insert(0, each)
			elif str(each.start) in archive and archive[str(each.start)] > len(each.pathWay):
				archive[str(each.start)] = len(each.pathWay)
				stack.insert(0,each)
			if len(stack) == 0:
				print "stack is empty"

def astar():

	# pathlength = 2.5,	carcostX = 6, carcostY = 10 with heuristics2 for solving board 5
	# this solves 1,2,3,4,6 with shortest path pathlength = 0.5 carcostX = 1 carcostY = 2
	pathlength = 2.5
	carcostX = 6
	carcostY = 10

	def heuristic1(board):
		cost = 0
		# loop over width
		for j in range(board.width):
			# cars left of red car no cost
			if board.start[exit][j] == 1:
				cost = 0
			# cars right from redcar extra cost
			if board.start[exit][j] != 0:
				cost += carcostX

				for n in range(exit, board.height):
					if board.start[n][j] != 0 and board.start[exit][j] != board.start[n][j]:
						cost += carcostX
						break
					elif board.start[n][j] == 0:
						break
				for n in range(0, board.height-exit):
					if board.start[exit-n][j] != 0 and board.start[exit][j] != board.start[exit-n][j]:
						cost += carcostY
						break
					elif board.start[exit-n][j] == 0:
						cost -= carcostY / 2
						break
				# penalty for every step extra
				for path in board.pathWay:
					cost += pathlength
		return cost

	def heuristic2(board):
		cost = 0

		# loop over width
		for j in range(board.width):
			# gets position of red car
			if board.start[exit][j] == 1 and board.start[exit][j + 1] != 1:
				# takes cars right from red car and adds penalty
				for k in range(board.start[exit][j], board.width):
					if board.start[exit][k] != 0:
						cost += carcostX
				# loops over cars vertical from red car and adds penalty
				for n in range(board.start[exit][j], board.height):
					if board.start[j][n] != 0:
						cost += carcostY
				# penalty for steps
				for path in board.pathWay:
					cost += pathlength
		return cost

	orientation = check_cars(game)
	# initialize the starting board
	boarding = Board(game,orientation[0], orientation[1])
	# create archive/ closed list
	archive = set()
	archive.add(str(boarding.start))
	# create open list
	priority = Queue.PriorityQueue()
	# put starting board in queue
	priority.put((0, boarding))
	counter = 0
	# for calculating path
	came_from = {}
	# calculates cost made so far
	cost_so_far = {}
	came_from[boarding] = 0
	cost_so_far[boarding] = 0
	won = 0
	childcost= 0
	winning_board = 0
	# until the queue is empty
	while not priority.empty():
		# get first board
		score, boarding = priority.get()
		# make children of that board
		childrens = boarding.children()
		for child in childrens:
			counter += 1
			if counter % 10000 == 0:
				print counter, len(archive)
			childCost = cost_so_far[boarding] + 1
			# if child not in archive
			if not str(child.start) in archive:
				cost_so_far[child] = childCost
				# computes totalcosts
				total = cost_so_far[child] + heuristic1(child)
				# put in priority queue
				priority.put( (total, child))
				# define pathway backs
				came_from[child] = boarding
				# archive child
				archive.add(str(child.start))
				# if won
				if Won(child):
					print "won \n"
					return child
				#else:
					#archive.add(str(child.start))
					#archive_astar[str(child.start)] = (child.start)

if algorithm == 1:
	print "astar"
	tijd = datetime.now()
	winning_board = astar()
	runtime = datetime.now() - tijd
	print "time:", runtime
	info(winning_board)
elif algorithm == 2:
	print "breadth first search"
	tijd = datetime.now()
	winning_board = bf()
	runtime = datetime.now() - tijd
	print "time:", runtime
	info(winning_board)
elif algorithm == 3:
	print "depth limited search"
	tijd = datetime.now()
	winning_board = dls()
	runtime = datetime.now() - tijd
	print "time:", runtime
	info(winning_board)
elif algorithm == 4:
	print "random search"
	# run the random search "loops" times, store the best result.
	#	all new results will be cut of at the length of the best result
	tijd2 = datetime.now()
	x = 0
	y = 0
	for i in range(loops):
		print "loop", i+1
		tijd = datetime.now()
		if x == 0:
			# rs(x), x is the inital cut off length
			winning_board = rs(10000)
		else:
			winning_board = rs(x)
		runtime = datetime.now() - tijd
		if winning_board:
			winning_board.pathWay = PathSweep(winning_board.pathWay)
			#winning_board.pathWay = PathSweep2(winning_board.pathWay)

			if x == 0 or x > len(winning_board.pathWay):
				real = winning_board
				x = len(winning_board.pathWay)
				print "steps:", x
				y = runtime
				print y
	print y
	info(real)
	runtime2 = (datetime.now() - tijd2)
	print runtime2

	winning_board = real
	info(winning_board)

if calculate:
	simulation(0.3, winning_board)
else:
	if len(path_sim) > 0:
		simulation(0.5, Board(game, orientation[0], orientation[1]))
