import tkinter as tk
import json
from tkinter import messagebox
from datetime import datetime



class Anim:
    def __init__(self, *arg, **args):
        args = {key.lower(): value for key,value in args.items()}
        self.root = tk.Tk()
        self.root.title( ' test ' )
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Escape>', self.on_closing)
        try:
            self.debug = args['debug']
        except:
            self.debug = False
            pass
        self.entry_size = 10

    def on_closing(self,event=None):
        if not self.debug:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()

    def close_app(self, event=None):
        self.root.destroy()

class Dice_counter(Anim):
    def __init__(self,*arg, **args):
        super().__init__(*arg, **args)


        self.json_file = r'Roll_Logger.py\logg.json'
        try:
            with open(self.json_file, 'r') as f:
                print(f)
                setting = json.load(f)
                self.data = setting
        except:
            self.clear_data()

        self.clear_data()

        self.root.title( 'Dice Logger' )
        self.names = [ 'New Name' ]
        self.dice = [ f'd{i}' for i in [4,6,8,10,12,20]] + ['New' ]

        self.widget = {
            0 : {1: [
                    self.create_dropdown(0,1)
                    ]
                }
        }

        self.root.mainloop()

    def clear_data(self):
        self.data = {}
        self.data['START'] = {
                    'NAMES' : [],
                    'DICE'  : [],
                    'TYPES' : []     }
        self.data['LOG'] = {}

        self.add_log( '','','','','' )

    def add_log( self, name, dice, types, amount, comment ):
        now = datetime.now()
        day = now.date(); time = now.time()
        try:
            self.data['LOG'][day][]
        print(day)      #'%Y-%m-%d'))
        print(time)     #'%H:%M:%S'))

        '%d/%m/%y %H:%M:%S'

    def on_closing(self,event=None):
        if not self.debug:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                with open(self.json_file, 'w') as f:
                    f.write(json.dumps(self.data, indent=4))
        self.root.destroy()

    def create_Frame(self):
        pass
    

    def create_dropdown(self, x,y):
        pass

if __name__ == "__main__":
    ui = Dice_counter()