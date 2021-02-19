import numpy as np
class Rates:
    def __init__(self, parameters):
        """ Returns an objects holding all the rates for the ODE's based on the input parameters"""
        self.current_dirs =None; self.current_dirs = set(dir(self))
        initiator = parameters.initiator
        inhibitor = parameters.inhibitor
        monomers  = parameters.monomers

        nA = 6.023e23  # Avagadro's number
        c  = 2.998e8   # speed of light
        h  = 6.626e-34 # plancs constant

        E_Initiator_photon  =   nA*h*c/initiator.nu # JK E = N_A*h*c/lambda
        I_light             =   parameters.init_intensity # mW / cm^2
        phi                 =   1 # #NOREF# initiator concentration?   # G&B
        eps                 =   36.5*2.3  # Oce  == monomer.eps_458 ?  # TODO pylint: disable = unused-variable

        ## ref 2 eq 8 -> Ri = eps*I*[Initator] / E'
        #  E' is the energy per mole of photons

        Igs         =   initiator.eps * phi * I_light/E_Initiator_photon # TODO pylint: disable = unused-variable

        #% formation of active species from Photo-Initiator (CQ) and Co-Initiator
        # rates in form: k . (I)nitiator (g)round to (s)inglet
        #self.Igs = 2.303 * I0 * epsi(I)

        self.Igs = Igs                    # #ref 2#  CQ-Ground  -> CQ-Singlet
        self.Isg = 1.7e5                  # #ref 1, p.5222#  CQ-Singlet -> CQ-Ground
        self.Ist = 1/19                   # #ref 3, p.2584#  CQ-Singlet -> CQ-Triplet
        self.Ideg =0                      # #NOREF#  degredation (/oxidation only?)

        a = 0                       # #NOREF#  small a means small loss of initator through degredation(/oxidation/peroxide formation?)
        self.Itg = (1-a) * self.Ideg      #          (1-a)k3  CQ-Triplet -> CQ-Ground              #quenching
        self.Ilost =  a  * self.Ideg      #          ak3      CQ-Triplet -> degredation products

        ## self.ItgM physical quenching by the monomer 
        # beta  = factor that becomes active species
        # gamma = factor that losses radical and returns to ground state
        # 1-beta-gamma = loss of I and CoI through degredation

        beta = 0.5; gamma = 0.5 

        self.Ite = 2.0e8                  # CQ-triplet -> singlet-exciplex
        self.Ise = 1.5e9                  # CQ-singlet -> triplet-exciplex

        self.Eform = self.Ite
        self.Eact = beta * self.Eform             #          Active species formation
        self.Edeact = gamma * self.Eform          #          Deactivation
        self.Elost = (1-beta-gamma) * self.Eform  #          Degredation products

        #% Inhibitor

        E_inhibitor_photon       =   nA*h*c/inhibitor.nu       # JK E = N_A*h*c/lambda
        I_light_inhi             =   parameters.inhi_intensity # mW / cm^2
        phi_inhi                 =   1                         #NOREF# inhibitor concentration?    % G&B

        IHgr                     =   inhibitor.eps * phi_inhi * I_light_inhi/E_inhibitor_photon

        self.IHgr  = IHgr     # IN-ground   -> 2 IN-r
        self.IHrg  = 10 / 2   # 2 + IN-r    -> IN-ground
        self.IHpol = max(monomers, key= lambda m : m.K.prop).K.prop * 100 # NOREF     # POLr + IN-r -> POL-IN

        # polymer initation
        # Active Co_initiator with vinylgroups
        self.Pinit = np.array([monomer.K.init for monomer in monomers])

        # CQ-Triplet + O2 -> CQ-OO' k = 2 * 10^8 #ref 1/3#
        self.Oop = 2e8 #  #ref 1#

    
    def __str__(self) -> 'str' :
        """ Human readable string"""
        string = ''
        for each in set(dir(self))-self.current_dirs:
            p = eval(f'self.{each}')
            try:
                string += f'{each}: {p:.2e}\n'
            except:
                string += f'{each}: {p}\n'
        return string


if __name__ == "__main__":
    import run_main