import Tkinter as tk

class simulation:
    def __init__(self,raster, cars = None):
        self.raster = raster
        self.cars = cars
        self.scale = 50
        self.height = len(self.raster.tracks) * self.scale
        self.width  = len(self.raster.tracks[0]) * self.scale
        print self.height,self.width


        self.root = tk.Tk()
        self.root.title("Schematic")
        self.canvas = tk.Canvas(self.root,height = self.height, width = self.width)
        self.canvas.pack()
        self.draw_map(str(self.raster))
        tk.mainloop()

    def draw_map(self,raster):
        print "sim:"
        print raster
        lines = []
        index = 0
        for i in range(len(raster)):
            if raster[i] == "\n":
                if i != 0:
                    index +=1
                lines.append("")
            else:
                if raster[i] in ("<>"):
                    lines[index] = str(lines[index]) + "-"
                elif raster[i] in ("v^"):
                    lines[index] = str(lines[index]) + "|"
                else:
                    lines[index] = str(lines[index]) + str(raster[i])
        for each in lines:
            print "#", each
        for y in range(len(lines)):
            for x in range(len(lines[y])):
                self.canvas.create_rectangle((x)*self.scale,(y)*self.scale,(x+1)*self.scale,(y+1)*self.scale, outline = "grey")
                x_center,y_center = x+0.5, y+0.5
                if lines[y][x] == "-":
                    self.canvas.create_line((x_center-0.5)*self.scale,(y_center)*self.scale,(x_center+0.5)*self.scale,(y_center)*self.scale)
                elif lines[y][x] == "|":
                    self.canvas.create_line((x_center)*self.scale,(y_center-0.5)*self.scale,(x_center)*self.scale,(y_center+0.5)*self.scale)
                elif lines[y][x] == "/":
                    if y-1 >= 0 and x-1 >= 0:
                        if lines[y-1][x] in ("|","+","\\","/") and lines[y][x-1] in ("-","+","\\","/"):
                            self.canvas.create_arc((x_center-1)*self.scale,(y_center-1)*self.scale,(x_center)*self.scale,(y_center)*self.scale, start = 270, style = "arc")
                    if y+1 < len(lines) and x+1 < len(lines[y]):
                        if lines[y+1][x] in ("|","+","\\","/") and lines[y][x+1] in ("-","+","\\","/"):
                            self.canvas.create_arc((x_center)*self.scale,(y_center)*self.scale,(x_center+1)*self.scale,(y_center+1)*self.scale, start = 90, style = "arc")
                elif lines[y][x] == "\\":
                    if y-1 >= 0 and x:
                        pass
        print "sim end"
