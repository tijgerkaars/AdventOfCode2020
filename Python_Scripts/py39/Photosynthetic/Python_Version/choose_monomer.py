class K:
    def __init__(self):
        self.current_dirs = None
        self.current_dirs = set(dir(self))
        pass
    
    def __str__(self):
        string = ''
        for each in set(dir(self))-self.current_dirs:
            param = f'self.{each}'
            string += f'{each}: {eval(param)}\n'
        return string

class Monomer:
    tags = [i+1 for i in range( 7 )] +[-1]
    def __repr__(self):
        return f'{self.name}: {self.moles:.2e} Mol'
    def __str__(self):
        return self.name
    def __init__(self, name, conc,conc_type, kdummy = 1e4):
        self.K = K()
        if name in ('test', '-1'):
            self.name   = 'test'           # store the monomer for graphs etc
            self.tag    = '-1'             # numerical tag to make picking the Rij easier
            self.vmax   = 2                # max number of vinyl groups in monomer
            self.pmax   = 2                # max number of radicals on a monomer unit
            self.nmax   = 2 * self.vmax    # max number of bonds per monomer unit
            self.M      = 50               # g/mol
            self.dens   = 1                # g/mL at 25 °C
            self.K.init = 7*kdummy
            self.K.prop = kdummy           # the propogation rate of this monomer
            self.K.tr   = kdummy           # the recombination termination rate of this monomer
            self.K.td   = kdummy           # the disproportionation termination rate of this monomer
        elif name in ('BPAEDA', '1'):
            self.name   = 'BPAEDA'
            self.tag    = '1'
            self.vmax   = 2
            self.pmax   = 2
            self.nmax   = 2 * self.vmax
            self.M      = 688
            self.dens   = 1.15
            self.K.init = 7*kdummy
            self.K.prop = 7*kdummy
            self.K.tr   = 100*kdummy
            self.K.td   = 100*kdummy
        elif name in ('TEGDMA', '2'):
            self.name   = 'TEGDMA'
            self.tag    = '2'
            self.vmax   = 2
            self.pmax   = 2
            self.nmax   = 2 * self.vmax
            self.M      = 286.32
            self.dens   = 1.092
            self.K.init = 7*kdummy
            self.K.prop = 7*kdummy
            self.K.tr   = 100*kdummy
            self.K.td   = 100*kdummy
        elif name in ('bisGMA', '3'):
            self.name   = 'bisGMA'
            self.tag    = '3'
            self.vmax   = 2
            self.pmax   = 2
            self.nmax   = 2 * self.vmax
            self.M      = 512.59
            self.dens   = 1.161
            self.K.init = 5*kdummy
            self.K.prop = 1*kdummy
            self.K.tr   = 100*kdummy
            self.K.td   = 100*kdummy
        elif name in ('TEGDVE','4'):
            self.name   = 'TEGDVE'
            self.tag    = '4'
            self.vmax   = 2
            self.pmax   = 2
            self.nmax   = 2 * self.vmax
            self.M      = 202.25
            self.dens   = 0.99
            self.K.init = 5*kdummy
            self.K.prop = 1*kdummy
            self.K.tr   = 100*kdummy
            self.K.td   = 100*kdummy
        elif name in ('NPM', '5'):
            self.name   = 'NPM' # N-Propylmaleimide
            self.tag    = '5'
            self.vmax   = 1
            self.pmax   = 1
            self.nmax   = 2 * self.vmax
            self.M      = 139.15
            self.dens   = 1.112
            self.K.init = 3*kdummy
            self.K.prop = 3*kdummy
            self.K.tr   = 100*kdummy
            self.K.td   = 100*kdummy
        elif name in ('PEGDA', '6'):
            self.name   = 'PEGDA'
            self.header = [self.name, f'{self.name}_radical']
            self.tag    = '6'
            self.vmax   = 2
            self.pmax   = 2
            self.nmax   = 2 * self.vmax
            self.M      = 360.18
            self.dens   = 1.11
            self.K.init = 5.787e+05 #  L/mol s %% rmg
            self.K.prop = 2.878e+04 # + 227.6 + 250.5 % L/mol s %% rmg 1!: R 173, 174, 196
            self.K.td   = 4.3955e7
            self.K.tr   = 4.3955e7
            # monomer.K.tr   = 8.658e+8  % L/mol s %% rmg
            # monomer.K.td   = 1.21e+9   % L/mol s %% rmg RMG 1: R 291
        elif name in ('HDDA', '7'):
            self.name   = 'HDDA'
            self.tag    = '7'
            self.vmax   = 2
            self.pmax   = 2
            self.nmax   = 2 * self.vmax
            self.M      = 226.27
            self.dens   = 1.01
            self.K.init = 6.1197e4
            self.K.prop = 6.1197e4
            self.K.tr   = 4.3955e7
            self.K.td   = 4.3955e7
        else:
            raise ValueError(f'This monomer ({name}) has not yet been added, did you type it right dummy?')
        self.K.Rij  = {f'R{self.tag}{i}' : 1 for i in Monomer.tags}


        # change to function on species class
        if conc_type == 'mol':
            self.moles = conc
        elif conc_type == 'g':
            self.moles = conc/self.M
        else:
            raise ValueError(f"That input type {conc_type} is not supported")


        self.headers = (self.name, f'{self.name}-radical')






if __name__ == "__main__":
    import run_main