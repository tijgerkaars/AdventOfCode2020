import math
import time

from Tkinter import *

class Visualization:
    def __init__(self, board, index, delay):
        self.delay = delay
        self.board = board
        self.index = index

        self.width = len(self.board[0][0])
        self.height = len(self.board[0])
        self.max_dim = max(self.width, self.height)

        # Initialize a drawing surface
        self.master = Tk()
        self.w = Canvas(self.master, width = 1000, height = 1000)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(self.width, self.height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "grey")

        self.text = self.w.create_text(25, 0, anchor = NW, text = self._status_string())
        self.id_text = None
        self.time = 0
        self.master.update()

        for i in range(self.width+1):
            x1, y1 = self._map_coords(i,0)
            x2, y2 = self._map_coords(i,self.height)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(self.height):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(self.width, i)
            self.w.create_line(x1, y1, x2, y2)

    def _status_string(self):
        # "Returns an appropriate status string to print."
        self.moves = self.moves + 1
        return "moves: ", self.moves

    def _map_coords(self, x, y):
        # "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((y - self.height / 2.0) / self.max_dim))

    def _draw_grid(self, board, each):
        for i in range(board.height):
            for j in range(board.width):
                if board.start[i][j] == each:
                    x = j
                    y = i

        if each in self.board.horizontal:
            x += 1
            x1, y1 = self._map_coords(x, y)
            color = "blue"
            if each == 1:
                color = "red"
            x2, y2 = self._map_coords(x-self.board.horizontal[each], y+1)
            return self.w.create_rectangle(x1, y1, x2, y2, fill = color)
        elif each in self.board.vertical:
            y += 1
            x1, y1 = self._map_coords(x, y)
            x2, y2 = self._map_coords(x+1, y-self.board.vertical[each])
            return self.w.create_rectangle(x1, y1, x2, y2, fill = "green")

    def update(self, board):

        if self.cars:
            for car in self.cars:
                self.w.delete(car)
                self.master.update_idletasks()

        self.cars = []
        self.id_text = []

        # draw cars
        for each in self.board.vertical:
            self.cars.append(self._draw_grid(board, each))
        for each in self.board.horizontal:
            self.cars.append(self._draw_grid(board, each))
                # self.id_text.append(self._draw_ids(car))
        counter = 0
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(25, 0, anchor = NW, text = self._status_string())
        self.master.update()
        time.sleep(self.delay)

    def done(self):
        mainloop()
