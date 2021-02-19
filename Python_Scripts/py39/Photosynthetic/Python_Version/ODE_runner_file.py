import sys

import datetime
import numpy as np

from return_monomer_species import return_monomer_species
from plot_sol               import plot
from RRE import RRE

def print_mat(mat):
    np.set_printoptions(threshold=sys.maxsize)
    print(mat)
    np.set_printoptions(threshold = False)

class ODE_runner:
    def __init__(self, parameters, run_id=1):
        self.parameters    = parameters
        self.rates         = parameters.k
        self.monomers      = parameters.monomers
        self.error_counter = np.zeros((5,2))
        self.indexes = {}

        # print(self.rates)

        # ------ Produce small species --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        initiator = parameters.initiator
        self.small_legend  = []
        self.small_legend += initiator.headers
        self.small_system  = [initiator.moles] + [0] * (len(initiator.headers)-1)

        r_l = 0        
        r_h = len(self.small_legend)
        self.indexes['radicals' ] = [i for i in range(r_l+1,r_h-1)]
        self.indexes['initiator'] = np.arange(r_l,r_h); r_l = r_h
        self.indexes['full_init'] = self.indexes['initiator']
        if hasattr(parameters, 'co_initiator'):
            co_initiator = parameters.co_initiator
            self.small_legend.extend( co_initiator.headers)
            self.small_system.extend([co_initiator.moles] + [0]*(len(co_initiator.headers)-1) )
            
            r_h = len(self.small_legend)
            self.indexes['radicals' ].extend([i for i in range(r_l+1,r_h-1)])
            self.indexes['co_initiator'] = np.arange(r_l,r_h); r_l = r_h
            np.append(self.indexes['full_init'], self.indexes['co_initiator'])
        if hasattr(parameters,'inhibitor'):
            inhibitor = parameters.inhibitor
            self.small_legend.extend(       inhibitor.headers)
            self.small_system.extend([inhibitor.moles] + [0]*(len(inhibitor.headers)-1) )
            
            r_h = len(self.small_legend)
            self.indexes['radicals' ].extend([i for i in range(r_l+1,r_h)])
            self.indexes['inhibitor'] = np.arange(r_l,r_h); r_l = r_h
            
        self.small_legend.append('Bonds')
        self.small_system.append(0)

        self.small_legend.append('Degredation_products')
        self.small_system.append(0)

        self.small_legend.append('Oxygen')
        self.small_system.append(0)

        self.small_legend.append('Peroxides')
        self.small_system.append(0)

        for monomer in parameters.monomers:
            self.small_legend.extend(monomer.headers)
            self.small_system.extend([monomer.moles] + [0]*(len(monomer.headers)-1) )
                    
        self.indexes['small_system'] = [i for i in range( 0,len(self.small_legend) )]
        parameters.small_legend = self.small_legend
        parameters.indexes      = self.indexes
        # ------ Produce large species --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        species, valid_species, species_legend = return_monomer_species(parameters.monomers)
        valid_species
        parameters.big_legend = species_legend
        self.big_legend       = species_legend
        # w = np.where(valid_species > 0)
        # print_mat( species[w] )
        
        self.full_system_state_zero = np.append(self.small_system, species)
        self.full_system_legend     = np.append(self.small_legend, self.big_legend)

    def run(self):
        import time

        import matplotlib.pyplot as plt
        from scipy.integrate import solve_ivp
        # from scipy.integrate import odeint
        # from scipy.integrate import ode
        
        parameters = self.parameters
        # print(self.small_legend)
        t_start = time.time()
        sol = solve_ivp(RRE
                      , (0,parameters.t_span)
                      , np.copy(self.small_system)
                      , args = (parameters,)
                      , method       = parameters.RRE_method
                      , first_step   = parameters.RRE_first_step
                      , max_step     = parameters.RRE_max_step
                      , atol         = parameters.RRE_atol
                      , dense_output = parameters.RRE_dense_output
                      )
        t_end = time.time()
        parameters.run_times[parameters.run] = t_end-t_start
        """
            r = ode(lambda t,y, p=self.parameters : RRE(t,y, p)).set_integrator('zvode', method='bdf')
            r.set_initial_value(np.copy(self.small_system), 0)
            t1 = 1000
            dt = 1
            while r.successful() and r.t < t1:
                print('test', r.t+dt, r.integrate(r.t+dt))
            
                        #, (0,self.parameters.t_span)
                        #, np.copy(self.small_system)
                        #, args = (self.parameters,)
                        #, method       = self.parameters.RRE_method
                        #, first_step   = self.parameters.RRE_first_step
                        #, max_step     = self.parameters.RRE_max_step
                        #, atol         = self.parameters.RRE_atol
                        #, dense_output = self.parameters.RRE_dense_output
                        # )
            print(r)
            return
            """
        """
            t = np.linspace(0,1.2e7,1000)
            sol = odeint(RRE
                        , np.copy(self.small_system)
                        , t
                        # , method='LSODA' # Radau, BDF, or LSODA
                        , args = (self.parameters,)
                        , tfirst = True
                        #, max_step = 1e-9
                        # , dense_output=True
                        )

            import matplotlib.pyplot as plt
            plt.plot(t, sol, label=self.small_legend)
            plt.legend(loc='best')
            plt.show()
            return [0]*2
            """

        print(f'RUN_TIME: {parameters.prefix} -- {t_end-t_start:0.5f} s')
        parameters.run += 1
        return (sol, None)
        
    def show(self, sol, parameters):
        
        if parameters.show_figs["all"] or parameters.show_figs["initiator"]:
            # plot CQ_g,s,t
            plot(sol.t, sol.y, self.small_legend, self.indexes['initiator'], f"{parameters.prefix}: initiator")
        if parameters.show_figs["all"] or parameters.show_figs["co_initiator"]:
            # plot co_g,a, and ex
            plot(sol.t, sol.y, self.small_legend, self.indexes['co_initiator'], f"{parameters.prefix}: co_initiator")
        if parameters.show_figs["all"] or parameters.show_figs["inhibitor"]:
            # plot all CQ/EDAB species
            plot(sol.t, sol.y, self.small_legend, self.indexes['inhibitor'], f"{parameters.prefix}: inhibitor")
        if parameters.show_figs["all"] or parameters.show_figs["full_init"]:
            # plot in_g,r
            plot(sol.t, sol.y, self.small_legend, self.indexes['initiator']+self.indexes['co_initiator'], f"{parameters.prefix}: full_init")
        if parameters.show_figs["all"] or parameters.show_figs["radicals"]:
            # plot all radical species
            plot(sol.t, sol.y, self.small_legend, self.indexes['radicals'], f"{parameters.prefix}: radicals")
        if parameters.show_figs["all"] or parameters.show_figs["small_system"]:
            # plot full small system
            plot(sol.t, sol.y, self.small_legend, self.indexes['small_system'], f"{parameters.prefix}: small_system")
        print('sool:', sol)



if __name__ == "__main__":
    import run_main