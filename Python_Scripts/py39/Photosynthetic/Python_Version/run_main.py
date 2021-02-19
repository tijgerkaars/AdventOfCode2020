import datetime
import numpy as np

from parameter_file      import Parameters
from ODE_runner_file     import ODE_runner
from choose_initiator    import Initiator
from choose_co_initiator import Co_Initiator
from choose_inhibitor    import Inhibitor
from choose_monomer      import Monomer
from return_rates        import Rates
# from dummy_return_rates  import Rates

from plot_system         import plot_system
from plot_conv           import plot_conv
from plot_series         import plot_series

starting_time = datetime.datetime.now()
figures = 0
marker = False

# ------------------------------------------------------------------------------------

parameters = Parameters()
parameters.total_runs = 1
parameters.show_figs={
    'all'           : False,
    'initiator'     : False,
    'co_initiator'  : False,
    'full_init'     : False,
    'inhibitor'     : False,
    'radicals'      : False,
    'small_system'  : False,
    'tests'         : True,
}
parameters.run_tests={
    'all'                  : False,
    'no light'             : False,
    'only init light'      : True,
    'only inhib light'     : False,
    'init == inhib light'  : False,
    'init >> inhib light'  : False,
    'init << inhib light'  : False,
    'prop rate range'      : False,
    'prop rate range long' : False,
}
parameters.run_times = {'Inital_time' : starting_time}
parameters.prefix    =  'test_run'
parameters.file_loc  = ''

# ------------------------------------------------------------------------------------

parameters.t_span = 3_000 # 2e7# 226

parameters.init_intensity = 10
parameters.init_nu        = 458

parameters.inhi_intensity = 0
parameters.inhi_nu        = 366

mixture_weight = 100
parameters.conc_inp = ['w%', 'g', 'mol'][0]
parameters.monomers = ['PEGDA']

parameters.initiator    = 'CQ'      
parameters.co_initiator = 'EDAB'      
parameters.inhibitor    = 'o-Cl-HABI'

conc_CQ      = 5
conc_EDAB    = 0.5 * conc_CQ
conc_HABI    = 1
conc_monomer = [100 - (conc_CQ+conc_EDAB+conc_HABI)]


# ------------------------------------------------------------------------------------

"""
# index 0 are the default arguments, needed for unpacking in ODE_solv function
"""
parameters.RRE_method        = ['RK45', 'Radau', 'BDF'  ][2]
parameters.RRE_first_step    = [None,   1e-9,           ][1]
parameters.RRE_max_step      = [np.inf, 10  ,           ][1]
parameters.RRE_atol          = [1e-6,   1e-9,           ][1]
parameters.RRE_rtol          = [1e-3,   1e-6,           ][1]
parameters.RRE_dense_output  = [False,  True,           ][0]
# parameters.RRE_allowed_error = 1e-15

# ------------------------------------------------------------------------------------

# changes chosen input (mol%,grams, or mol already) to moles
mol_calc = {
    'w%'  : lambda c,w : (w*(c/100), 'g'),
    'g'   : lambda c,w : (c, 'g'),
    'mol' : lambda c,w : (c, 'mol')
}

conc_CQ, conc_EDAB, conc_HABI = [mol_calc[parameters.conc_inp](each, mixture_weight) for each in (conc_CQ, conc_EDAB, conc_HABI)]
conc_monomer                  = [mol_calc[parameters.conc_inp](each, mixture_weight) for each in conc_monomer]


parameters.initiator    = Initiator(   parameters.initiator,    *conc_CQ,   parameters.init_nu)
parameters.co_initiator = Co_Initiator(parameters.co_initiator, *conc_EDAB)
parameters.inhibitor    = Inhibitor(   parameters.inhibitor,    *conc_HABI, parameters.inhi_nu)

# parameters.oxygen.conc    = 0

parameters.monomers = [Monomer(monomer, *conc_monomer[i]) for i,monomer in enumerate(parameters.monomers)]
parameters.k        =  Rates(parameters)

# ------------------------------------------------------------------------------------
# NOTE implement plotting
# NOTE Testcases
# NOTE test polymerization rates range
base_init_intensity = parameters.init_intensity
base_inhi_intensity = parameters.inhi_intensity
if parameters.run_tests['all'] or parameters.run_tests['no light']:
    parameters.prefix = 'no light'
    parameters.init_intensity = 0
    parameters.inhi_intensity = 0
    parameters.k = Rates(parameters)
    runner = ODE_runner(parameters)
    results, *warnings = runner.run()

    # print(parameters)
    # print('\n'*3 + '-'*100)
    plot_system(results, parameters)
    plot_conv(results, parameters, parameters.prefix)
if parameters.run_tests['all'] or parameters.run_tests['only init light']:
    parameters.prefix = 'only init light'
    parameters.init_intensity = 100000
    parameters.inhi_intensity = 0
    parameters.k = Rates(parameters)

    runner = ODE_runner(parameters)
    results, *warnings = runner.run()
    
    # print(parameters)
    plot_system(results, parameters)
    plot_conv(results, parameters, parameters.prefix)
if parameters.run_tests['all'] or parameters.run_tests['only inhib light']:
    parameters.prefix = 'only inhib light'
    parameters.init_intensity = 0
    parameters.inhi_intensity = 10000
    parameters.k = Rates(parameters)
    runner = ODE_runner(parameters)
    results, *warnings = runner.run()
    
    plot_system(results, parameters)
    plot_conv(results, parameters, parameters.prefix)
if parameters.run_tests['all'] or parameters.run_tests['init == inhib light']:
    parameters.prefix = 'init == inhib light'
    parameters.init_intensity = 10000
    parameters.inhi_intensity = 10000
    parameters.k = Rates(parameters)

    runner = ODE_runner(parameters)
    results, *warnings = runner.run()
    
    plot_system(results, parameters)
    plot_conv(results, parameters, parameters.prefix)
if parameters.run_tests['all'] or parameters.run_tests['init >> inhib light']:
    parameters.prefix = 'init bigger than inhib light'
    parameters.init_intensity = 10000
    parameters.inhi_intensity = 10
    parameters.k = Rates(parameters)
    runner = ODE_runner(parameters)
    results, *warnings = runner.run()
    
    plot_system(results, parameters)
    plot_conv(results, parameters, parameters.prefix)
if parameters.run_tests['all'] or parameters.run_tests['init << inhib light']:
    parameters.prefix = 'init smaller than inhib light'
    parameters.init_intensity = 10
    parameters.inhi_intensity = 10000
    parameters.k = Rates(parameters)
    runner = ODE_runner(parameters)
    results, *warnings = runner.run()
    
    plot_system(results, parameters)
    plot_conv(results, parameters, parameters.prefix)

parameters.init_intensity = base_init_intensity
parameters.inhi_intensity = base_inhi_intensity

if parameters.run_tests['all'] or parameters.run_tests['prop rate range']:
    parameters.prefix = 'prop rate range'
    parameters.t_span = 3_000
    parameters.k = Rates(parameters)
    # prop_ranges = [i for i in range(-10,11, 2)]
    prop_ranges = [i for i in range(-10,11, 2)]
    test_results = []
    labels       = []
    base_k = parameters.monomers[0].K.prop
    fname_marker_base = f'prop_test_t{parameters.t_span}_'
    r0 = parameters.run
    for rate in prop_ranges:
        #parameters.monomers[0].K.prop = base_k*(1+(rate/10))
        parameters.monomers[0].K.prop = base_k*(1+(rate/10))
        runner = ODE_runner(parameters)
        results, *warnings = runner.run()
        test_results.append(results)
        fname_marker = fname_marker_base + f'{parameters.run}'
        labels.append(f"Rate={parameters.monomers[0].K.prop:2.3e}")
        # plot_system(results, parameters, f'{parameters.prefix}: {parameters.monomers[0].K.prop}', fname_marker)
        # plot_conv(  results, parameters, f'{parameters.prefix}: {parameters.monomers[0].K.prop}', fname_marker)
    
    parameters.monomers[0].K.prop = base_k
    
    plot_series(  test_results, parameters, labels, f'{parameters.prefix}', f"{fname_marker}_{r0}-{r0+len(prop_ranges)}")

if parameters.run_tests['all'] or parameters.run_tests['prop rate range long']:
    parameters.prefix = 'prop rate range long'
    parameters.t_span = 4_000_000
    parameters.init_intensity = 10000
    parameters.inhi_intensity = 0
    parameters.k = Rates(parameters)
    # prop_ranges = [i for i in range(-10,11, 2)]
    prop_ranges = [i for i in range(-10,11, 2)]
    test_results = []
    labels       = []
    base_k = parameters.monomers[0].K.prop
    fname_marker_base = f'prop_test_t{parameters.t_span}_'
    r0 = parameters.run
    for rate in prop_ranges:
        #parameters.monomers[0].K.prop = base_k*(1+(rate/10))
        parameters.monomers[0].K.prop = base_k*(1+(rate/10))
        runner = ODE_runner(parameters)
        results, *warnings = runner.run()
        test_results.append(results)
        fname_marker = fname_marker_base + f'{parameters.run}'
        labels.append(f"Rate={parameters.monomers[0].K.prop:2.3e}")
        # plot_system(results, parameters, f'{parameters.prefix}: {parameters.monomers[0].K.prop}', fname_marker)
        # plot_conv(  results, parameters, f'{parameters.prefix}: {parameters.monomers[0].K.prop}', fname_marker)
    
    parameters.monomers[0].K.prop = base_k
    
    plot_series(  test_results, parameters, labels, f'{parameters.prefix}', f"{fname_marker}_{r0}-{r0+len(prop_ranges)}")
    











parameters.run_times['Final_Time'] = datetime.datetime.now()

print( parameters.run_times['Final_Time'] - parameters.run_times['Inital_time'] )