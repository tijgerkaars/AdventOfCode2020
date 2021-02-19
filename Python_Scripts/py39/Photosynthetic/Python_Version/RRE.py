import numpy as np



def RRE(t:'solve_ivp_timestep', state_n_s:'np_1darray', parameters:'parameter_struct') -> 'np_1darray_dt':
    """
    t:         Time
    state_n:   1D-numpy array for each species to be considered
    Paramters: Parameters with info on the system for readability

    [ 'Initiator_ground state', 'Initiator_Singlet state', 'Initiator_Triplet state', 
    'Reduced_Initiators', 'Co_initiator', 'Exciplex', 'Active_co_initiator', 
    'Reduced_Co-Initiator', 'Inhibitor', 'Inhibitor_radical', 'consumed_Inhibitor', 
    'Polymer', 'PEGDA', 'PEGDA-radical', 'Degredation_products']
    """
    k        = parameters.k
    monomers = parameters.monomers
    
    next_state_small = np.zeros_like(state_n_s)

    # Order of indexed species 
    # Initiator_ground state, Initiator_Singlet state, Initiator_Triplet state, 
    # Initiator_Reduced, Co_initiator, Exciplex, Active_co_initiator, 
    # Reduced_Co-Initiator, Inhibitor, Inhibitor_radical, consumed_Inhibitor, 
    # Polymer, Monomer, Monomer-radical, Degredation_products]

    # Assign array index to species name, centralize update location if array order changes
    # Increased readability for ODE's

    i_ = 0
    IN_g =  i_; i_ += 1 # (In)itiator_(g)round_state
    IN_s =  i_; i_ += 1 # (In)itiator_(S)inglet_state
    IN_t =  i_; i_ += 1 # (In)itiator_(T)riplet_state   # NOTE for consitency maybe change to IN_ta or IN_a as it is the active radical species
    IN_r =  i_; i_ += 1 # (In)itiator_(R)educed
    Co_g =  i_; i_ += 1 # Co_initiator_ground
    EX   =  i_; i_ += 1 # Exciplex : Excited-complex of Initiator and Co-initiator
    CO_a =  i_; i_ += 1 # Active_co_initiator
    CO_r =  i_; i_ += 1 # Reduced_Co-Initiator
    IH_g =  i_; i_ += 1 # Inhibitor_ground
    IH_a =  i_; i_ += 1 # Inhibitor_radical
    IH_r =  i_; i_ += 1 # Inhibitor_reduced
    Bond =  i_; i_ += 1 # Bonds
    D    =  i_; i_ += 1 # Degredation products   # NOTE for O2 degredation but no rate references were found, Logic left inplace
    Ox   =  i_; i_ += 1 # Oxygen
    Pox  =  i_; i_ += 1 # Perpoxide
    sn   = np.arange(i_, i_+(2*len(monomers)), 2); i_ += 1 # Vinyl groups
    sp   = np.arange(i_, i_+(2*len(monomers)), 2); i_ += 1 # Radicals groups

    # I ground
    next_state_small[IN_g] =( -k.Igs    * state_n_s[IN_g]    # excitation  G  -> S 
                              +k.Isg    * state_n_s[IN_s]    # relaxation  S  -> G
                              +k.Itg    * state_n_s[IN_t]    # relaxation  T  -> G
                              +k.Edeact * state_n_s[ EX ] )  # relaxation  Ex -> G
    # I singlet                          
    next_state_small[IN_s] =( +k.Igs    * state_n_s[IN_g]    # excitation  G -> S
                              -k.Isg    * state_n_s[IN_s]    # relaxation  S -> G
                              -k.Ist    * state_n_s[IN_s] )  # excitation  S -> T
    # I Triplet    
    next_state_small[IN_t] =( +k.Ist    * state_n_s[IN_s]    # excitation  S      -> T
                              -k.Itg    * state_n_s[IN_t]    # relaxation  T      -> G
                              -k.Eform  * state_n_s[Co_g]    #   
                                        * state_n_s[IN_t] )  # combination T + Co -> Ex
    # I reduced 
    next_state_small[IN_r] =( +k.Eact   * state_n_s[ EX ] )  # activation   Ex -> CQrH

    # Co ground   
    next_state_small[Co_g] =( next_state_small[Co_g]
                              -k.Eform  * state_n_s[Co_g]    # excitation   IN-T + Co -> Ex
                                        * state_n_s[IN_t]    #
                              +k.Edeact * state_n_s[ EX ] )  # relaxation   Ex       -> I-g + Co
    # Ex         
    next_state_small[ EX ] =( +k.Eform  * state_n_s[Co_g]    #  
                                        * state_n_s[IN_t]    # combination  T + Co -> Ex
                              -k.Eact   * state_n_s[ EX ]    # activation   Ex     -> CQrH + Co-radical
                              -k.Edeact * state_n_s[ EX ] )  # deactivation Ex     -> CQ + Co
    # activated Co
    next_state_small[CO_a] =( next_state_small[CO_a]
                              +k.Eact   * state_n_s[ EX ] )  # activation   Ex -> Co-radical  
    
    # Used up Co_initiator
    next_state_small[CO_r] = sum( # k values are floats but Pinit is np.array for monomer mixtures
                              +k.Pinit  * state_n_s[CO_a]    # activation   Co-r + V -> POLr
                                        * state_n_s[ sn ] )  #

    # Inhibitor
    next_state_small[IH_g] =(-k.IHgr  * 1 * state_n_s[IH_g]      # light induced split  
                             +k.IHrg  * 1 * state_n_s[IH_a] )    # recombination
    # Inhibitor radical  
    next_state_small[IH_a] =(+k.IHgr  * 2 * state_n_s[IH_g]      # ligth induced split       ----> InHibitor specific reactions
                              -k.IHrg * 2 * state_n_s[IH_a]      # recombination             --/
                              -k.IHpol* 2 * state_n_s[IH_a]      #                           ----> InHibitor system reactions
                                          * sum(state_n_s[sp]) ) # polymer radical termination through inhibitor
                                        
    # loop through Monomers in mixture
    for i, monomer_i in enumerate(monomers):
        kinit = monomer_i.K.init

        # Co_initiator-rad used by Initiation
        next_state_small[CO_a]  = (next_state_small[CO_a]      #  activation   Co-r + V -> POLr + CO_r
                                  -kinit * state_n_s[CO_a ]    #  - CO_a / - V
                                         * state_n_s[sn[i]] )  #  + POLr / + CO_r
                            
        # Production of reduced Co_initiator
        next_state_small[CO_r]  = (next_state_small[CO_r]      #  
                                  +kinit  * state_n_s[CO_a ]   # 
                                          * state_n_s[sn[i]] ) #
                            
        # The 'consumption' of vinyl by reaction of vinyl with initiator                       
        next_state_small[sn[i]] =(next_state_small[sn[i]]      #
                                  -kinit  * state_n_s[CO_a]    # 
                                          * state_n_s[sn[i]] ) #

        # Vinyl i is consumed by reaction with radical j
        for j, monomer_j in enumerate(monomers):
            kprop_ji = monomer_j.K.prop / monomer_j.K.Rij[f'R{monomer_j.tag}{monomer_i.tag}']

            sni_conc_change =(kprop_ji * state_n_s[ sp[j] ]       # rad   j
                                       * state_n_s[ sn[i] ] )     # vinyl i    
                                
            next_state_small[ sp[j] ] =(next_state_small[ sp[j] ] # - rad j 
                                      - sni_conc_change )         #  
            next_state_small[ sn[i] ] =(next_state_small[ sn[i] ] # - mon i
                                      - sni_conc_change )         #  
            next_state_small[ sp[i] ] =(next_state_small[ sp[i] ] # + rad i
                                      + sni_conc_change )         #  


            """
                %{          NOTE : Edited out for some reason?      
                % radical i is consume by reaction with vinyl j
                
                kprop_ij = monomer.K.prop / monomer.K.(['R', tags(i), tags(j)]);
                spi_conc_change = kprop_ij * state_n( sp(i) ) ...
                                        * state_n( sn(j) );  %
                
                next_state( sp(i) ) = next_state( sp(i) )     ... - rad i
                                    - spi_conc_change;          %
                next_state( sn(j) ) = next_state( sn(j) )     ... - mon j
                                    - spi_conc_change;          %
                next_state( sp(j) ) = next_state( sp(j) )     ... + rad j
                                    + spi_conc_change;          %
                %}       
                """

            # The 'production'  of bonds by propogation
            next_state_small[Bond]    =(next_state_small[Bond]    #
                                      + 2 * sni_conc_change )     # the increase in bonds by this monomer attacking

        next_state_small[sp[i]] =(next_state_small[sp[i]]         #
                                - monomer_i.K.tr                  # recombination
                                  * sum(state_n_s[sp])            # - the sum of all all the radical species
                                  * state_n_s[ sp[i] ]            # - the radcials of this species
                                  * 2                             # 
                                - monomer_i.K.td                  # disproportionation
                                  * sum(state_n_s[sp])            #
                                  * state_n_s[ sp[i] ]            #
                                  * 2                             #
                                - k.IHpol                         # Inhibition
                                  * state_n_s[ sp[i] ]            #
                                  * state_n_s[IH_a]               #
                                + kinit                           # The 'production'  of POLr by reaction of vinyl with initiator
                                  * state_n_s[CO_a]               # 
                                  * state_n_s[sn[i]] )            #

        next_state_small[Bond]  =(next_state_small[Bond]          #
                                + monomer_i.K.tr                  # recombination rate
                                  * sum(state_n_s[sp])            # the totatal radical concentration
                                  * state_n_s[ sp[i] ]            # the concentration of radicals on this monomer
                                  * 2 )                           # 2 half bonds
        next_state_small[IH_r]  =(next_state_small[IH_r]          #
                                + k.IHpol * 2                     # Inhibition
                                  * state_n_s[ sp[i] ]            #
                                  * state_n_s[ IH_a  ] )          #

    """ Unused, since Oxygen concentration is always 0 """ 
    # Oxygen
    next_state_small[ Ox ] =(-k.Oop * state_n_s[IN_t]
                                    * state_n_s[ Ox ] )
    # Peroxide
    next_state_small[Pox ] =(+k.Oop * state_n_s[IN_t]
                                    * state_n_s[ Ox ] )
    # Oxigen degredation of radicals                                    
    next_state_small[ D  ] =(+k.Oop * state_n_s[IN_t]
                                    * state_n_s[ Ox ] )
    # w = np.where(next_state_small < parameters.RRE_allowed_error)
    # next_state_small[w] = np.absolute(next_state_small[w])
    """"""
    return next_state_small
                           


if __name__ == "__main__":
    import run_main