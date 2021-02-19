import datetime


class Parameters:
    def __init__(self):
        self.current_dirs = None
        self.current_dirs = set(dir(self))
        self.figures = 0
        self.run = 0


    def __str__(self):
        string = ''
        for each in set(dir(self))-self.current_dirs:
            param = f'self.{each}'
            string += f'{each}: {eval(param)}\n'
        return string



if __name__ == "__main__":
    import run_main