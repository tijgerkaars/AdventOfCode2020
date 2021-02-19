import tkinter as tk


class Anim:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title( ' test ' )
        self.root.bind('<Escape>', self.close_app)
        self.entry_size = 10

    def close_app(self, event=None):
        self.root.destroy()

class Dice_counter(Anim):
    def __init__(self):
        super().__init__()
        self.root.title( 'Dice Logger' )
        self.names =[
            'New Name'
        ]
        self.dice = [ f'd{i}' for i in [4,6,8,10,12,20]] + ['New' ]

        self.add_layout()
        self.root.mainloop()

    """
        Data Structure

        self.data:
            - dict: self.names = keys
            - values:
                - dict: self.dice = keys
                - values = counter
        """
    
    def dropdown_name(self, x,y, event=None, **args):
        event=event.lower()
        print(x,y, event, args)
        if event == 'new name':
            self.update_widget_pos_row(x+1,y,d=1)
            e = self.create_entry(self.root,x+1,y, text='New Name', focus=True)
            e.focus()
    
    def update_widget_pos_row(self,x,y,d):
        for widget_x in reversed(list(self.widgets[y].keys())):
            if widget_x >= x:
                for each in self.widgets[y][widget_x]:
                    each.grid(row=y,column=widget_x+d)
                    w = self.widgets[y].pop(widget_x, None)
                    self.widgets[y][widget_x+d] = w



    def dropdown_dice(self, x,y, event=None, **args):
        event=event.lower()
        if event == 'new name':
            print( x,y, event=None, **args)
            print(self.widgets)

    def create_dropdown(self,root, x:int,y:int, command:callable, dropdown_list:list) -> tk.Widget:
        var = tk.StringVar(root)
        drp = tk.OptionMenu(root, var, *dropdown_list, command=lambda event, x=x,y=y: command(x,y, event=event))
        var.set(dropdown_list[0])
        drp.grid(column=x,row=y)
        drp.bind('<Button-1>', lambda event, drp=drp : self.dropdown_focus(drp, event))
        print(f"{drp.grid_info()}=")
        try:
            self.widgets[y][x].append(drp)
        except:
            try:
                self.widgets[y][x] = [drp]
            except:
                self.widgets[y] = {x:[drp]}
        return drp
    
    def dropdown_focus(self, drp, event=None):
        print(f"{drp=}, {event=}")
        drp.focus()
        self.root.focus()

    def create_entry(self,root, x:int,y:int,text:str='',focus:bool=False, f:[callable] = []):
        e = tk.Entry(root)
        e.config(fg = 'grey')
        e.grid(row=y, column=x)
        e.hold = ''
        e.first_key=True
        if focus:
            e.bind('<Key>', lambda event, e=e : self.on_entry_click(e, event))
            e.bind('<Button-1>', lambda event, e=e : self.on_entry_click(e, event))
            e.bind('<FocusOut>', lambda event, e=e : self.on_focusout(e, event))
            pass
        e.insert(0,text)
        return e

    def on_focusout(self, e, event= None):
        e.grid_forget()
        e.first_key=True
        e.insert(0,e.hold)
        self.root.update()
    
    def entry_focus(self, e,event=None):
        pass
    def on_entry_click(self,e, event=None):
        print(e, dir(event))
        print(event.type)
        e.hold = e.get()
        if e.first_key:
            e.delete(0,'end')
            e.first_key=False


    def add_layout(self):
        self.widgets = {0:[],1:[]}
        i=0; j=0

        # add dropdown for names
        self.create_dropdown(self.root, i,j, self.dropdown_name, self.names); i += 1
        """
        menu = tk.StringVar(self.root)
        drp = tk.OptionMenu(self.root, menu, *self.names, command=lambda event, x=0,y=0 : self.dropdown_name(x,y, event=event))
        menu.set(self.names[0])
        drp.grid(row = j, column=i); i += 1
        """

        self.create_dropdown(self.root, i,j, self.dropdown_dice, self.dice)
        """
        # add dropdown for dice
        menu = tk.StringVar(self.root)
        drp = tk.OptionMenu(self.root, menu, *self.dice[1:], command=lambda event, x=0,y=0 : self.dropdown_dice(x,y, event=event))
        menu.set(self.dice[0])
        drp.grid(row = j, column=i); i += 1
        self.widgets[j].append(drp)
        """

        return 

        # add entry for results
        e = tk.Entry(self.root) # pylint: disable=unreachable
        e.config(fg = 'grey')
        e.grid(row = 0, column=i); i += 1
        # entry.bind('<FocusIn>', on_entry_click)
        # entry.bind('<FocusOut>', on_focusout)
        e.insert(0,'number here')
        self.widgets[j].append(e)
        w = tk.Entry(self.root)
        w.grid(row = 0, column=i); i += 1
        w.insert(0,'Comment Here')

        w = tk.Button(self.root, text='commit')
        w.grid(row = 0, column=i); i += 1
        #        self.widgets.append(w)

        i = 0
        querry_options = ['session', 'all']
        menu = tk.StringVar(self.root)
        menu.set(querry_options[0])
        self.widgets = []
        w = tk.OptionMenu(self.root, menu, *querry_options[1:])
        w.grid(row = 1, column=i); i += 1
        #       self.widgets.append(w)



        w = tk.Button(self.root, text='show')
        w.grid(row = 1, column=i); i += 1
        #       self.widgets.append(w)

if __name__ == "__main__":
    Ui = Dice_counter()