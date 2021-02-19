

class Initiator:
    def __init__(self, name, conc, conc_type, eps):
        """
        TODO change dictionary selection structure to database load:
            - JSON probably
            - maybe use pandas or pickle
        TODO : Add species class for inhertince
        TODO : add __str__/__repr__
        """
        self.name  = name
        { # placeholder, change to database load later
            'test' : self.return_test,
            'CQ'   : self.return_CQ
        }[name](eps)
        conc_types = {'mol', 'g'}
        if conc_type not in conc_types:
            raise ValueError(f"Concentartion notation type ({conc_type}) isn't known. Should be in {conc_types}")
        self.moles = conc if conc_type == 'mol'  else conc/self.M
    
    def __str__(self):
        return f'{self.name}: {self.moles:.2e} Mol'

    def return_test(self, eps):
        self.state = 'Imaginary'
        self.pmax     = 1       # max number of radicals on a monomer unit
        self.M        = 10      # g/mol
        self.dens     = -1      # g/mL at 25 °C
        self.eps      = 1       # M^-1 cm^-1 || cm^−1 /(mol/L)
        self.nu       = -100    # wavelength nm

    def return_CQ(self, eps):
        """ placeholder function  at later point change this to a database load """
        self.headers  = [
            "Initiator_ground_state",
            "Initiator_Singlet_state",
            "Initiator_Triplet_state",
            "Initiator_Reduced"
        ]
        self.state    = 'Solid'
        self.pmax     = 4                  
        self.M        = 166.22                 
        self.dens     = []
        try :
            self.eps = {
                458 : 40.0,
                469 : 46.0,
                405 : 6.8,
                365 : 2.05
            }[eps]
        except:
            raise KeyError(f'Initiator: {self.name} has no known eps: {eps}')
        self.nu       = eps*1e-9

    



if __name__ == "__main__":
    import run_main