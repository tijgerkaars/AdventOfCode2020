
class Co_Initiator:
    
    def __str__(self):
        return f'{self.name}: {self.moles:.2e} Mol'

    def __init__(self, name, conc, conc_type):
        self.name = name
                
        if name == 'test':
            self.pmax = 1                  # max number of radicals on a monomer unit
            self.M    = 10                 # g/mol
            self.dens = 1                  # g/mL at 25 °C
            self.eps  = 1                  # M^-1 cm^-1
            self.visc = []                 # mPa s
        elif name ==  'EDAB':
            self.headers = [
                'Co_initiator_ground',
                'Exciplex',
                'Active_co_initiator',
                "Reduced_Co-Initiator"
            ]
            self.pmax    = 1                  
            self.M       = 193.24                 
            self.dens    = 1.04
            self.eps     = []
            self.visc    = []
        elif name == 'MDEA':
            self.pmax = 1                  
            self.M    = 119.163                 
            self.dens = 1.04
            self.eps  = []
            self.visc = 101

        if conc_type == 'mol':
            self.moles = conc
        elif conc_type == 'g':
            self.moles = conc/self.M
        else:
            raise ValueError(f"That input type ({conc_type}) is not supported")



if __name__ == "__main__":
    import run_main