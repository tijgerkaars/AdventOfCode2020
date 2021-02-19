function next_state = RRE(t, state_n, parameters)
%RRE takes state n to state n+1
%{

% reaction pathways from: Polymer 44 (2003) 5219–5226
- Exciplex singlet left out, since near unity conversion of CQ-singlet to
CQ-triplit leaves the contribution insignificant

- Reactants -> products, SpeciesConcentration difference -- pathway? 
state_zero:
1 = CQ-ground state
- CQ-G -> CQ-S,                   v = -1  -- excitation
- CQ-S -> CQ-G,                   v = +1  -- recombination?
- CQ-T -> CQ-G,                   v = +1  -- relaxation
- E    -> CQ + Co                 v = +1  -- recombination
2 = Co-Initiator
- CQ-T + Co -> Exciplex,          v = -1
-%CQ-T + Co -> CQrH + Cor ?
- Exciplex  -> CQ + Co,           v = +1
3 = CQ-Singlet
- CQ + hv -> CQ-S,                v = +1
- CQ-S    -> CQ-G,                v = -1
- CQ-S    -> CQ-T,                v = -1
4 = CQ-Triplet
- CQ-S      -> CQ-T,              v = +1 -- excitation
- CQ-T      -> CQ,                v = -1 -- relaxation
- CQ-T + co -> Ex,                v = -1 -- combination
- CQ-T      -> DegPro,            v = -1 -- degredation
5 = Exciplex
- CQ-T + co -> Ex               , v = +1
- Ex        -> CQrH + Co-radical, v = -1
- Ex        -> CQ + Co          , v = -1
- Ex        -> DegPro           , v = -1
6 = Singly reduced Initiator species
- Ex        -> CQrOOH,              v = +1
7 = Active Co-initiator species
- Ex        -> Co-radical,        v = +1
- Co-r + V  -> POLr               v = -1
8 = degredation products
- CQ-T -> DegPro,                 v = +1
- Ex   -> DegPro,                 v = +1
%}

temp = find(state_n < 0);
lost = sum( abs( state_n( temp ) ) );
state_n(temp) = 0;
clear temp

global error_counter

error_counter(1,1) = error_counter(1,1) + 1;
error_counter(1,2) = error_counter(1,2) + lost;

k = parameters.k;
monomers = parameters.monomers;
clear next_state;
next_state = zeros(size(state_n));

species = 0;

% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Reduced Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = consumed Inhibitor, 12= Reduced Co-Initiator, 13 = bonds, 14 = Oxygen, 15 = Peroxide, 
% 15+1 -> 15 + n = vinyl groups, 15+n+1 -> 15 + 2n = polymer, radicals 
   
i_ = 1;
CQ_g =  i_; i_ = i_ +1; 
Co_g =  i_; i_ = i_ +1; 
CQ_s =  i_; i_ = i_ +1;
CQ_t =  i_; i_ = i_ +1; 
EX   =  i_; i_ = i_ +1; 
CQ_o =  i_; i_ = i_ +1; 
CO_r =  i_; i_ = i_ +1; 
D    =  i_; i_ = i_ +1;
IH_g =  i_; i_ = i_ +1; 
IH_r =  i_; i_ = i_ +1;
IH_c =  i_; i_ = i_ +1;
CO_o =  i_; i_ = i_ +1;
Bond =  i_; i_ = i_ +1;
Ox   =  i_; i_ = i_ +1; 
Pox  =  i_; i_ = i_ +1;
sn   = parameters.species_indexes.small_system_monomers;
sp   = parameters.species_indexes.small_system_radicals;
clear i_;





%% Initiator/Co-initiator
% I ground
species = species+1;
next_state(CQ_g) = -k.Igs    * state_n(CQ_g) ... excitation   G  -> S
                   +k.Isg    * state_n(CQ_s) ... relaxation   S  -> G
                   +k.Itg    * state_n(CQ_t) ... relaxation   T  -> G
                   +k.Edeact * state_n( EX );  % relaxation   Ex -> G ???
% Co ground   
species = species+1;         
next_state(Co_g) = -k.Eform  * state_n(Co_g) ... excitation   I-T + Co -> Ex
                             * state_n(CQ_t) ...
                   +k.Edeact * state_n( EX );  % relaxation   Ex       -> I-g + Co
% I Singlet   
species = species+1;         
next_state(CQ_s) = +k.Igs    * state_n(CQ_g) ... excitation   G -> S
                   -k.Isg    * state_n(CQ_s) ... relaxation   S -> G
                   -k.Ist    * state_n(CQ_s);  % excitation   S -> T
% I Triplet  
species = species+1;                                 
next_state(CQ_t) = +k.Ist    * state_n(CQ_s) ... excitation   S      -> T
                   -k.Itg    * state_n(CQ_t) ... relaxation   T      -> G
                   -k.Eform  * state_n(Co_g) ...  
                             * state_n(CQ_t);  % combination  T + Co -> Ex

% Ex         
species = species+1;   
next_state( EX ) = +k.Eform  * state_n(Co_g) ...  
                             * state_n(CQ_t) ... combination  T + Co -> Ex
                   -k.Eact   * state_n( EX ) ... activation   Ex     -> CQrH + Co-radical
                   -k.Edeact * state_n( EX ) ... deactivation Ex     -> CQ + Co
                   -k.Elost  * state_n( EX ) ...
                             * state_n(Pox );  % degradation  Ex     -> DegPro
% reduced I    
species = species+1;        
next_state(CQ_o) = next_state(CQ_o)          ...
                   +k.Eact   * state_n( EX );  % activation   Ex -> CQrH

% activated Co
species = species+1;
next_state(CO_r) = next_state(CO_r)          ...
                   +k.Eact   * state_n( EX );  % activation   Ex -> Co-radical
               
% degredation
species = species+1;
next_state(D   ) = next_state(D   ) ...
                   +k.Ilost  * state_n(CQ_t) ... degradation  T  -> DegPro
                   +k.Elost  * state_n(EX  );  % degradation  Ex -> Degpro
            
%% Inhibitor

% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Reduced Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = consumed Inhibitor, 12= Reduced Co-Initiator, 13 = bonds, 14 = Oxygen, 15 = Peroxide, 
% 16+1 -> 16 + n = vinyl groups, 16+n+1 -> 16 + 2n = polymer, radicals 
   

%{

IHg = Inhibitor - Ground
IHr = Inhibitor - Radical
Int = Used Inhitbitor


% 9  = Inhibitor
- IHg      -> 2 IHr,         v = -1
- 2 IHr    -> IHg,           v = +1

% 10 = Inhibitor radical
- IHg      -> 2 IHr,         v = +2
- 2 IHr    -> IHg,           v = -2
- IHr + POLr  -> POLt + IHt, v = -1


%}
% Inhibitor
species = species+1;
next_state(IH_g) = -k.IHgr  * 1 * state_n(IH_g) ... light induced split  
                   +k.IHrg  * 1 * state_n(IH_r);  % recombination
% Inhibitor radical  
species = species+1;           
next_state(IH_r) = +k.IHgr  * 2 * state_n(IH_g) ... ligth induced split       ----> InHibitor specific reactions
                   -k.IHrg  * 2 * state_n(IH_r) ... recombination             --/
                   -k.IHpol     * state_n(IH_r) ...                           ----> InHibitor system reactions
                                * sum(state_n(sp)); % polymer radical termination through inhibitor
 
%% Polymerization
%{

% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Reduced Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = consumed Inhibitor, 12= Reduced Co-Initiator, 13 = bonds, 14 = Oxygen, 15 = Peroxide, 
% 16+1 -> 16 + n = vinyl groups, 16+n+1 -> 16 + 2n = polymer, radicals 
   


% 11 = Vinyl groups
- V + Co-r -> POLr + B,      v = -1
- V + POLr -> POLr + B,      v = -1

% 12 = Polymer radicals
- V + IHr     -> POLr + B    v = +1
- POLr + V    -> POLr + B    v = +0
- POLr + POLr -> POL-POL + B v = -2
- POLr + POLr -> POL + POL   v = -2
- POLr + IHr  -> POL-IH      v = -1

% 13 = bonds 


%}

% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Reduced Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = consumed Inhibitor, 12= Reduced Co-Initiator, 13 = bonds, 14 = Oxygen, 15 = Peroxide, 
% 16+1 -> 16 + n = vinyl groups, 16+n+1 -> 16 + 2n = polymer, radicals 
   
   

%{
% Reduced Co-Initiator
species = species+1;
next_state(CO_o) = sum( ...                     
                 +k.Pinit  * state_n(CO_r)     ... activation   Co-r + V -> POLr
                           * state_n( sn ));
%}

  
species = species + 2*( size( monomers, 2) ); % monomers & monomer radicals
species = species + 1;                        % reduced Inhibitor
species = species + 1;                        % bonds
species = species + 1;                        % reduced CO

tags = [monomers.tag];
for i = 1 : size( monomers, 2)
    
    monomer = monomers(i);
    kinit = monomer.K.init;
    
    % EDAB-rad used by Initiation
    next_state(CO_r)  = next_state(CO_r)       ...  activation   Co-r + V -> POLr + CO_o
                      - kinit  * state_n(CO_r) ...  - CO_r / - V
                               * state_n(sn(i));  % + POLr / + CO_o
                           
    % Production of reduced EDAB
    next_state(CO_o)  = next_state(CO_o)       ...
                      + kinit  * state_n(CO_r) ...
                               * state_n(sn(i)); % 
                           
    % The 'consumption' of vinyl by reaction of vinyl with initiator                       
    next_state(sn(i)) = next_state(sn(i))      ...
                      - kinit  * state_n(CO_r) ...
                               * state_n(sn(i)); % 
                           
      
                               
    for j = 1 : size(monomers, 2)
        monomer_j = monomers(j);
        % get the reaction rate between 2 monomers
        
        %{
        rad j + mon i --[kji]-> rad i
            - rad j
            - mon i
            + rad i

        rad i + mon j --[kij]-> rad j
            - rad i 
            - mon j
            + rad j
        %}
        
        % Vinyl i is consumed by reaction with radical j
        
        kprop_ji = monomer_j.K.prop / monomer_j.K.(['R', tags(j), tags(i)]);
        sni_conc_change = kprop_ji * state_n( sp(j) ) ... rad   i
                                   * state_n( sn(i) );  % vinyl j    
                               
        next_state( sp(j) ) = next_state( sp(j) )     ... - rad j 
                            - sni_conc_change;          %        
        next_state( sn(i) ) = next_state( sn(i) )     ... - mon i
                            - sni_conc_change;          %
        next_state( sp(i) ) = next_state( sp(i) )     ... + rad i
                            + sni_conc_change;          %
        
        %{                
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
        spi_conc_change = 0;                    

        % The 'production'  of bonds by propogation
        next_state(Bond)    = next_state(Bond)     ...
                            + 2 * sni_conc_change;   %  the increase in bonds by this monomer attacking
    end
    % This monomer radicals termination * all the monomer radicals * this monomer radical
    next_state(sp(i)) = next_state(sp(i))            ...
                          - monomers(i).K.tr         ... recombination
                                  * sum(state_n(sp)) ... - the sum of all all the radical species
                                  * state_n( sp(i) ) ... - the radcials of this species
                                  * 2                ... 
                          - monomers(i).K.td         ... disproportionation
                                  * sum(state_n(sp)) ...
                                  * state_n( sp(i) ) ...
                                  * 2                ...
                          - k.IHpol                  ...
                                  * state_n( sp(i) ) ... Inhibition
                                  * state_n(IH_r)    ...
                          + kinit * state_n(CO_r)    ... 
                                  * state_n(sn(i));    % The 'production'  of POLr by reaction of vinyl with initiator
                    
    next_state(Bond)  = next_state(Bond)             ... 
                          + monomers(i).K.tr         ... recombination rate
                                  * sum(state_n(sp)) ... the totatal radical concentration
                                  * state_n( sp(i) ) ... the concentration of radicals on this monomer
                                  * 2;                 % 2 half bonds
    next_state(IH_c)  = next_state(IH_c)             ...
                          + k.IHpol * 0.5            ...
                                  * state_n( sp(i) ) ... Inhibition
                                  * state_n(IH_r);     %
end

%% degredation through oxidation

% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Active Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = Reduced Co-Initiator, 12 = bonds, 13 = Oxygen, 14 = Peroxide, 
% 15+1 -> 15 + n = vinyl groups, 15+n+1 -> 15 + 2n = polymer, radicals 

% Oxygen
species = species+1;
next_state( Ox ) = -k.Oop * state_n(CQ_t) ...
                          * state_n( Ox );
% Peroxide
species = species+1;
next_state(Pox ) = +k.Oop * state_n(CQ_t) ...
                          * state_n( Ox );
  
                    
%% Newley added



%% Big System

global marker

resin_monomers = size(monomers,2);
vmax = 0; pmax = 0; nmax = 0;

for i = 1:resin_monomers
    monomer = monomers(i);
    if monomer.vmax > vmax
        vmax = monomer.vmax;
    end
    if monomer.pmax > pmax
        pmax = monomer.pmax;
    end
    if monomer.nmax > nmax
        nmax = monomer.nmax;
    end
end

monomer_species = state_n(species+1:end); % range = all but the mainspecies


% species_conc= zeros(resin_monomers, vmax +1, pmax +1, nmax+1, nmax +1, nmax +1);
species_conc = reshape(monomer_species, resin_monomers, vmax +1, pmax +1, nmax+1, nmax +1, nmax +1);

Sum_Vinyl_species_Conc   = 0;
Sum_Radical_species_Conc = 0;
Sum_monomers_vinyl_conc = zeros(1, resin_monomers); % prealocated mostly to get rid of the squigle
Sum_monomers_radic_conc = zeros(1, resin_monomers);

for i = 1:resin_monomers                              % all the monomers
    monomer = monomers(i);                            % all the species for a monomer
    for v = 1:monomer.vmax +1                         % vinyl_groups
        for p = 1:monomer.pmax +1                     % radicals
            for b_in = 1:monomer.nmax/2 +1              % outgoing bonds  (monomer/polymer radical attacks other monomer/polymer vinyl)
                for b_out = 1:monomer.nmax/2 +1         % incomming bonds (monomer/polymer vinyl is attacked by other monomer/polymer radical)
                    for b_neutral = 1:monomer.nmax/2 +1 % neutral bonds   (monomer/polymer radical termination by combination)
                        %----------------------------------------------------------------------------------------------------------
                        Sum_Vinyl_species_Conc     = Sum_Vinyl_species_Conc     + (v-1) * species_conc(i,v,p,b_in,b_out,b_neutral);
                        Sum_Radical_species_Conc   = Sum_Radical_species_Conc   + (p-1) * species_conc(i,v,p,b_in,b_out,b_neutral);
                        %----------------------------------------------------------------------------------------------------------
                        Sum_monomers_vinyl_conc(i) = Sum_monomers_vinyl_conc(i) + (v-1) * species_conc(i,v,p,b_in,b_out,b_neutral);
                        Sum_monomers_radic_conc(i) = Sum_monomers_radic_conc(i) + (p-1) * species_conc(i,v,p,b_in,b_out,b_neutral);
                        %----------------------------------------------------------------------------------------------------------
                    end
                end
            end
        end
    end
end

% species_conc(1,1,1,1,3,1)
% i == 1 && v == 3 && p == 1 && b_in == 1 && b_out == 1 && b_neutral == 1
% i == 1 && v == 2 && p == 2 && b_in == 1 && b_out == 1 && b_neutral == 1 && next_species_conc(1,1,1,1,3,1) > 0

next_species_conc = zeros(resin_monomers, vmax +1, pmax +1, nmax+1, nmax +1, nmax +1);

% acceptable_loss = 10e-90;
show_errors = false;

for i = 1:resin_monomers                              % all the monomers
    monomer = monomers(i);                            % all the species for a monomer
    for v = 1:monomer.vmax +1                         % vinyl_groups
        for p = 1:monomer.pmax +1                     % radicals
            for b_in = 1:monomer.nmax/2 +1              % outgoing bonds  (monomer/polymer radical attacks other monomer/polymer vinyl)
                for b_out = 1:monomer.nmax/2 +1         % incomming bonds (monomer/polymer vinyl is attacked by other monomer/polymer radical)
                    for b_neutral = 1:monomer.nmax/2 +1 % neutral bonds   (monomer/polymer radical termination by combination)
                        %
                        %%% debug_species = [ int2str(i) int2str(v) int2str(p) int2str(b_in) int2str(b_out) int2str(b_neutral) ];
                        b_tot = b_in + b_out + b_neutral - 3;
                        if ((v-1)*2) + (p-1) + b_tot <= monomer.nmax  &&  ((v-1)*2) + 2*(p-1)<=monomer.nmax && monomer.vmax - (v-1) >= (b_in -1) ...
                                && monomer.vmax - (v-1) >= (b_out -1) && monomer.vmax - (v-1) >= (b_neutral -1)
                            % deals with the changes in the vinyls
                            if v > 1
                                init_conc_change = monomer.K.init                           ... The rate of initation times 
                                                 * (v-1)                                    ... the amount of vinyl groups (non_zero index)
                                                 * species_conc(i,v,p,b_in,b_out,b_neutral) ... the concentration in the last step
                                                 * state_n(CO_r);                             % the initator species concentration

                                prop_conc_change = 0;
                                for j = 1:resin_monomers
                                    kprop = monomers(j).K.prop / monomers(j).K.(['R', tags(j), tags(i)]); % attack of j on i
                                    prop_conc_change = prop_conc_change + kprop                 ... The rate of propogation
                                                     * (v-1)                                    ... The amount of vinyl groups (non_zero index)
                                                     * species_conc(i,v,p,b_in,b_out,b_neutral) ... The concentration in the last step
                                                     * Sum_monomers_radic_conc(j);                % The concentration of all radical species
                                end      
                                next_species_conc(i,v  ,p  ,b_in  ,b_out,b_neutral)     = next_species_conc(i,v  ,p  ,b_in,b_out,b_neutral) ... The decrease in this species
                                                                                        - init_conc_change                                  ...
                                                                                        - prop_conc_change;                                   %
                                if p <= monomer.pmax                                                                                          %
                                    next_species_conc(i,v-1,p+1,b_in  ,b_out,b_neutral) = next_species_conc(i,v-1,p+1,b_in,b_out,b_neutral) ... The increase of the species 
                                                                                        + init_conc_change;                                   % matching initation                       %
                                else
                                    error_counter(2,1) = error_counter(2,1) + 1;
                                    error_counter(2,2) = error_counter(2,2) + init_conc_change;
                                end

                                if b_in <= monomer.nmax && p <= monomer.pmax
                                    next_species_conc(i,v-1,p+1,b_in+1,b_out,b_neutral) = next_species_conc(i,v-1,p+1,b_in+1,b_out,b_neutral) ... the increase of the species
                                                                                        + prop_conc_change;                                     % matching propogation
                                else
                                    error_counter(3,1) = error_counter(3,1) + 1;
                                    error_counter(3,2) = error_counter(3,2) + prop_conc_change;
                                end
                            end
                            % deals with the changes in the radicals
                            if p > 1
                                rad_prop_conc_change = 0;
                                for j = 1:resin_monomers
                                    kprop = monomers(i).K.prop / monomers(i).K.(['R', tags(i), tags(j)]);      % Attack of i on j
                                    rad_prop_conc_change      = rad_prop_conc_change + kprop                 ... The change in radicals by the propogation
                                                              * (p-1)                                        ... the amount of radicals (non_zero index)
                                                              * species_conc(i,v,p,b_in,b_out,b_neutral)     ... the concentration of the species
                                                              * Sum_monomers_vinyl_conc(j);                    % the total concentration of radical species

                                end
                                rad_term_comb_conc_change = + monomer.K.tr * 2                             ... The change in this species radical by combination
                                                            * (p-1)                                        ... the amount of radicals (non_zero index)
                                                            * species_conc(i,v,p,b_in,b_out,b_neutral)     ... the concentration of the species
                                                            * Sum_Radical_species_Conc;                      % the total concentration of radical species

                                rad_term_disp_conc_change = + monomer.K.td * 2                             ... The change in this radical species by disproportionation
                                                            * (p-1)                                        ... the amount of radicals (non_zero index)
                                                            * species_conc(i,v,p,b_in,b_out,b_neutral)     ... the concentration of this species
                                                            * Sum_Radical_species_Conc;                      % the total concentration of radical species

                                rad_term_IH_conc_change   = + k.IHpol                                      ... the change in this radical species by inhibition
                                                            * (p-1)                                        ... the amount of radicals (non_zero index)
                                                            * species_conc(i,v,p,b_in,b_out,b_neutral)     ... the cocnentration of the species
                                                            * state_n(IH_r);                                 % the concentration of inhibitor

                                %{
                                this species: - prop/ - recomb/ - disp/ - inhib
                                p -> p-1:
                                # p-1, b_out +1 -- + prop
                                # p-1, b_n +1   -- + recombination
                                # p-1           -- + disproportionation
                                # p-1           -- + Inhibition
                                # v-1, b_in +1  -- + prop  % handeled in the if v > 1
                                %}

                                % the new concentration of this species                          
                                next_species_conc(i,v,p,b_in,b_out,b_neutral)         = next_species_conc(i,v,p  ,b_in,b_out  ,b_neutral  ) ...
                                                                                      - rad_prop_conc_change                                ...
                                                                                      - rad_term_comb_conc_change                           ...
                                                                                      - rad_term_disp_conc_change                           ...
                                                                                      - rad_term_IH_conc_change;                              %
                                % the new concentration of the species that changed a radical to a outgoing bond  (propogation)
                                if b_out <= monomer.nmax % either increase the size of the matrix or this
                                    next_species_conc(i,v,p-1,b_in,b_out+1,b_neutral) = next_species_conc(i,v,p-1,b_in,b_out+1,b_neutral  ) ...
                                                                                      + rad_prop_conc_change;                             
                                else
                                    error_counter(4,1) = error_counter(4,1) + 1;
                                    error_counter(4,2) = error_counter(4,2) + rad_prop_conc_change;
                                end
                                % the new concentration of the species that changed a radical to a neutral bond   (combination)                                              
                                if b_neutral <= monomer.nmax
                                    next_species_conc(i,v,p-1,b_in,b_out,b_neutral+1) = next_species_conc(i,v,p-1,b_in,b_out  ,b_neutral+1) ...
                                                                                      + rad_term_comb_conc_change;                            %
                                else
                                    error_counter(5,1) = error_counter(5,1) + 1;
                                    error_counter(5,2) = error_counter(5,2) + rad_prop_conc_change;
                                end      

                                % the new concentration of the species that only lost a radical            (disproportionation)
                                next_species_conc(i,v,p-1,b_in,b_out,b_neutral)       = next_species_conc(i,v,p-1,b_in,b_out,b_neutral)     ...
                                                                                      + rad_term_disp_conc_change;                            %
                                % the new concentration of the species that only lost a radical                    (Inhibition)
                                next_species_conc(i,v,p-1,b_in,b_out,b_neutral)       = next_species_conc(i,v,p-1,b_in,b_out,b_neutral)     ...
                                                                                      + rad_term_IH_conc_change;                              %
                            end
                        end
                    end
                end
            end
        end
    end
end

Next_monomer_vinyl_conc = zeros(1, resin_monomers);
Next_monomer_radic_conc = zeros(1, resin_monomers);

for i = 1:resin_monomers                              % all the monomers
    monomer = monomers(i);                            % all the species for a monomer
    for v = 1:monomer.vmax +1                         % vinyl_groups
        for p = 1:monomer.pmax +1                     % radicals
            for b_in = 1:monomer.nmax +1              % outgoing bonds  (monomer/polymer radical attacks other monomer/polymer vinyl)
                for b_out = 1:monomer.nmax +1         % incomming bonds (monomer/polymer vinyl is attacked by other monomer/polymer radical)
                    for b_neutral = 1:monomer.nmax +1 % neutral bonds   (monomer/polymer radical termination by combination)
                        %----------------------------------------------------------------------------------------------------------
                        Next_monomer_vinyl_conc(i) = Next_monomer_vinyl_conc(i) + (v-1) * next_species_conc(i,v,p,b_in,b_out,b_neutral);
                        Next_monomer_radic_conc(i) = Next_monomer_radic_conc(i) + (p-1) * next_species_conc(i,v,p,b_in,b_out,b_neutral);
                        %----------------------------------------------------------------------------------------------------------
                    end
                end
            end
        end
    end
end


% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Active Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = Reduced Co-Initiator, 12 = bonds, 13 = Oxygen, 14 = Peroxide, 
% 15+1 -> 15 + n = vinyl groups, 15+n+1 -> 15 + 2n = polymer, radicals 

margin = 10e-5;

%% state n check
Vinyl_dif = abs( sum(Sum_monomers_vinyl_conc) - sum( state_n(sn) ) );
Radic_dif = abs( sum(Sum_monomers_radic_conc) - sum( state_n(sp) ) );

%% next state check
Next_sum_monomers_vinyl_conc = sum(Next_monomer_vinyl_conc);
Next_sum_monomers_radic_conc = sum(Next_monomer_radic_conc);

Next_vinyl_dif = abs( Next_sum_monomers_vinyl_conc - sum( next_state(sn) ) );
Next_Radic_dif = abs( Next_sum_monomers_radic_conc - sum( next_state(sp) ) );

%%
if false && ( ( ( abs(Vinyl_dif) > margin || abs(Radic_dif) > margin ) || ( abs(Next_vinyl_dif) > margin || abs(Next_Radic_dif) > margin )) && marker < 105 )
   marker = marker +1;
   if marker == 100
       disp(["marker reached 1000" newline])
   end
end

%%

% shows the difference between the 2 starting states
if ( abs(Vinyl_dif) > margin || abs(Radic_dif) > margin ) && marker < 100 && false 
      disp(join(["Error in RRE,         small and big system don't agree --- at t:", num2str(t, '%10.1e\n'), " Vin_dif: ", num2str(Vinyl_dif, '%10.1e\n'), "  Rad_dif: ", num2str(Radic_dif, '%10.1e\n')]))
      
end

% shows the difference between the 2 dif_states
if ( abs(Next_vinyl_dif) > margin || abs(Next_Radic_dif) > margin ) && marker < 100 && false
      disp(join(["Error in RRE, evolved small and big system don't agree --- at t:", num2str(t, '%10.1e\n'), " Vin_dif: ", num2str(Next_vinyl_dif, '%10.1e\n'), "  Rad_dif: ", num2str(Next_Radic_dif, '%10.1e\n')]))
end

%%% debuging code
% monomer_conc__ = next_species_conc(1,3,1,1,1,1);
% next_monomer_conc__ = next_species_conc(1,2,2,1,1,1);

next_state(species+1:end) = reshape(next_species_conc, [], 1);


end




%{
complete rate of CQ
polymerization using camphorquinone & amine system.pdf

-d[CQ]/dt = 2.303 * k2 * (ka * [A] * (1 - gama) + alpha *k3)
          * I0 * EpsiCQ *[CQ]/{(k1+k2)k3 + (k1+k2)ka[A]} 
%}




