        for y in range(len(lines)):
            for x in range(len(lines[y])):
                self.canvas.create_rectangle((x)*self.scale,(y)*self.scale,(x+1)*self.scale,(y+1)*self.scale, outline = "grey")
                if lines[y][x] == "\\":
                    if y < len(lines) and x-1 >= 0:
                        print y , len(lines)
                        if lines[y][x] != "-":
                            if lines[y][x] != "|":
                                self.canvas.create_arc((x-0.5)*self.scale,(y+0.5)*self.scale,(x+0.5)*self.scale,(y+1.5)*self.scale, style = "arc")
                    elif y-1 >= 0 and x+1 < len(lines[y]) and False:
                        self.canvas.create_arc((x+0.5)*self.scale,(y-0.5)*self.scale,(x+1.5)*self.scale,(y+0.5)*self.scale, style = "arc", start = 180)
                    self.canvas.create_line(x*self.scale,y*self.scale,(x+1)*self.scale,(y+1)*self.scale, fill = "grey")
                elif lines[y][x] == "/":
                    if y+1 < len(lines) and x+1 < len(lines[y]):
                        pass
                        # self.canvas.create_arc((x-0.5)*self.scale,(y-0.5)*self.scale,(x+0.5)*self.scale,(y+0.5)*self.scale, style = "arc", start = 270)
                        # self.canvas.create_arc((x-0.5)*self.scale,(y-0.5)*self.scale,(x+0.5)*self.scale,(y+0.5)*self.scale, style = "arc", start = -180)
                    self.canvas.create_line((x+1)*self.scale,(y)*self.scale,x*self.scale,(y+1)*self.scale, fill = "grey")
                elif lines[y][x] == "-":
                    self.canvas.create_line((x)*self.scale,(y+0.5)*self.scale,(x+1)*self.scale,(y+0.5)*self.scale)
                elif lines[y][x] == "|":
                    self.canvas.create_line((x+0.5)*self.scale,(y)*self.scale,(x+0.5)*self.scale,(y+1)*self.scale)
