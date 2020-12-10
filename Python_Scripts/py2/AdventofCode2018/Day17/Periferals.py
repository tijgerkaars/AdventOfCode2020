from datetime import datetime



class ground():
    def __init__(self,coords,well):
        print (well)
        # determin dimensions
        self.y_max, self.x_min, self.x_max = coords[0][0],coords[0][1],coords[0][1]
        self.y_min = 0
        for each in coords:
            self.y_max = max(each[0], self.y_max)
            self.x_max = max(each[1], self.x_max)
            self.x_min = min(each[1], self.x_min)
        # include buffers to the left, right
        self.x_min -= 1
        self.x_max += 2
        # acount for the row 0
        self.y_max += 1

        self.well = (well[0] - self.y_min, well[1] - self.x_min)

        print(self.well)

        print (self.y_max, self.x_min, self.x_max)

        # make a dict containing all the clay
        _coords = dict()
        for i,each in enumerate(coords):
            if each[0] not in _coords:
                _coords[each[0]] = set()
                _coords[each[0]].add(each[1] - self.x_min)
            else:
                _coords[each[0]].add(each[1] - self.x_min)
            coords[i] = (each[0], each[1] - self.x_min)
        print ("_coords:", _coords)

        # create map
        start_time = datetime.now()
        # add all the rows as keys and
            # and all the tiles to those rows
        chart = dict()
        for y in range(self.y_max):
            chart[y] = dict()
        print ("created a list for the rows in:", datetime.now() - start_time)
        start_time = datetime.now()
        for y in range(self.y_max):
            # print ("drawing row:", y ,"of", self.y_max-1)
            # add the correct tile type to the chart "#" for clay, "+" for well, "." for sand
            for x in range(self.x_max - self.x_min):
                if y in _coords and x in _coords[y]:
                    chart[y][x] = cube((y,x), "#")
                elif (y,x) == (self.well[0],self.well[1]):
                    temp = cube((y,x), "+")
                    chart[y][x] = temp
                    self.water_head = temp
                    self.water_head.source = "Well"
                    self.well_cube = self.water_head
                else:
                    chart[y][x] = cube((y,x))
        print ("filled the rows in:", datetime.now() - start_time)
        self.chart = chart

    def create_water(self):
        current = self.water_head
        # find water_head
        y,x = current.coord
        # if it is not the lowest level
        if y+1 < self.y_max:
            # if i can flow down
            if self.chart[y+1][x].state == ".":
                # print "going down"
                # ill flow down
                new = self.chart[y+1][x]
                new.state = "|"
                new.source = current
                self.water_head = new
            # elif i can flow left
            elif x-1 >= 0 and self.chart[y][x-1].state == "." and self.chart[y+1][x].state in "~#":
                # ill flow left
                # print "going left"
                new = self.chart[y][x-1]
                new.state = "|"
                new.source = current
                self.water_head = new
            #elif i can flow right
            elif x+1 < self.x_max - self.x_min and self.chart[y][x+1].state == "." and self.chart[y+1][x].state in "~#":
                #ill flow right
                # print "flowing down"
                new = self.chart[y][x+1]
                new.state = "|"
                new.source = current
                self.water_head = new
            # else
            else:
                # if the backtracking reaches the start all branches are done
                if current == self.well_cube:
                    return
                # if a wall is found on the right or left
                    # check how far away the other wall is, if any
                    ## check while the square = "|" or "#"
                    ## check if the square below is clay or setteled water
                        # if so, then settel all the water between the clay walls
                enclosed = False
                # if the square to the left of the water_head is a wall or already setteled water
                if x-1 > 0 and self.chart[y][x-1].state in "#~":
                    # look to the right of this square for all the squares in that row
                    for _x in range(x, self.x_max - self.x_min):
                        # if you find an open square, break
                        if self.chart[y][_x].state == "." and self.chart[y+1][_x].state in ".|":
                            break
                        # if you find an other wall before that happens, that piece is enclosed
                        elif self.chart[y][_x].state == "#":
                            enclosed = True
                            break
                elif x+1 < self.x_max - self.x_min and self.chart[y][x+1].state in "~#":
                    for _x in range(x,0,-1):
                        if self.chart[y][_x].state == "."  and self.chart[y+1][_x].state in ".|":
                            break
                        elif self.chart[y][_x].state == "#":
                            enclosed = True
                            break
                if enclosed:
                    temp = [x,_x]
                    for i in range(min(temp),max(temp)):
                        if self.chart[y][i].state == "|":
                            self.chart[y][i].state = "~"

                    while current.state == "~":
                        self.water_head = current.source
                        current = self.water_head
                    self.create_water()

                else:
                    self.water_head = current.source
                    self.create_water()
        else:
            self.water_head = current.source
            self.create_water()
            # if the stream reached the bottom
            # take a step back and check if it can flow otherwise



    def reachable(self):
        # counters for the flowing and setteled water tiles
        setteled_counter = 0
        flowing_counter = 0
        well_counter = 0
        # loop over all the tiles
        for y in range(self.y_max):
            for x in range(self.x_max-self.x_min):
                square = self.chart[y][x]
                if square.state  == "~":
                    setteled_counter += 1
                elif square.state == "|":
                    flowing_counter += 1
                elif square.state == " +":
                    well_counter += 1
        print ("Result: -- | :", flowing_counter, " ~ :", setteled_counter, " + :", well_counter)
        return flowing_counter + setteled_counter


    def __str__(self):
        string = ""
        #"""
        #------------------------------------------------------------------------------------
        # if you want the x marked above the print
            # buffer is used both for the x and y marking
        buffer = " "

        x_markers = []
        longest_x = len(str(self.x_max))
        longest_y = len(str(self.y_max))
        x_buffer = ""
        for i in range(longest_y):
            x_buffer += " "
        x_buffer += buffer
        for i in range(longest_x):
            temp = x_buffer
            x_markers.append(temp)
        for x in range(self.x_max-self.x_min):
            _x = str(self.x_min+x)
            this_x_len = len(_x)
            for i,letter in enumerate(_x):
                x_markers[i] += _x[i]
        for i in range(longest_x):
            x_markers[i] += " \n"
        for each in x_markers:
            string += each
        #------------------------------------------------------------------------------------
        #"""
        for y in range(self.y_max):
            #-----------------------------------------
            # if you want the y marked along the print
            _y = str(y)
            while len(_y) < longest_y:
                _y = " " + _y
            string += _y + buffer
            #-----------------------------------------
            for x in range(self.x_max-self.x_min):
                square = self.chart[y][x]
                if square == self.water_head and square != self.well_cube:
                    string += "*"
                elif square.state == ".":
                    string += " "
                elif square.state == "~":
                    string += "-"
                else:
                    string += str(square)
            string += "\n"
        string += "\n"
        return string


class cube():
    def __init__(self,coord,state = "."):
        self.coord = coord
        self.state = state
        self.source = None

    def __str__(self):
        return self.state
