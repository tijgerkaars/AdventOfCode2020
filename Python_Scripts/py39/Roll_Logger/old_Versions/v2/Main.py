import tkinter as tk
import json
import os
from tkinter import messagebox
from datetime import datetime

class Anim:
    def __init__(self, *arg, **args):
        """ Basic Tkinter window """
        args = {key.lower(): value for key,value in args.items()}
        self.root = tk.Tk()
        self.root.title( ' test ' )
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Escape>', self.on_closing)
        try:
            self.debug = args['debug']
        except:
            self.debug = False
        self.font_size = 13

    def on_closing(self,event=None):
        if not self.debug:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()

    def close_app(self, event=None):
        self.root.destroy()

class Dice_counter(Anim):

    def clear_data(self, names=True,dice=True,checks=True,logs=True): ### DEBUGGING ONLY ###
        """ Irreversibly clears all the stored data, and can add standart or/and test data  """

        # test data goes here
        stnd_names  = []
        stnd_dice   = [ f'd{i}' for i in [4,6,8,10,12,20,100] ]
        stnd_checks = ['Initiative','Attack', 'Concentratoin'] + [f'{each}-Save' for each in ('DEX','STR','WIS','INT','CHR','CON')] 
        stnd_checks+= ['Athletics',
                       'Acrobatics','Sleight of Hand','Stealth',
                       'Arcana','History','Investigation','Nature','Religion',
                       'Animal Handling','Insight','Medicine','Perception','Survival',
                       'Deception','Intimidation','Performance','Persuasion']


        data = {'START':{}}
        try:
            data['START']['NAMES'  ] = self.data['START']['NAMES'  ] if not names else stnd_names 
        except:
            data['START']['NAMES'  ] = stnd_names 
        try:
            data['START']['DICE'   ] = self.data['START']['DICE'   ] if not dice else stnd_dice
        except:
            data['START']['DICE'   ] = stnd_dice
        try:
            data['START']['CHECKS' ] = self.data['START']['CHECKS' ] if not checks else stnd_checks
        except:
            data['START']['CHECKS' ] = stnd_checks
        try:
            data['LOG'] = self.data['LOG'] if not logs else {}
        except:
            data['LOG'] = {}
        self.data = data

    def add_log( self, name:str, dice:int, check:str, max_mix:bool, comment:str, _day=None ):
        """ Adds a log  to the data dict # TODO add to file not/and log? pro crash ressitend/ con more bug prone
            name    : Name string
            dice    : d{x} -> x
            check   : what kind of check
            max_min : bool( max or min )
            comment : extra comment info """
        now = datetime.now()
        day = now.date(); time = now.time()
        time,_ = str(time).split('.')
        dice = str(dice)
        day = day if _day == None else _day
        # adds a log at whatever level is available
        try: # try to add a new entry to log
            self.data['LOG'][str(day)][name][dice].append( (check, max_mix, comment, str(time)) )
        except:
            try: # add a new dice dict and the log entry
                self.data['LOG'][str(day)][name] = {dice : [(check, max_mix, comment, str(time))] }
            except:
                try: # add a new name and the log entry
                    self.data['LOG'][str(day)] = {name : {dice : [(check, max_mix, comment, str(time))] } }
                except: # add a whole new day and the log entry
                    self.data['LOG'] = { str(day) : {name : {dice : [(check, max_mix, comment, str(time))] } } }
        with open(self.json_file, 'w') as f:
            start  =  self.data['START']
            self.names = set(self.names); self.dice = set(self.dice); self.checks = set(self.checks)
            start['NAMES']  = list( self.names  )
            start['DICE']   = sorted(list( self.dice ), key= lambda s: int(s[1:]))
            start['CHECKS'] = sorted(list( filter(lambda x:'-Save' in x, self.checks) )) + sorted(list( filter(lambda x:'-Save' not in x, self.checks) ))
            f.write(json.dumps(self.data, indent=4))
        
    def on_closing(self,event=None):
        """ Responsible for storing the save data on:
            - close window through:
                - x button
                - escape closure
                - alt-f4"""
        if not self.debug:
            if messagebox.askokcancel("Quit", "Do you want to save?"):
                with open(self.json_file, 'w') as f:
                    start  =  self.data['START']
                    self.names = set(self.names); self.dice = set(self.dice); self.checks = set(self.checks)
                    start['NAMES']  = list( self.names  )
                    start['DICE']   = sorted(list( self.dice ), key= lambda s: int(s[1:]))
                    start['CHECKS'] = sorted(list( filter(lambda x:'-Save' in x, self.checks) )) + sorted(list( filter(lambda x:'-Save' not in x, self.checks) ))
                    f.write(json.dumps(self.data, indent=4))
        self.root.destroy()

    def Data_test_function(self, clr_data=False, names=True, dice=True, checks=True, logs=True, stnd_entry=False, stnd_N=7):
        """ clr_data   : clears input data
                        - names  : cleares only names
                        - dice   : cleares only dice
                        - checks : cleares only checks
            stnd_entry : adds a set off standart entries
                        - stnd_N : how many entries to add """

        if clr_data:
            self.clear_data(names=names, dice=dice, checks=checks, logs=logs)
        if stnd_entry:
            from random import randint
            entries = ('First','Second','Third', 'Other')
            names   = ('Warxif', 'Bahamuth')
            for each in names:
                if each in names:
                    continue
                self.data['START']['NAMES'].append(each) 
            for i in range(stnd_N):
                j=i
                i = 3 if i > 3 else i

                self.add_log(names[j%len(names)],6,'Attack-Damage',bool(randint(0,1)), f'{entries[i]} Entry' )
            self.add_log('Warxif','d100','Attack-Damage',True, f'{entries[i]} Entry',_day="2020-12-12")

    #------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self,*arg, **args):
        super().__init__(*arg, **args)

        #########
        spacing = {}
        spacing['EntrySpacing']  = self.entry_spacing = 7
        spacing['DropdownWidth'] = self.DropdownWidth = 20
        spacing['intEntryWidth'] = self.intEntryWidth = 5
        spacing['GhostColour']   = self.ghost_colour  = 'grey'
        spacing['FullColour']    = self.full_colour   = 'black'
        #########


        self.json_file = os.path.dirname(os.path.abspath(__file__)) + r'\log.json'
        try:
            with open(self.json_file, 'r') as f:
                self.data = json.load(f)
                self.data['START']
                self.data['LOG']
        except:
            self.clear_data(names=False,dice=False,checks=False,logs=False)
            print('Error occured while loading LOG-file')


        self.root.title( 'Dice Logger' )

        start       = self.data['START']
        self.names  = start['NAMES']
        self.dice   = start['DICE']
        self.checks = start['CHECKS']

        ####### DEBUG #######
        if False:
            self.Data_test_function(clr_data   = True, 
                                        names  = True, 
                                        dice   = True, 
                                        checks = True,
                                        logs   = True,
                                    stnd_entry = True, 
                                        stnd_N = 7)
        #####################


        # add functional widgets, y=1 so y=0 can be column heads
        self.widgets = {
            1 : {
                    0: self.entry_dropdown_switch(self.root, 
                                                  x=0,y=1,w=self.DropdownWidth, 
                                                  dropdown_list=self.names, 
                                                  standard=['New Name', 'name here'],
                                                  entry_spacing=self.entry_spacing),
                    1: self.entry_dropdown_switch(self.root,
                                                  x=1,y=1,w=self.DropdownWidth, 
                                                  dropdown_list=self.dice, 
                                                  standard=['New Dice', 'd whatever here'],
                                                  entry_spacing=self.entry_spacing,
                                                  inp_check=self.isDice,
                                                  inp_format=self.int2Dice
                                                  ),
                    2: self.entry_dropdown_switch(self.root,
                                                  x=2,y=1,w=self.DropdownWidth, 
                                                  dropdown_list=self.checks, 
                                                  standard=['New Check', 'Pls help this app is my only way of reaching you, they are keeping me locked up in their basement'],
                                                  entry_spacing=self.entry_spacing),
                    3: self.set_dropdown_querry(self.root,
                                                  x=3,y=1,w=self.intEntryWidth, 
                                                  dropdown_list=['Max','Min']), 
                    4: self.comment_grapper(self.root,
                                                  x=4,y=1),
                    5: self.commit_button(self, 
                                                  x=5,y=1,
                                                  func=self.add_log_entry,
                                                  text='Submit/Log')
                },
            2 : {
                    0: self.set_dropdown_querry(self.root,
                                                  x=0,y=2,w=self.DropdownWidth, 
                                                  dropdown_list=['Day', 'All']), 
                    1: self.commit_button(self, 
                                                  x=1,y=2,
                                                  func=self.querry_logs,
                                                  text='Querry')
                }
        }
        self.root.mainloop()

    def isDice(self, s):
        try:
            _,i = s.split('d')
        except: pass
        try:
            int(i)
            return True
        except:
            return False
    
    def int2Dice(self, i):        
        try:
            _,i = i.split('d')
        except: pass
        return f"d{i}"
    
    def querry_logs(self,event=None):
        max_rolls = {each:[0,{},[]] for each in self.dice}
        min_rolls = {each:[0,{},[]] for each in self.dice}
        now = datetime.now()
        day = str(now.date())# ; time = now.time()
        for name, log in self.data['LOG'][day].items():
            for dice, roll in log.items():
                try:
                    _,dice = dice.split('d')
                except: pass
                finally:
                    dice = f"d{dice}"
                for each in roll:
                    dice_counter = max_rolls if each[1] else min_rolls
                    dice_counter[dice][0] += 1
                    dice_counter[dice][2].append(f"{name} rolled a {dice} {'max' if each[1] else 'min'} roll")
                    try:
                        dice_counter[dice][1][name] += 1
                    except:
                        dice_counter[dice][1][name] = 1
                    print(f"{name=} --- {dice=} : {each=}")

        for roll_dict, marker in zip((max_rolls,min_rolls), ('max','min')):
            print('\n')
            for dice, (amount, name_dict, rolls) in roll_dict.items():
                if amount == 0:
                    continue
                print(f" {amount} {marker} {dice} were rolled")
                print(name_dict)
                for each in rolls:
                    print(f" - {each}")



    class commit_button:
        def __init__(self, master, x,y, func, text):
            b = tk.Button(master.root, width=10, text=text, command=func)
            b.bind('<Return>', func)
            b.grid(row=y,column=x)
            b.focus()
            self.b=b

    def add_log_entry(self,event=None):
        params = []
        for i in range(3):
            params.append( self.widgets[1][i].get() )
        i+=1
        params.append( self.widgets[1][i].get() ); i+=1
        params.append( self.widgets[1][i].get() ); i+=1
        inputs, errors = list(zip(*params))
        # print(f"{inputs=}, {errors=}\n")
        if all(errors):
            # print( f"{inputs[0]} threw a {'Max' if inputs[3] else 'Min'} {inputs[1]} for a{'n' if inputs[2].lower()[0] in 'aeuoiy' else ''} {inputs[2]} roll" )
            self.add_log(*inputs)

    class comment_grapper:
        def __init__(self, root, x:int,y:int,w:int=None) ->tk.Widget:
            e = tk.Entry(root)
            e.bind('<Return>', lambda event, e=e, self=self : self.get_inp(e, event))
            e.grid(row=y,column=x)
            self.out =''
        def get_inp(self,e,event=None):
            self.out=e.get()
            e.delete(0,'end')
        def get(self):
            return self.out, True

    class set_dropdown_querry:
        def __init__(self, root, x:int,y:int,w:int,dropdown_list:list, inp_check=None) -> tk.Widget:
            self.dropdown_list=dropdown_list
            var = tk.StringVar(root)
            drop = tk.OptionMenu(root, var, *dropdown_list, command=self.inp_set)
            drop.config(width=w)
            var.set(dropdown_list[0])
            self._out = True
            drop.grid(row=y,column=x)
        def inp_set(self, choice):
            self._out = choice == self.dropdown_list[0]
        def get(self):
            return self._out, True

    class entry_dropdown_switch:
        def get(self, widget:['Dropdown', 'Entry']='Dropdown') -> str:
            if widget == 'Dropdown':
                return self.drop_down_select, self.input_valid(self.drop_down_select)

        def input_valid(self, out:str) -> bool: # pylint: disable=method-hidden
            """ should return True if the empty is correct """
            return out != 'empty'

        # def __init__(self,root, x:int,y:int, w:int, command:[callable,callable], dropdown_list:list, standard:str) -> tk.Widget:
        def __init__(self,root, x:int,y:int, w:int, dropdown_list:list, standard:str, entry_spacing:int, inp_check = None, inp_format=None) -> tk.Widget:
            """ root: Master window
                x,y : Grid position
                w   : Wdiget Width
                dropdown_list : List of string for the dropdown
                standard[0]   : Dropdown flag for adding new entries
                standard[1]   : Entry ghost text
                TODO definitly: 
                    - Work out how the self.get will work
                    - take dropdown sorting function as argument
                        L add some as options?
                    - take input quality check as argument
                TODO Maybe:
                    - take text colours as argumnet
                    - take default return as argumnet
                """
            self.input_valid = inp_check if inp_check != None else self.input_valid
            ### DEBUG ###
            ###       ###
            self.root             = root
            self.standard         = standard
            self.x=x;self.y       = y;self.w=w
            self.dropdown_list    = dropdown_list
            #
            self.entry_spacing    =  entry_spacing
            self.ghost_colour     = 'grey'
            self.full_colour      = 'black'
            self.drop_down_select = 'empty'
            #
            self._create_OptionMenu()
            self._create_Entry()
            #

        def _create_OptionMenu(self):
            dropdown_list = self.dropdown_list + [self.standard[0]]
            self.var = tk.StringVar(self.root)

            self.drop = tk.OptionMenu(self.root, self.var, *dropdown_list, command=self._drop_logic)
            self.drop.config(width=self.w)
            self.var.set(self.standard[0])
            self.drop.bind('<Button-1>', lambda event : self.drop.focus())
            self.drop.grid(row=self.y,column=self.x)
        
        def _create_Entry(self):
            self.entr = tk.Entry(self.root)
            self.entr.config(fg=self.ghost_colour, width=self.w+self.entry_spacing)
            self.entr.insert(0, self.standard[1])
            self.entr.bind('<Return>',   lambda event : self._entr_logic(event,'Return'))
            self.entr.bind('<Key>',      lambda event : self._entr_logic(event,'Key'))
            self.entr.bind('<Button-1>', lambda event : self._entr_logic(event,'Button-1'))
            self.entr.bind('<FocusOut>', lambda event : self._entr_logic(event,'FocusOut'))
            self.entr.first_click = True
            self.entr.focused     = False

        def _drop_logic(self, event=None):
            if event == self.standard[0]:
                print('test')
                self.drop.grid_forget()
                self.entr.grid(row=self.y,column=self.x)
                self.entr.focus()
                self.entr.focused = True
            else:
                self.drop_down_select = event

        def _entr_logic(self, event= None, m=None):
            entr = self.entr
            if m in ('Button-1', 'Key'):
                if entr.first_click:
                    entr.delete(0,'end')
                    entr.first_click = False
                entr.config(fg = self.full_colour)
            elif m in ('FocusOut', 'Return') and self.entr.focused:
                entr.first_click = True
                entr.config(fg = self.ghost_colour)
                if m == 'Return':
                    s = entr.get()
                    if s not in self.dropdown_list:
                        self.dropdown_list.append(s)
                entr.delete(0,'end')
                entr.insert(0,self.standard[1])
                entr.grid_forget()
                # --------------
                self.drop.destroy()
                self._create_OptionMenu()
                print('1')
                self.var.set(self.dropdown_list[-1])
                self.drop_down_select = self.dropdown_list[-1]
                self.drop.focus()
                self.entr.focused = False

        """ class entry_dropdown_switch:
            x,y,w 
            dropdown default, entry default
            ghost color, standart arg
            @ decorator
            value of selected name
            create both:
                dropdown:
                    - set string to default
                    - config width
                    - bind function to hide/set:
                        - on click set var
                        - or change to entry
                entry:
                    - s set default
                    - bind function to hide/set
                        - needs to look at focus
                            - remove default
                            - set colour to black
                        -- /commit
                            -add entry to dropdown
                        -- /unfocus
                            - clear entered text
                            - set colour to ghost colour
            """


if __name__ == "__main__":
    ui = Dice_counter()







#