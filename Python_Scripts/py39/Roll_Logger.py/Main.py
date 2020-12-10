import tkiner as tk


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

        self.widget = {
            0 : {1: [
                    self.create_dropdown(0,1)
                    ]
                }
        }

        self.root.mainloop()
    `
    def create_Lable(self):
        pass
    

    def create_dropdown(self, x,y):
        pass