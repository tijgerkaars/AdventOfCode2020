function [result, warning] = run(parameters)
%{
%RUN The main model that simulates the polymerization reaction through an kinetic model (RRE)
% In this RRE we employ 2 methodes mPBE and monomer aproach where mPBE is
% mainly used to describe the initator/co-initiator, inhibitor concentrations
% These are then used with the monomer aproach.
% in the monomer approach we view the monomer as a unit with attributs: vinyl
% groups, radicals, incomming bonds, outgoing bonds, and recombinated bonds.
% From these units we can get the concentration of the different bonds over time,
% these bonds can be viewed as directed edges in a random graph. This graph
% is used to gain insight in the global properties of the monomer.

%  There are several assumtions that are made:
%  - The Initiator processes don't form degredation products
%  - The resin is oxygen free
%  - The Inhibitor does only react with propogating radicals
%  - The initiation/inhibition becomming imbedded in the monomer is not 
%    concidered (there is no diffusion)
%  - The system is not affected by temperature changes
%  - The system is viewed as an thin layer, initiating and inhibitting 
%    light is uniform in intesity throughout the reaction
%  - The reaction rates are not diffussion limited

%}


result.run_id = parameters.run;
result.run_times.run_starting_time = datetime('now');

starting_time = parameters.run_times.start_time;
k_ = return_rates(parameters);
parameters.k = k_;


parameters.counter = 0;

%% Start

disp(newline)

global figures marker
marker = false;

monomers = parameters.monomers;

error_temp = zeros(5,2);

parameters.error_counter = error_temp;

 
%% Initalisation
header = ["Initiator ground state", "Co-Initiator ground state", "Initiator Singlet state", "Initiator Triplet state", "Exicomplex", "Reduced Initiators", "Activated Co-Initiator", "Degredation products",...
          "Inhibitor", "Inhibitor radical", "Consumed Inhibitor", ...
          "Reduced Co-Initiator", "Half Bonds", ...
          "Oxygen", "Peroxide"];
      
monomer_header_constructor = string();
radical_header_constructor = string();

for i = 1:size(parameters.monomers,2)
    monomer_header_constructor(i) = monomers(i).name;
    radical_header_constructor(i) = [monomers(i).name, '-radical'];
end

small_system_edge = size(header,2);
header = [header,monomer_header_constructor];
small_system_monomers = [(small_system_edge +1) : (size(header,2))];
species_indexes.small_system_monomers = small_system_monomers;

small_system_edge = size(header,2);
header = [header, radical_header_constructor];
small_system_radicals = [(small_system_edge +1) : (size(header,2))];
species_indexes.small_system_radicals = small_system_radicals;


% starting concentrations

Initiator    = parameters.initiator;
Co_initiator = parameters.co_initiator;
Inhibiter    = parameters.inhibiter;
Oxygen       = parameters.oxygen;

% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Reduced Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = consumed Inhibitor, 12 = Reduced Co-Initiator, 13 = bonds, 14 = Oxygen, 15 = Peroxide, 
% 16+1 -> 16 + n = vinyl groups, 16+n+1 -> 16 + 2n = polymer, radicals 
    
% set the starting states to the starting concentrations
state_zero = [Initiator.conc; Co_initiator.conc; 0;0;0;0;0;0; ... 1 - 8
              Inhibiter.conc; 0; 0; ...                         % 9 - 11
              0; 0; ...                                         % 12- 13
              Oxygen.conc; 0];                                  % 14- 11

          
% take the concentration of each monomer and multiply it with the amount of vinyl groups on that monomer
Starting_Venyl_groups = [monomers.conc].*[monomers.vmax];
state_zero = [state_zero', Starting_Venyl_groups, zeros(size(monomers)) ]';

species_indexes.small_species = [1:size(state_zero,1)];
species_indexes.Initiators = [1,3:6,8];
species_indexes.Co_Initiators = [2,5,7,12];
species_indexes.Inhibitors = [9:11];
species_indexes.oxygen = [14:15];
species_indexes.Initiator_system = unique([species_indexes.Initiators,species_indexes.Co_Initiators]);
species_indexes.small_bonds = [13];

species_indexes.small_index_content = join( [header(species_indexes.small_species(:))', num2str( species_indexes.small_species(:) )], " = " )';

parameters.species_indexes = species_indexes;
        

% set the time span in seconds        
t_max = parameters.t_span;

calc = parameters.calc;

%% Expand the species list

% creates all the possible combinations of attributs for each monomer
% vinyl groups/ radicals/ 3 types of bonds
[monomer_species, valid_monomer_species, species_header, indexes] = create_species(monomers);

total_monomer_species = size(monomer_species,1);
num_valid_species = sum(valid_monomer_species(:) == 1);
species_indexes.free_monomer_indexes = indexes.free_monomer_indexes + max(size(state_zero));
species_indexes.free_monomer_indexes = indexes.vinyl_indexes        + max(size(state_zero));
species_indexes.free_monomer_indexes = indexes.radical_indexes      + max(size(state_zero));

%% give some info on the system


disp([                                parameters.prefix])
disp(['                   run: ',     num2str(parameters.run), '/', num2str(parameters.total_runs) ])
disp(['            time frame: ',     num2str(t_max)] );
disp(['         small_species: [1:',  num2str( max( species_indexes.small_species) ), ']' ]);
disp(['              monomers: ',     char( join(monomer_header_constructor, " & " ) ) ]);
% disp(['                  conc: ',     char( join([ num2str(monomers.conc), " & " ) ) ]);
if Inhibiter.conc > 0
    disp(['            Inhibiters: ', Inhibiter.name]);
end
disp(['     num_valid_species: ',     num2str(num_valid_species)]);
disp([' total_monomer_species: ',     num2str(total_monomer_species)]);


% disp(['         small_species: ', newline, join( [header(species_indexes.small_species(:))', num2str( species_indexes.small_species(:) )], " = " )' ]');

% calculate the average run time and estimate when the run is complete
if parameters.run > 1
    ellapsed = datetime('now') - starting_time; % the time since the screening started
    average_per_run = ellapsed/(parameters.run-1); % the ellapsed time devided by the finished runs
    remaining_runs = parameters.total_runs - (parameters.run-1); % the remaining runs
    remaining_run_time = average_per_run * remaining_runs;
    disp(['           Time format: ', 'DD HH:MM:SS'])
    disp(['        Total run time: ', datestr( ellapsed, 'DD HH:MM:SS'),        '  Average time per run: ', datestr(average_per_run, 'DD HH:MM:SS') ])
    disp(['   Time off completion: ', datestr( datetime('now') +  remaining_run_time, 'DD HH:MM:SS'), '    Remaining run time: ' datestr( remaining_run_time, 'DD HH:MM:SS' )])
end







%% Add the monomerspecies to the small system species list

starting_state = zeros(size(state_zero,1) + size(monomer_species,1),1);

starting_state( 1 : size(state_zero,1) ) = state_zero;
starting_state( size(state_zero,1)+1 : end ) = monomer_species;

% to the header as well
new_header( 1 : size(header,2) ) = header;
new_header( size(header,2)+1 : size(header,2) + size(species_header,1) ) = species_header;
header = new_header;

%%
%% Do the calculations
%%
%%


% returns all the rates related to the initialisation and polymerization
% sets up the differential equation solver (ODE)

options = odeset();
options.InitialStep = 1e-10;
options.AbsTol      = 1e-15;
options.MaxStep     = 5;

if calc.ode || calc.all
    rre_s_time = datetime('now');
    disp([newline, '- Running ODE, started at: ', datestr(rre_s_time,'mmm-dd HH:MM:SS')])
    
    global error_counter marker
    error_counter = zeros(5,2);
    marker = 0;
    
    
    % actually solves the differential equations
    [t,y] = ode15s(@(t,starting_state) RRE(t,starting_state, parameters) , [0 t_max], starting_state, options);
    
    [msglast, msgidlast] = lastwarn;
    if strcmp(msgidlast, 'MATLAB:ode15s:IntegrationTolNotMet')
        warning.ODE = true;
        lastwarn('');
    else
        warning.ODE = false;
    end    
    
    parameters.error_counter = error_counter;
    
    clear error_counter
    
    errors_in_RRE = parameters.error_counter;
    if sum(errors_in_RRE(:,2)) > parameters.RRE_allowed_error
        temp = strings(1,2);
        temp(1) = 'Occurrences';
        temp(2) = 'Mass loss';
        disp([temp])
        disp([errors_in_RRE])
    end
    rre_c_time = datetime('now') - rre_s_time;
    disp(['  Done running ODE, time taken: ', datestr(rre_c_time, 'HH:MM:SS'), ' Total time: ', datestr((datetime('now') - starting_time), 'HH:MM:SS')])
    %---------------------
    result.state_zero      = starting_state;
    result.RRE_y           = y;
    result.RRE_t           = t;
    result.run_times.RRE_t = rre_c_time;
    result.header          = header;
    result.errors_in_RRE   = errors_in_RRE;
    %---------------------
end



%% Pre process the output

% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Active Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = Reduced Co-Initiator, 12 = bonds, 13 = Oxygen, 14 = Peroxide, 
% 15+1 -> 15 + n = vinyl groups, 15+n+1 -> 15 + 2n = polymer, radicals //species_indexes

resin_monomers = size(monomers,2);
vmax = 0; pmax = 0; nmax = 0;

% Finds the max vinyl,radical,bonds
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

small_species = y(:, species_indexes.small_species);

monomer_species_index = [ size(state_zero,1) + 1 : size(starting_state,1) ];
species_indexes.big_monomer_species_index = monomer_species_index;

monomer_species       = y(:,monomer_species_index); % range = all but the mainspecies
monomer_species_conc  = reshape(monomer_species, resin_monomers, vmax +1, pmax +1, nmax+1, nmax +1, nmax +1, size(t,1));
 
small_conversion = 1 - ( sum(Starting_Venyl_groups) - small_species(:,species_indexes.small_bonds) /2 ) / sum(Starting_Venyl_groups);

result.small_conversion      = small_conversion;

%{
%---------------------
result.small_species         = small_species;
result.monomer_species_index = monomer_species_index;
result.monomer_species       = monomer_species;
result.monomer_species_conc  = monomer_species_conc;
%---------------------
%}



%%
%% Find the Degree-Distribution
%%
%%

%{ do
if calc.deg || calc.gel_point    || calc.comp_size_distr_gelpoint_3d || calc.ms2 || calc.all
    %%% For each timestep combine the concentration of species with the same amount of bonds
    % degree contains this collection for each timestep
    % header contains the correlated bonds
    deg_s_time = datetime('now');
    disp(['- Determining the degree distribution, started at: ' datestr(deg_s_time, 'mmm-dd HH:MM:SS')])
    
    %-------- return the deg dist --------%
    [degree, degree_header, typed_degree, typed_degree_header] = return_deg_dist( t, y(:,size(state_zero,1)+1 :end), monomers);
    
    deg_c_time = datetime('now') - deg_s_time;
    disp(['  Found the degree distribution, time taken: ', datestr(deg_c_time, 'HH:MM:SS'), ' Total time: ', datestr((datetime('now') - starting_time), 'HH:MM:SS')])
    %---------------------
    result.degree               = degree;
    result.degree_header        = degree_header;
    result.typed_degree         = typed_degree;
    result.typed_degree_header  = typed_degree_header;
    result.run_times.deg_c_time = deg_c_time;
    %---------------------
end

%}


%%
%% Random Graph Part
%%
%%

%% Run parameters

analyse.exact_gelpoint_3d=0;    %Calculate exact gel points by interpolation and solving ODE 3D
analyse.exact_gelpoint_1d=0;    %Calculate exact gel points by interpolation and solving ODE 1D
analyse.calc_comp_size_distr_gelpoint_3d=1; %Calculate component size distribution exactly at gel point 3D
analyse.calc_comp_size_distr_gelpoint_1d=0; %Calculate component size distribution exactly at gel point 1D

%% Get Gel Point

if calc.gel_point || calc.all
    GelP3d_s_time = datetime('now');
    disp(['- Finding gelpoint, stated at: ', datestr(GelP3d_s_time, 'mmm-dd HH:MM:SS')])
    [checkgel_3d, gel_i, gel_conv_3d, deg3d_gel, C_gel, gel_conv] = get_gelpoint_3d([y,t],                     ...
                                                                          monomer_species_conc,      ...
                                                                          small_species',            ...
                                                                          typed_degree,              ...
                                                                          small_conversion,          ...
                                                                          analyse.exact_gelpoint_3d, ...
                                                                          parameters);
    GelP3d_c_time = datetime('now') - GelP3d_s_time;
    disp(['  found gelpoint, time taken: ', datestr(GelP3d_c_time, 'HH:MM:SS'), ' Total time: ', datestr((datetime('now') - starting_time), 'HH:MM:SS')])
                                                                     
    %---------------------
    result.checkgel_3d = checkgel_3d;
    result.gel_i       = gel_i;
    result.gel_conv_3d = gel_conv_3d;
    result.deg3d_gel   = deg3d_gel;
    result.C_gel       = C_gel;
    result.gel_conv    = gel_conv;
    
    result.run_times.GelP_c_time = GelP3d_c_time;
    %---------------------
end


%% Get average mass

%{ do
 

if calc.ms2 || calc.all
    ms2_s_time = datetime('now');
    disp(['- Finding average length, started at: ', datestr(ms2_s_time, 'mmm-dd HH:MM:SS')])
    
    [ Ms2 ] = expected_size_3D_1dir_1undir( typed_degree, t, parameters);
    
    ms2_c_time = datetime('now') - ms2_s_time;
    disp(['  Done finding length, time taken: ', datestr(ms2_c_time, 'HH:MM:SS'), ' Total time: ', datestr((datetime('now') - starting_time), 'HH:MM:SS')])
    %---------------------
    result.Ms2 = Ms2;
    result.run_times.ms2_c_time = ms2_c_time;
    %---------------------
end

%}

%% At gel point 3d


ncomp_max_3d=1:1e3;
if analyse.calc_comp_size_distr_gelpoint_3d==0 || calc.all
    comp_size_dist_s_time = datetime('now');
    disp(['- Calculation component size distribution at gellpoint, started at: ', datestr(comp_size_dist_s_time, 'mmm-dd HH:MM:SS')])
    
    
    [w_gel, g_f_gel]=component_size_distr_at_gelpoint_3d( deg3d_gel, ncomp_max_3d, parameters);
    
    comp_size_dist_c_time = datetime('now') - comp_size_dist_s_time;
    disp(['  Done, time taken: ', datestr(comp_size_dist_c_time, 'HH:MM:SS'), ' Total time: ', datestr((datetime('now') - starting_time), 'HH:MM:SS')])
    %---------------------
    result.w_gel   = w_gel;
    result.g_f_gel = g_f_gel;
    
    result.run_times.comp_size_dist_c_time = comp_size_dist_c_time;
    %---------------------
end

if calc.gel_frac || calc.all
    gel_frac_s_time = datetime('now');
    disp(['- Calculation gel fraction, started at: ', datestr(gel_frac_s_time, 'mmm-dd HH:MM:SS')])
    clear temp
    for i = 1:max(size(result.RRE_t))
        dim=size(result.typed_degree);
        temp(i) = poly_rand_graph_onlygf_3D(reshape(result.typed_degree(i,:,:,:),dim(2:end)));
    end
    corrected_temp = temp;
    corrected_temp(1:gel_i-5) = 0;
    gel_frac_c_time = datetime('now') - gel_frac_s_time;
    disp(['  Done, time taken: ', datestr(gel_frac_c_time, 'HH:MM:SS'), ' Total time: ', datestr((datetime('now') - starting_time), 'HH:MM:SS')])
    %---------------------
    
    result.gelf_fraction = temp;
    result.currected_gelf_fraction = corrected_temp;
    
    result.run_times.gel_frac_c_time = gel_frac_c_time;
    %---------------------
end

%%
%% Display Results
%% 
%%

disp([newline, 'Starting plotting']);

draw = parameters.draw;
prefix = parameters.prefix;

%% Plot small system
%%

% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Active Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = Reduced Co-Initiator, 12 = bonds, 13 = Oxygen, 14 = Peroxide, 
% 15+1 -> 15 + n = vinyl groups, 15+n+1 -> 15 + 2n = polymer, radicals 

% % % disp('plotting test plot')
% % % plot(t,y)
% % % disp('plotted test plot')

if ~draw.none && ( draw.small_syst || draw.all )
    disp([newline, 'Plotting small system, figures: '])
    
    plot_concentrations(t,                                           ...
                        y(:, species_indexes.small_species),         ...
                        header( species_indexes.small_species),      ...
                        [prefix, 'Concentrations of small total system'] );
    disp(['                       figure: ', num2str(figures)])
    plot_concentrations(t,                                           ...
                        y(:,species_indexes.Initiator_system),       ...
                        header(:,species_indexes.Initiator_system),  ...
                        [prefix, 'Initiator system, Initiator/Co-initiator'] );
    disp(['                       figure: ', num2str(figures)])
    plot_concentrations(t,                                           ...
                        y(:,species_indexes.Initiators),             ...
                        header(:,species_indexes.Initiators),        ...
                        [prefix, 'Small system: Initiator species'] );
    disp(['                       figure: ', num2str(figures)])
    plot_concentrations(t,                                           ...
                        y(:,species_indexes.Co_Initiators),          ...
                        header(:,species_indexes.Co_Initiators),     ...
                        [prefix, 'Small system: Co-Initiator species']);
    disp(['                       figure: ', num2str(figures)])
    if Inhibiter.conc > 0
        plot_concentrations(t,                                             ...
                            y(:,species_indexes.Inhibitors),               ...
                            header(:,species_indexes.Inhibitors),          ...
                            [prefix, 'Small system: Concentrations of Inhibitors']);
        disp(['                       figure: ', num2str(figures)])
    end
    plot_concentrations(t,                                                                                        ...
                        y(:,[species_indexes.small_system_monomers, species_indexes.small_system_radicals,13]),      ...
                        header(:,[species_indexes.small_system_monomers, species_indexes.small_system_radicals,13]), ...
                        [prefix, 'Small system: Concentrations of polymer species']);
    disp(['                       figure: ', num2str(figures)])
    if Oxygen.conc > 0
        plot_concentrations(t,                                                     ...
                            y(:,species_indexes.oxygen),                           ...
                            header(:,species_indexes.oxygen),                      ...
                            [prefix, 'Small system: Concentrations of Oxygen related species']);
        disp(['                       figure: ', num2str(figures)])
    end
end

%% Plot Big system
%%

%% Make preperations for the plotting of the big system
% find the indexes that represent 'valid' monomer species
valid_species_index = find(valid_monomer_species);
valid_species_index = valid_species_index' + size(state_zero,1);

% find the indexes that represent 'non-valid' monomer species
non_valid_monomers = [ size(state_zero,1)+1 : size(y,2) ];
non_valid_monomers(:, valid_species_index-size(state_zero,1)) = [];

species_indexes.valid_species_index = valid_species_index;
species_indexes.non_valid_monomer_index = valid_species_index-size(state_zero,1);


% prints shows all 'valid' species
header(:,valid_species_index)'; %#ok<VUNUS>

% shows the concentrations of all 'valid' species
show_valid = [header(:,valid_species_index); ...
                   y(:,valid_species_index); ...
              header(:,valid_species_index)];  %
% dips(show_valid)          

%% The species that are 'valid' but gain no concentration

%%
%%
%{
% takes the concentrations from the valid_species over time
% then summes them and finds the ones that are zero
% then takes the "names" of that species from the header
% same for non-valid but finds the ones that are non-zero
%}

valid_species_zero_conc = header( valid_species_index( sum( y(:,valid_species_index) ) == 0) )';
non_valid_species_zero_conc = header( non_valid_monomers( sum( y(:,non_valid_monomers) ) ~= 0) )';

valid_species_zero_conc';
non_valid_species_zero_conc';
    
%% Plots all the monomer species

if ~draw.none && ( draw.all_monomers || draw.all )
    disp([newline, 'Plotting all monomer species, figure: ', num2str(figures+1)])
    plot_concentrations(t, y(:,[size(state_zero,1)+1 : end]), header(:,[size(state_zero,1)+1 : end]), [prefix, 'Big system: All monomer species']);
end
    
%% Plots all the 'valid' monomer species

if ~draw.none && ( draw.valid_monomers || draw.all )
    disp([newline, 'Plotting all valid monomer species, figure: ', num2str(figures+1)])
    plot_concentrations(t, y(:,valid_species_index), header(:,valid_species_index), [prefix, "Big system: 'Valid' monomer species"]);
end

%% Plots all the 'none-valid' monomer species

if ~draw.none && ( draw.non_valid_monomers || draw.all )
    disp([newline, 'Plotting all none-valid monomers species, figure: ', num2str(figures+1)])
    plot_concentrations(t, y(:,non_valid_monomers), header(non_valid_monomers), [prefix, "Big system: 'none-valid' monomer species"]);
end

%% Plots the valid vs non-valid monomer species

if ~draw.none && ( draw.compare_monomers || draw.all )
    
    disp([newline, 'Plotting the valid vs non-valid monomer species, figure: ', num2str(figures+1)])
    
    plot_compare_n_sets(t, y, valid_species_index, non_valid_monomers, header, 'Valid monomers', 'Non-Valid monomers');
end

%% Degree distribution
%%

%% Plot bonds summed

if ~draw.none && ( draw.summed_bonds || draw.all )
    disp([newline, 'Plotting the degree distribution, figure: ', num2str(figures+1)])
    % removes those that are 0
    temp = degree/degree(1,1);
    temp2 = degree_header;
    temp2( :, ~any(temp,1) ) = [];
    temp( :, ~any(temp,1) )  = [];
    %
    plot_concentrations(t,temp, temp2, [prefix, 'Big system: Degree distribution']);
end

%% Plot typed_bonds

if ~draw.none && ( draw.typed_bonds || draw.all )
    disp([newline, 'Plotting the detailed degree, figure: ', num2str(figures+1)])
    plot_concentrations(t,typed_degree/typed_degree(1,1,1,1), typed_degree_header, [prefix, 'Typed degree distribution'])
end


%% Show conversion of small system

if ~draw.none && ( draw.small_conversion || draw.all ) 
    disp([newline, 'Plotting the small system conversion, figure: ', num2str(figures+1)])
    temp = [species_indexes.small_system_monomers, species_indexes.small_system_radicals, species_indexes.small_bonds];
    
    plot_conversion(t,y, header, [species_indexes.small_species   ], parameters, [prefix, 'Small system: Conversion of total system'])
    plot_conversion(t,y, header, [species_indexes.Initiator_system], parameters, [prefix, 'Small system: Conversion of Initiators/Co-Initiators'])
    plot_conversion(t,y, header, [species_indexes.Initiators      ], parameters, [prefix, 'Small system: Conversion of Initiators'])
    plot_conversion(t,y, header, [species_indexes.Co_Initiators   ], parameters, [prefix, 'Small system: Conversion of Initiators'])
    plot_conversion(t,y, header, [temp                            ], parameters, [prefix, 'Small system: Conversion of polymer species'])
    %  monomer,radical,bonds
end

%% Show conversion of Big system

if ~draw.none && ( draw.big_conversion || draw.all )
    disp([newline, 'Plotting the big system conversion, figure: ', num2str(figures+1)])
    
    plot_conversion_degree_dist_subplots(t, degree, degree_header, monomers)
    plot_conversion_degree_dist(t, degree, degree_header, monomers, [prefix, "Big system conversion"])
end

%% Determine validity of system
%# several checks to see if the model works correctly, checks:
% - if initiator mass is lost
% - if co-initiator mass is lost
% - if big_system monomer mass is lost
% - if a 'non-valid' monomer has/had concentration
% - if the mass loss in the RRE is not to high

disp([newline, 'Plotting done'])

% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Active Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = Reduced Co-Initiator, 12 = bonds, 13 = Oxygen, 14 = Peroxide, 
% 15+1 -> 15 + n = vinyl groups, 15+n+1 -> 15 + 2n = polymer, radicals 


% sums all the species that represent initator 
Initiator_sum = sum( y(:, species_indexes.Initiators), 2 );
% sums all the species that represent co-initiator
Co_initiator_sum = sum( y(:, species_indexes.Co_Initiators), 2 );
% sums all the monomer species conentrations
% WIP
Monomer_sum = sum(y(:,species_indexes.big_monomer_species_index),2);
% shows how many valid_species had no concentration
valid_species_zero_conc_size = size(valid_species_zero_conc);
% sums all the mass lost during RRE
RRE_mass_loss = sum( errors_in_RRE(:,2) );


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

monomer_species = y(:,species_indexes.big_monomer_species_index); % range = all but the mainspecies

%% Checks

margin = 10e-100;

if std(Monomer_sum) > margin
    Monomer_sum';
    disp(['standart_def_Monomer = ', num2str( std(Monomer_sum) )] )
end
if std(Initiator_sum) > margin
    Initiator_sum';
    disp(['standart_def_initator = ', num2str( std(Initiator_sum) )] )
end
if std(Co_initiator_sum) > margin
    disp(['standart_def_Co_initiator_sum = ', num2str( std(Co_initiator_sum) )] )
end
if ~isempty(non_valid_species_zero_conc)
    disp('non_valid_species_zero_conc')
end
if RRE_mass_loss > margin
    disp(['RRE_mass_loss = ', num2str(RRE_mass_loss)])
end


differenc_errors.monomer_sum                 = Monomer_sum;
differenc_errors.initiator_sum               = Initiator_sum;
differenc_errors.co_initiator_sum            = Co_initiator_sum;
differenc_errors.non_valid_species_zero_conc = non_valid_species_zero_conc;
differenc_errors.RRE_mass_loss               = RRE_mass_loss;

%% Plots

%% Compare the vinyl and radicals of the small and big system

vinyl_over_time_small = zeros(size(t));
radical_over_time_small = zeros(size(t));

vinyl_over_time_big = zeros(size(t));
radical_over_time_big = zeros(size(t));

vinyl_over_time_big_Split   = zeros(resin_monomers, size(t,1) );
radical_over_time_big_Split = zeros(resin_monomers, size(t,1) );

for t_ = 1:size(t,1)
    
    vinyl_sum = 0;
    radic_sum = 0;
    monomer_species_conc = reshape(monomer_species(t_,:), resin_monomers, vmax +1, pmax +1, nmax+1, nmax +1, nmax +1);
    
    
    for i = 1:resin_monomers                              % all the monomers
        monomer = monomers(i);                            % all the species for a monomer
        for v = 1:monomer.vmax +1                         % vinyl_groups
            for p = 1:monomer.pmax +1                     % radicals
                for b_in = 1:monomer.nmax +1              % outgoing bonds  (monomer/polymer radical attacks other monomer/polymer vinyl)
                    for b_out = 1:monomer.nmax +1         % incomming bonds (monomer/polymer vinyl is attacked by other monomer/polymer radical)
                        for b_neutral = 1:monomer.nmax +1 % neutral bonds   (monomer/polymer radical termination by combination)
                            vinyl_sum = vinyl_sum  + (v-1) * monomer_species_conc(i,v,p,b_in,b_out,b_neutral);
                            radic_sum = radic_sum  + (p-1) * monomer_species_conc(i,v,p,b_in,b_out,b_neutral);
                            vinyl_over_time_big_Split(i,t_) =   vinyl_over_time_big_Split(i,t_) + (v-1) * monomer_species_conc(i,v,p,b_in,b_out,b_neutral);
                            radical_over_time_big_Split(i,t_) = radical_over_time_big_Split(i,t_) + (p-1) * monomer_species_conc(i,v,p,b_in,b_out,b_neutral);
                        end
                    end
                end
            end
        end
    end
    
    vinyl_over_time_small(   t_) = sum( y( t_,[species_indexes.small_system_monomers] ) );
    radical_over_time_small( t_) = sum( y( t_,[species_indexes.small_system_radicals] ) );
    
    vinyl_over_time_big(t_)   = vinyl_sum;
    radical_over_time_big(t_) = radic_sum;
    
end




max_vinyl_dif   = max( abs(vinyl_over_time_big - vinyl_over_time_small) );
max_radical_dif = max( radical_over_time_big(:) - sum( y(:,[species_indexes.small_system_radicals]), 2 ) );

if max_vinyl_dif > margin || max_radical_dif > margin || true
    disp([newline,'Difference in concentration between big and small system:'])
    if ~draw.none && ( draw.error || draw.error_detailed || draw.all )
        i = 1;
        disp(['-           vinyl_big/small: ', num2str(max_vinyl_dif,   '%10.5e\n'), ' figure: ', num2str(figures+i)]); i = i +1;
        disp(['-         radical_big/small: ', num2str(max_vinyl_dif,   '%10.5e\n'), ' figure: ', num2str(figures+i)]); i = i +1;
        disp(['- vinyl_&_radical_big/small: ', num2str(max_vinyl_dif,   '%10.5e\n'), ' figure: ', num2str(figures+i)]); i = i +1;
        disp(['-   Max_radical_&_vinyl_dif: ', num2str(max_radical_dif, '%10.5e\n'), ' figure: ', num2str(figures+i)]);
        temp_header = strings( size(monomers) );
        for i = 1:resin_monomers
            temp_header(i) = join( ["bigsystem: " monomers(i).name]);
        end
        % plots vinyl's in big and small system
        if ~draw.none && ( draw.error_detailed || draw.all )
            plot_concentrations(t,  ...
                                [   vinyl_over_time_big,                                 ...     big system : all the vinyls
                                    vinyl_over_time_big_Split',                           ...     big system : the vinyls per monomer
                                    sum(y(:,[species_indexes.small_system_monomers]),2), ... small sysstem  : all the vinyls
                                    y(:,[species_indexes.small_system_monomers])         ... small system   : the vinyls per monomers
                                 ], ...
                                [   "Total big vinyl", ...
                                    temp_header, ...
                                    join(header(species_indexes.small_system_monomers), ' + '), ...
                                    header(species_indexes.small_system_monomers)
                                 ], ...
                                "Vinyl: Big VS Small")
        end
        % plots radicals in big and small system                
        if ~draw.none && ( draw.error_detailed || draw.all )
            plot_concentrations(t,  ...
                                [   radical_over_time_big,                                 ...     big system : all the vinyls
                                    radical_over_time_big_Split',                           ...     big system : the vinyls per monomer
                                    sum(y(:,[species_indexes.small_system_radicals]),2), ... small sysstem  : all the vinyls
                                    y(:,[species_indexes.small_system_radicals])         ... small system   : the vinyls per monomers
                                 ], ...
                                [   "Total big vinyl", ...
                                    temp_header, ...
                                    join(header(species_indexes.small_system_radicals), ' + '), ...
                                    header(species_indexes.small_system_radicals)
                                 ], ...
                                "Radicals: Big VS Small")
        end
        % plots radicals and vinyls in big vs small system                
        
        plot_concentrations(t,  ...
                                [   vinyl_over_time_big,   y(:,[species_indexes.small_system_monomers]),    ...
                                    sum(                   y(:,[species_indexes.small_system_monomers]),2), ...
                                                                                                            ...
                                    radical_over_time_big, y(:,[species_indexes.small_system_radicals]),    ...
                                    sum(                   y(:,[species_indexes.small_system_radicals]),2)  ...
                                 ], ...
                                [   "big vinyl",    header(species_indexes.small_system_monomers),      ...
                                    join(header(species_indexes.small_system_monomers), ' + '),         ...
                                                                                                        ...
                                    "big radicals", header(species_indexes.small_system_radicals)       ...
                                    join(header(species_indexes.small_system_radicals), ' + ')          ...
                                 ], ...
                                "Vinyl & radical big VS small")
        % plots the difference between the big and small system                
        plot_concentrations(t, ...
                                [  abs( vinyl_over_time_big(:)   - sum( y(:,[species_indexes.small_system_monomers]), 2 ) ), ...
                                   abs( radical_over_time_big(:) - sum( y(:,[species_indexes.small_system_radicals]), 2 ) ) ...
                                   ], ...
                                [  "big vinyl VS small vinyl", ...
                                   "big radicals VS small radicals" ...
                                   ], ...
                                "Vinyl & radical big VS small")
    else
        disp(['-   Max_vinyl_dif: ', num2str(max_vinyl_dif)])
        disp(['- Max_radical_dif: ', num2str(max_radical_dif)])
    end
end
result.species_indexes = species_indexes;
result.parameters = parameters;
result.differenc_errors = differenc_errors;

disp(newline)
