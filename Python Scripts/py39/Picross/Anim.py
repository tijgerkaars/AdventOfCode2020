import tkinter as tk


class Anim:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title( ' test ' )
        self.root.bind('<Escape>', self.close_app)
        self.entry_size = 10

    def close_app(self, event=None):
        self.root.destroy()

class User_Input(Anim):
    def __init__(self):
        super().__init__()
        self.w = 5
        self.h = 5
        self.entries = {}
        self.root.grid_columnconfigure(0,minsize=self.entry_size)


        for x in range(self.w):
            self.add_entry(x+1,0)
        for y in range(self.h):
            self.add_entry(0,y+1)

        self.root.mainloop()
    
    def add_entry(self, x,y):
        f = tk.Frame(self.root, width = 50, height = 50)
        f.grid_propagate(0)
        f.grid(row=y, column=x)
        f.grid_columnconfigure(0, weight=1)
        e = tk.Entry(f)
        e.grid(row=y, column=x, sticky= 'NESW')
        e.grid_columnconfigure(0, weight=1)
        try:
            self.entries[(x,y)].append(e)
        except:
            self.entries[(x,y)] = [e]


class Dice_counter(Anim):
    def __init__(self):
        super().__init__()
        self.root.title( 'Dice Logger' )
        self.names =[
            'New',
            'Boris',
            'Pim',
            'Daan',
            'Jobber'
        ]
        self.dice = [
            f'd{i}' for i in [4,6,8,10,12,20]
        ]
        self.add_layout()

    """
        Data Structure

        self.data:
            - dict: self.names = keys
            - values:
                - dict: self.dice = keys
                - values = counter
        """
        
    
    def add_layout(self):
        menu = tk.StringVar(self.root)
        menu.set('-- names --')
        self.widgets = []
        w = tk.OptionMenu(self.root, menu, *self.names)
        i = 0
        w.grid(row = 0, column=i); i += 1
        self.widgets.append(w)

        menu = tk.StringVar(self.root)
        menu.set(self.dice[0])
        self.widgets = []
        w = tk.OptionMenu(self.root, menu, *self.dice[1:])
        w.grid(row = 0, column=i); i += 1
        self.widgets.append(w)

        w = tk.Entry(self.root)
        w.grid(row = 0, column=i); i += 1
        w.insert(0,'number here')

        w = tk.Entry(self.root)
        w.grid(row = 0, column=i); i += 1
        w.insert(0,'Comment Here')

        w = tk.Button(self.root, text='commit')
        w.grid(row = 0, column=i); i += 1
        self.widgets.append(w)

        i = 0
        querry_options = ['session', 'all']
        menu = tk.StringVar(self.root)
        menu.set(querry_options[0])
        self.widgets = []
        w = tk.OptionMenu(self.root, menu, *querry_options[1:])
        w.grid(row = 1, column=i); i += 1
        self.widgets.append(w)



        w = tk.Button(self.root, text='show')
        w.grid(row = 1, column=i); i += 1
        self.widgets.append(w)


        self.root.mainloop()



if __name__ == "__main__":
    Ui = Dice_counter()