class dungeon():
    def __init__(self,input):
        self.grid = input
        self.rounds_played = 0
        self.debug = None

    def round(self):
        # round moves each entity in order
        # stop only for testing
        stop = False
        # used to prefent double turns if a mob moves down and/or right
        turn_order = []
        # 2 for loops determing orther
        for y,row in enumerate(self.grid):
            for x,square in enumerate(self.grid[y]):
                # if the square under evaluation contains an elf or gobling
                if ("E" == square.team or "G" == square.team) and square not in turn_order:
                    turn_order.append(square)
                    # exectue the turn of this mob
                    self.turn((y,x))
            if stop:
                break
        self.rounds_played += 1

    def turn(self,coord):
        # the entity under consideration
        current_mob = self.grid[coord[0]][coord[1]]
        # find all the enemys in the dungeon
        current_enemys = self.detect_enemys(coord)
        if self.debug and False:
            print current_mob, coord, current_enemys
        # if there are no enemys, end its turn
        if current_enemys == []:
            return
        # determin where to travel
        current_target_tile = self.find_target(coord,current_enemys)
        # if there are no reachable tiles, end its turn
        if current_target_tile == []:
            return
        # if the current entity reached an enemy, it will attack
        # else it will move in an enemies direction
        if self.within_slapping_range(coord,current_enemys):
            self.attack()
        else:
            self.move(coord,current_target_tile)

    def within_slapping_range(self,coord,enemies):
        current_mob = self.grid[coord[0]][coord[1]]
        y,x = coord
        if (y-1,x) in enemies:
            return True
        elif (y,x-1) in enemies:
            return True
        elif (y,x+1) in enemies:
            return True
        elif (y+1,x) in enemies:
            return True
        return False

    def move(self,coord,destination):
        options = []
        y,x = coord
        if self.grid[y-1][x].team == "Tile":
            options.append((y-1,x))
        if self.grid[y+1][x].team == "Tile":
            options.append((y+1,x))
        if self.grid[y][x-1].team == "Tile":
            options.append((y,x-1))
        if self.grid[y][x+1].team == "Tile":
            options.append((y,x+1))
        if destination in options:
            best_step = destination
        else:
            best_steps = self.find_closessed(destination, options)
            best_step = self.find_first(best_steps)
        temp = self.grid[best_step[0]][best_step[1]]
        self.grid[best_step[0]][best_step[1]] = self.grid[y][x]
        self.grid[y][x] = temp

    # scan the dungeon for enemys
    def detect_enemys(self, coord):
        current = self.grid[coord[0]][coord[1]]
        # determin what to target
        if "E" == current.team:
            target = "G"
        elif "G" == current.team:
            target = "E"
        # find the coordinates of the enemys
        enemys = []
        for y,row in enumerate(self.grid):
            for x,square in enumerate(self.grid[y]):
                if target == square.team:
                    enemys.append((y,x))
        return enemys

    # determine how the current entity moves
    def find_target(self, coord, enemys):
        y,x = coord
        current = self.grid[y][x]
        # determin friend from foe
        if current.team == "E":
            target = "G"
        elif current.team == "G":
            target = "E"
        # check the spaces around the current entity for enemies
        if (y-1,x) in enemys:
            return [(y-1,x)]
        elif (y,x-1) in enemys:
            return [(y,x-1)]
        elif (y,x+1) in enemys:
            return [(y,x+1)]
        elif (y+1,x) in enemys:
            return [(y+1,x)]
        # determin the reachable tiles around the enemys
        # excluding walls or orther entitys, including its own position
        destinations = []
        for enemy in enemys:
            y,x = enemy
            if self.grid[y-1][x].team == "Tile":
                destinations.append((y-1,x))
            if self.grid[y+1][x].team == "Tile":
                destinations.append((y+1,x))
            if self.grid[y][x-1].team == "Tile":
                destinations.append((y,x-1))
            if self.grid[y][x+1].team == "Tile":
                destinations.append((y,x+1))
        # if there are no empty tiles around the enemys
        # return an empty list that will trigger the end of its turn
        if destinations == []:
            return []
        # determine the reachable and preverable destinations
        destination = self.determine_move(coord,destinations)
        return destination

    # determine the reachable and preverable destinations
    def determine_move(self,coord,destinations):
        # evalute each possible destination
        destinations = self.find_closessed(coord,destinations)
        destination = self.find_first(destinations)
        return destination


    def find_first(self,destinations):
        # choose the best destination from the dict
        best_row = len(self.grid)
        for each in destinations:
            if each[0] < best_row:
                best_row = each[0]
        for each in reversed(destinations):
            if each[0] != best_row:
                destinations.remove(each)
        best_column = len(self.grid[0])
        for each in destinations:
            if each[1] < best_column:
                best_column = each[1]
        return best_row, best_column

    def find_closessed(self,coord,destinations):
        # add the starting coordinate to a list
        if type(coord) != list:
            current = [coord]
        else:
            current = coord
        # keep track of the squares that have been visited
        visited = []
        # while there are still tiles left to explore
        while current:
            # store the outer range here
            new = []
            # for each of the tiles that are equidistance from the starting point
            for each in current:
                # mark that space as visited
                visited.append(each)
                y,x = each
                # look at the tiles around the current tile
                # if that tile is empty, aka not a wall or an entity
                # and if it has not yet been visited
                # and if it was not reached yet through one of the other border tiles
                if self.grid[y-1][x].team == "Tile" and (y-1,x) not in visited and (y-1,x) not in new:
                    new.append((y-1,x))
                if self.grid[y+1][x].team == "Tile" and (y+1,x) not in visited and (y+1,x) not in new:
                    new.append((y+1,x))
                if self.grid[y][x-1].team == "Tile" and (y,x-1) not in visited and (y,x-1) not in new:
                    new.append((y,x-1))
                if self.grid[y][x+1].team == "Tile" and (y,x+1) not in visited and (y,x+1) not in new:
                    new.append((y,x+1))
            # check if any of the border tiles are a destination
            temp = []
            for each in new:
                if each in destinations:
                    temp.append(each)
            # if one of the border tiles is a destination stop looking
            if len(temp) > 0:
                break
            # prepare the new border if no destination was reached
            else:
                current = new
        return temp

    def attack(self):
        pass

    def mark(self,coords):
        temp = []
        for y,row in enumerate(self.grid):
            temp.append([])
            for x,square in enumerate(self.grid[y]):
                if (y,x) in coords:
                    temp[y].append("?")
                else:
                    if self.grid[y][x].team == "Tile":
                        temp[y].append(".")
                    else:
                        temp[y].append(self.grid[y][x].team)
        string = ""
        for each in temp:
            for each2 in each:
                if "E" in each2:
                    string += "E"
                elif "G" in each2:
                    string += "G"
                else:
                    string += str(each2)
            string += "\n"
        print string


    def __str__(self):
        string = ""
        for each in self.grid:
            for each2 in each:
                if "Tile" == each2.team:
                    string += "."
                else:
                    string += each2.team
            string += "\n"
        return string

class entity():
    def __init__(self,team = "Tile"):
        self.team = team
        self.number = 0
        self.health = None

    def __str__(self):
        return self.team + str(self.number)

    def __eq__(self,other):
        if type(other) == type(""):
            if other == self.team:
                return True
            else:
                return False
    def __ne__(self,other):
        if type(other) == type(""):
            if other != self.team:
                return True
            else:
                return False
