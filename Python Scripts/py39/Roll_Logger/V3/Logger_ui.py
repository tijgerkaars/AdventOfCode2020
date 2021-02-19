import os
import json
import tkinter as tk
from tkinter import messagebox; tk.messagebox = messagebox

class Logger_UI:
    def __init__(self, *arg, **args):
        """ Basic Tkinter window """
        args = {key.lower(): value for key,value in args.items()}
        self.root = tk.Tk()
        self.root.title( ' Roll Logger V3 ' )
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Escape>', self.on_closing)
        self.font_size = 13

        self.file_name =  r'\log.json'
        self.json_file = os.path.dirname(os.path.abspath(__file__)) + self.file_name
        try:
            with open(self.json_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError as e:
            print(
                str(e).replace('\\\\', '\\')
                )
            self.data = {}
            stnd_names  = []
            stnd_dice   = [ f'd{i}' for i in [4,6,8,10,12,20,100] ]
            stnd_checks = ['Initiative','Attack', 'Concentratoin'] + [f'{each}-Save' for each in ('DEX','STR','WIS','INT','CHR','CON')] 
            stnd_checks+= [ 'Athletics',
                            'Acrobatics','Sleight of Hand','Stealth',
                            'Arcana','History','Investigation','Nature','Religion',
                            'Animal Handling','Insight','Medicine','Perception','Survival',
                            'Deception','Intimidation','Performance','Persuasion']

            data = {'START':{}}
            data['START']['NAMES'  ] = stnd_names 
            data['START']['DICE'   ] = stnd_dice
            data['START']['CHECKS' ] = stnd_checks
            self.data = data
            tk.messagebox.showinfo('ERROR: FILE missing', f"Error occured while loading 'log.json'. File should be in: {self.json_file.replace(self.file_name, '')}\n\n Will try to create temp file on closure")
            self.json_file = self.json_file.replace('.json', '_temp.json')
            print('Error occured while loading "log.json"')
            self.root.focus_force()


    def on_closing(self,event=None):
        if tk.messagebox.askyesno("Quit", "Do you want to save before quitting?"):
            with open(rf"{self.json_file}", 'w') as f:
                f.write(json.dumps(self.data, indent=4))
        self.close_app()

    def close_app(self, event=None):
        self.root.destroy()


if __name__ == "__main__":
    import Main