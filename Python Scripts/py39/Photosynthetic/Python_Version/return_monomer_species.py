import numpy as np


def return_monomer_species(monomers, setup=True):
    nmonomers = len(monomers)
    vmax = max(monomers, key= lambda m : m.vmax).vmax +1    # max vinyl groups ----- # +1 since range should be inclusive e.g. monomer with vmax=2 can have 0,1, or 2 vinyl groups
    pmax = max(monomers, key= lambda m : m.pmax).pmax +1    # max radicals
    nmax = max(monomers, key= lambda m : m.nmax).nmax +1    # max bonds (2*vmax)

    temp_species_name = f'{nmonomers}{vmax}{pmax}{nmax}{nmax}{nmax}'
    max_name_length = f'S{len(temp_species_name)}' # for cases with 5+ vinyl groups or mixtures of 10+ monomers

    # overall max used for matrix to appeace the numpy gods of matrix concatenation
    species = np.zeros((nmonomers, vmax, pmax, nmax, nmax, nmax)) # 3*nmax for 3 bonds b_in,b_out,b_neutral
    if setup:
        valid_species = np.zeros((nmonomers, vmax, pmax, nmax, nmax, nmax))
        header        = np.empty((nmonomers, vmax, pmax, nmax, nmax, nmax), dtype=(max_name_length)) # 3*nmax for 3 bonds bin,bout,bneutral

    for i, monomer in enumerate(monomers):
        species[i,monomer.vmax,0,0,0,0] = monomer.moles # set starting concentrations
        if not setup: # since valid monomer species and headers don't change we only have to look at them the first time
            continue
        for v in range(monomer.vmax +1):        # +1 since range should be inclusive e.g. monomer with vmax=2 can have 0,1, or 2 vinyl groups
            for p in range(monomer.pmax +1):
                for b_in in range(monomer.nmax +1):
                    for b_out in range(monomer.nmax +1):
                        for b_neutral in range(monomer.nmax +1):
                            header[i,v,p,b_in,b_out,b_neutral] = f'{i}{v}{p}{b_in}{b_out}{b_neutral}'
                            b_tot = b_in + b_out + b_neutral
                            """
                            if (v*2 + p + b_tot <= monomer.nmax and
                                monomer.vmax - v == b_in and
                                b_in - (b_out + b_neutral) == p):
                            """
                            if (  v*2 + p + b_tot <= monomer.nmax and
                                              p+v <= monomer.vmax and
                                b_out + b_neutral <= monomer.vmax and
                                             b_in <= monomer.vmax and
                                         b_in + v >= monomer.vmax   ): # (true || monomer.vmax - (v-1) <= (b_in -1)) ???
                                valid_species[i,v,p,b_in,b_out,b_neutral] = 1

    species = np.reshape(species, -1)
    if setup:
        valid_species = np.reshape(valid_species, -1)
        header        = np.reshape(header, -1)
        return species, valid_species, header
    else:
        return species










if __name__ == "__main__":
    import run_main