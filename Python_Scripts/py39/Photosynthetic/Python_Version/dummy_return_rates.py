
class Rates:
    def __init__(self, parameters):
        
        initiator = parameters.initiator

        nA = 6.023e23  # Avagadro?s number
        c  = 2.998e8   # speed of light
        h  = 6.626e-34 # plancs constant

        E_Initiator_photon  =   nA*h*c/initiator.nu # JK E = N_A*h*c/lambda
        I_light             =   100 # mW / cm^2
        phi                 =   1 # #NOREF# initiator concentration?   # G&B
        eps                 =   36.5*2.3  # Oce  == monomer.eps_458 ?  # TODO pylint: disable = unused-variable

        ## ref 2 eq 8 -> Ri = eps*I*[Initator] / E'
        #  E' is the energy per mole of photons

        Igs         =   initiator.eps * phi * I_light/E_Initiator_photon # TODO pylint: disable = unused-variable

        #% formation of active species from Photo-Initiator (CQ) and Co-Initiator
        # rates in form: k . (I)nitiator (g)round to (s)inglet
        #self.Igs = 2.303 * I0 * epsi(I)

        self.Igs = 10                  # #ref 2#  CQ-Ground  -> CQ-Singlet
        self.Isg = 0                   # #ref 1, p.5222#  CQ-Singlet -> CQ-Ground
        self.Ist = 10                  # #ref 3, p.2584#  CQ-Singlet -> CQ-Triplet
        self.Ideg = 0                          # #NOREF#  degredation (/oxidation only?)

        a = 0                       # #NOREF#  small a means small loss of initator through degredation(/oxidation/peroxide formation?)
        self.Itg = (1-a) * self.Ideg      #          (1-a)k3  CQ-Triplet -> CQ-Ground              #quenching
        self.Ilost =  a  * self.Ideg      #          ak3      CQ-Triplet -> degredation products

        ## self.ItgM physical quenching by the monomer 
        # beta  = factor that becomes active species
        # gamma = factor that losses radical and returns to ground state
        # 1-beta-gamma = loss of I and CoI through degredation

        beta = 0.5; gamma = 0.5 

        self.Ite = 50                  # CQ-triplet -> singlet-exciplex
        self.Ise = 5                  # CQ-singlet -> triplet-exciplex

        self.Eform = self.Ite
        self.Eact = beta * self.Eform             #          Active species formation
        self.Edeact = gamma * self.Eform          #          Deactivation
        self.Elost = (1-beta-gamma) * self.Eform  #          Degredation products

        #% Inhibitor

        self.IHgr  = 100 if parameters.inhi_intensity != 0 else 0     # IN-ground   -> 2 IN-r
        self.IHrg  = 5      # 2 + IN-r    -> IN-ground
        self.IHpol = 100     # POLr + IN-r -> POL-IN
        

        #% formation of polymer

        self.Pinit = 20  # Eact + V    -> POLr
        self.Pprop = 10 # POLr + V    -> POLr + B
        self.Ptr = 5    # POLr + POLr -> B
        self.Ptd = 1    # POLr + POLr -> POL + POL

        #% Interaction with Oxygen

        self.Oop = 2e8 #  #ref 1#



if __name__ == "__main__":
    import run_main