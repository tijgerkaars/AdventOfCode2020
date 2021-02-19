class Inhibitor:
    
    def __str__(self):
        return f'{self.name}: {self.moles:.2e} Mol'

    def __init__(self, name, conc, conc_type, eps):
        """
        TODO change  if/else structure to database load:
            - JSON probably
            - maybe use pandas or pickle
        TODO : Add species class for inhertince
        TODO : add __str__/__repr__
        """
        self.name = name

        if name == 'test':
            self.state = 'Imaginary'
            self.pmax     = 1       # max number of radicals generated per inhibitor molecule
            self.M        = 10      # g/mol
            self.dens     = -1      # g/mL at 25 °C
            self.eps      = 1       # M^-1 cm^-1
            self.nu       = -100    # wavelength
        elif name == 'o-Cl-HABI':
            self.headers  = [
                "Inhibitor_ground",
                "Inhibitor_radical",
                "Inhibitor_reduced"
            ]
            self.state    ='Solid'
            self.pmax     = 2                  
            self.M        = 659.6                 
            self.dens     = []
            try :
                self.eps = {
                    366 : 400,    # ref 1
                    469 : 5.69,   # ref zotero eps
                    405 : 219,    # ref zotero eps 
                    365 : 376     # ref zotero eps 
                }[eps]
            except:
                raise KeyError(f'Inhibitor: {self.name} has no known eps: {eps}')
            self.nu       = 366e-9

        # change to function on species class
        if conc_type == 'mol':
            self.moles = conc
        elif conc_type == 'g':
            self.moles = conc/self.M
        else:
            raise ValueError(f"That input type {conc_type} is not supported")
