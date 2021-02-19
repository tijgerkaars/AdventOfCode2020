clear all
% clf             % clears plots from previous runs
starting_time = datetime('now');
format shortE

global figures marker
figures = 0;
marker  = false;

%------------------------------------------------------------------------------------

conc_factor = 1;
parameters.conc_factor = conc_factor;
grams = 150;

conc_CQ   = 0.0060;
conc_EDAB = 0.0030;
conc_HABI = 0.0027;

conc_monomers_fraction = (1 - (conc_CQ + conc_EDAB + conc_HABI));
conc_monomer = conc_monomers_fraction * grams;

conc_CQ = conc_CQ * grams; conc_EDAB = conc_EDAB * grams; conc_HABI = conc_HABI * grams;

parameters.initiator         = choose_initiator(   'CQ',        0.002,   'mol', 458);
% parameters.initiator.conc    = conc_factor * parameters.initiator.conc;
parameters.co_initiator      = choose_co_initiator('EDAB',      0.001, 'mol');
% parameters.co_initiator.conc = conc_factor * parameters.co_initiator.conc;
parameters.inhibiter         = choose_inhibitor(   'o-Cl-HABI', 0, 'mol');
% parameters.inhibiter.conc    = conc_factor * parameters.inhibiter.conc;

parameters.init_intensity = 10;
parameters.inhi_intensity = 0;

parameters.oxygen.conc    = 0;


% Monomer specifications
% NPM, TEGDVE, bisGMA, TEGDMA, BPAEDA, PEGDA
i = 1;

monomers(1) = choose_monomer('PEGDA', conc_monomer, 'g'); i = i+1;
monomers(2) = choose_monomer('NPM', conc_monomer, 'g'); i = i+1;

for i = 1:size(monomers,2)
    monomers(i).conc = conc_factor * monomers(i).conc;
end

clear monomers
monomers(1) = choose_monomer('PEGDA', 1, 'mol');

parameters.monomers = monomers;

%------------------------------------------------------------------------------------

k_ = return_rates(parameters);
parameters.k = k_;

parameters.t_span = 5000;

parameters.RRE_allowed_error = 1e-15;
parameters.deg3d_gel_F_tol = 10e-5;
parameters.Ms2_F_tol = 10e-6;

%------------------------------------------------------------------------------------

parameters.run = 1;
parameters.total_runs = 1;
parameters.prefix = 'system over time: ';
parameters.run_times.start_time = starting_time;

%------------------------------------------------------------------------------------

calc_.all                         = false;

calc_.ode                         = true;
calc_.deg                         = true;
calc_.gel_point                   = true;
calc_.comp_size_distr_gelpoint_3d = false;
calc_.ms2                         = false;
calc_.gel_frac                    = true;

parameters.calc = calc_;

%------------------------------------------------------------------------------------

draw_.all = false;

draw_.none = true;



if draw_.none
    draw_.all = false;
else
    if draw_.all
        parameters.calc.all = true;
    end
end % gives draw.none priority

draw_.small_syst         = false;
draw_.all_monomers       = false;
draw_.valid_monomers     = false;
draw_.non_valid_monomers = false;
draw_.compare_monomers   = false;
draw_.summed_bonds       = false;
draw_.typed_bonds        = false;
draw_.small_conversion   = false;
draw_.big_conversion     = false;
draw_.ms2                = true; 
draw_.comp_sizedist_gel  = false;
draw_.error              = true;
draw_.error_detailed     = false;

parameters.draw = draw_;

%------------------------------------------------------------------------------------

test      = false;

run_model = true;

filename  = '99-99: Test_run';

over_write_file = true;

%------------------------------------------------------------------------------------
if run_model
    load_file = false;
end
%------------------------------------------------------------------------------------
%% Dummy struct for checking empty if empty
%{
a=struct('field1',1,'field2',2,'field3',5)
b=struct('field1',3,'field3',4,'field4',6)
f1=fieldnames(a)
f2=fieldnames(b)
f=intersect(f1,f2)
a=rmfield(a,f)
b=rmfield(b,f)
%}
dummy_struct.run_id             = [];
dummy_struct.run_times          = [];
dummy_struct.state_zero         = [];
dummy_struct.RRE_y              = [];
dummy_struct.RRE_t              = [];
dummy_struct.header             = [];
dummy_struct.errors_in_RRE      = [];
dummy_struct.small_conversion   = [];
dummy_struct.degree             = [];
dummy_struct.degree_header      = [];
dummy_struct.typed_degree       = [];
dummy_struct.typed_degree_header= [];
dummy_struct.checkgel_3d        = [];
dummy_struct.gel_i              = [];
dummy_struct.gel_conv_3d        = [];
dummy_struct.deg3d_gel          = [];
dummy_struct.C_gel              = [];
dummy_struct.gel_conv           = [];
dummy_struct.species_indexes    = [];
dummy_struct.parameters         = [];
dummy_struct.differenc_errors   = [];
%%
if run_model || test
    if draw_.none
        disp([newline, 'No plots will be made'])
    elseif draw_.all
        disp([newline, 'Drawing ALL plots for EACH run'])
    else
        disp([newline, 'Drawing selected plots for each run'])
    end
    if test || false 
        disp('running test')
        
        [end_results.results(1,1),end_results.warning(1,1)] = run(parameters);
        end_results.results(1,1).parameters.draw.none = false;
        % plot_result(end_results.results(i,1))
        save(filename, 'end_results')
        clear end_results
        
        
        return
    else
        %%
        
        light_range = [0, logspace(-1,3,11)];
        
        conc_range  = logspace(-5,0,10); 
                       
        parameters_ = parameters;
        %% 1 screen for working range
        if true
            filename = ': screening_screening_functionality_no_ihib_intensity_large';
            filename = [  datestr( datetime('now') , 'mm-DD' ) , filename ];
            
            parameters_ = parameters;
            parameters_.run_times.start_time = datetime('now');
            
            parameters_.calc.gel_frac = false;
            
            parameters_.initiator         = choose_initiator(   'CQ',        1.2e-2, 'mol', 458);
            parameters_.co_initiator      = choose_co_initiator('EDAB',      0.6e-2, 'mol');
            parameters_.inhibiter         = choose_inhibitor(   'o-Cl-HABI', 1.2e-2, 'mol');

            parameters_.init_intensity = 1;
            parameters_.inhi_intensity = 0;

            monomers(1) = choose_monomer('PEGDA', 1, 'mol');
            monomers(2) = choose_monomer('NPM',   1, 'mol');

            light_range = logspace(0,3,10);
            functionality_range = [0:0.1:1];

            parameters_.monomers = monomers;

            screening_functionality(parameters_,         ...
                                    light_range,         ...
                                    functionality_range, ...
                                    filename)              %
        end          %% 2 screen for working range
        if true
            filename = ': screening_screening_functionality_extreem_ihib_intensity_large';
            filename = [  datestr( datetime('now') , 'mm-DD' ) , filename ];
            
            parameters_ = parameters;
            parameters_.run_times.start_time = datetime('now');
            
            parameters_.calc.gel_frac = false;
            
            parameters_.initiator         = choose_initiator(   'CQ',        1.2e-2, 'mol', 458);
            parameters_.co_initiator      = choose_co_initiator('EDAB',      0.6e-2, 'mol');
            parameters_.inhibiter         = choose_inhibitor(   'o-Cl-HABI', 1.2e-2, 'mol');

            parameters_.init_intensity = 1;
            parameters_.inhi_intensity = 1000;

            monomers(1) = choose_monomer('PEGDA', 1, 'mol');
            monomers(2) = choose_monomer('NPM',   1, 'mol');

            light_range = logspace(0,3,10);
            functionality_range = [0:0.1:1];

            parameters_.monomers = monomers;

            screening_functionality(parameters_,         ...
                                    light_range,         ...
                                    functionality_range, ...
                                    filename)              %
        end          %% 3 screen for working range
        if false
            filename = ': screening_screening_functionality_med_ihib_intensity_large';
            filename = [  datestr( datetime('now') , 'mm-DD' ) , filename ];
            
            parameters_ = parameters;
            parameters_.run_times.start_time = datetime('now');
            
            parameters_.calc.gel_frac = false;
            
            parameters_.initiator         = choose_initiator(   'CQ',        1.2e-2, 'mol', 458);
            parameters_.co_initiator      = choose_co_initiator('EDAB',      0.6e-2, 'mol');
            parameters_.inhibiter         = choose_inhibitor(   'o-Cl-HABI', 1.2e-2, 'mol');

            parameters_.init_intensity = 1;
            parameters_.inhi_intensity = 25;

            monomers(1) = choose_monomer('PEGDA', 1, 'mol');
            monomers(2) = choose_monomer('NPM',   1, 'mol');

            light_range = logspace(0,3,10);
            functionality_range = [0:0.1:1];

            parameters_.monomers = monomers;

            screening_functionality(parameters_,         ...
                                    light_range,         ...
                                    functionality_range, ...
                                    filename)              %
        end  
        return
        %% Concentration screening
        parameters_ = parameters;
        filename = ': screening_Monomer_concentrations_0_10_20__0_10_20';
        filename = [  datestr( datetime('now') , 'mm-DD' ) , filename ];
        
        conc_monomers_1 = conc_monomers_fraction/2 * grams;
        conc_monomers_2 = conc_monomers_fraction/2 * grams;
        
        monomers(1) = choose_monomer('PEGDA', conc_monomers_1, 'g');
        monomers(2) = choose_monomer('NPM',   conc_monomers_2, 'g');
        
        for i = 1:size(monomers,2)
            monomers(i).conc = conc_factor * monomers(i).conc;
        end
        parameters_.monomers = monomers;
        
        monomers_1_cons_range = [0,10,20];
        monomers_2_cons_range = [0,10,20];
            
        screen_monomers_concentrations(parameters_, ...
            monomers_1_cons_range,  ...
            monomers_2_cons_range,  ...
            conc_monomers_fraction, ...
            filename);
            
        try 
            temp = 0;
            clear temp
        catch
            disp('failed here')
        end
        %% Reactivity screening
        parameters_ = parameters;
        filename = ': Screen_reactivity_ratios_debug_PEGDA_NPM_1_10__1_10';
        filename = [  datestr( datetime('now') , 'mm-DD' ) , filename ];
        parameters_.inhibiter.conc = 0;
        parameters_.monomers(1) = choose_monomer('HDDA', 100, 'mol');
        parameters_.monomers(2) = choose_monomer('NPM', 500, 'mol');
        range_1 = [0:10:100];
        range_2 = [0:10:100];
        
        try
            screen_reactivity_ratios(parameters_, ...
                                     range_1,     ...
                                     range_2,     ...
                                     filename);     %
        catch
            disp('failed the reactivity ratio screening')
        end
        %%
        parameters_ = parameters;
        filename = ': Screen_init_inhib_light_comp_exp_ranges_HDDA';
        filename = [  datestr( datetime('now') , 'mm-DD' ) , filename ];

        
        if isfile([filename,'.mat'])
            disp('That file name is already in use')
            if ~over_write_file
                return
            end
        elseif ismember(filename, '.')
            disp(['A "." is in the filename. The file probably wont save right', newline, 'quiting'])
        end
                
        Init_intesity_range = [3,5,8,10,18,26];
        Inhi_intesity_range = [0,5,10,21];
        parameters.run = 1;
        parameters.total_runs = max(size(Init_intesity_range)) * max(size(Inhi_intesity_range)); 	
        disp(filename)
        
        try
            screen_init_inhib_light(parameters_, ...
                                    Init_intesity_range, ...
                                    Inhi_intesity_range, ...
                                    filename);
        catch
            disp(["failed screening:", newline, filename])
        end
        %% Concentration screening
        parameters_ = parameters;
        filename = ': Screen_reactivity_ratios_debug_PEGDA_NPM_1_10__1_10';
        filename = [  datestr( datetime('now') , 'mm-DD' ) , filename ];
        parameters_.inhibiter.conc = 0;
        parameters_.monomers(1) = choose_monomer('HDDA', 100, 'mol');
        parameters_.monomers(2) = choose_monomer('NPM', 500, 'mol');
        range_1 = [0:10:100];
        range_2 = [0:10:100];
        
        screen_reactivity_ratios(parameters_, ...
                                 range_1,     ...
                                 range_2,     ...
                                 filename);     %
        parameters_ = parameters;
        filename = ': screening_Monomer_concentrations_100_1000_100_1000';
        filename = [  datestr( datetime('now') , 'mm-DD' ) , filename ];
        monomers_1_cons_range = [1:10] * 100;
        monomers_2_cons_range = [1:10] * 100;
        
        try
            parallel_screen_monomers_concentrations(parameters_, ...
                                                   monomers_1_cons_range, ...
                                                   monomers_2_cons_range, ...
                                                  [filename '_parallel']);
        catch
            screen_monomers_concentrations(parameters_, ...
                                          monomers_1_cons_range, ...
                                          monomers_2_cons_range, ...
                                          filename);
        end
        
        
        
        %{
        x = 20; y = 10;
        % results(x,y) = dummy_struct;
        for i = 1:x
            for j = 1:y
                parameters.run = (i-1)*y + j;
                parameters.file_name = filename;
                parameters.X_Y = [x,i,y,j];
                parameters.prefix = ['Run ', num2str(parameters.run), '/', num2str(x*y)];
                
                %-------- Customise parameters --------%
                new_x = 5  + (i-1) * 20;
                var_x = 'R25';
                new_y = 20 + (j-1) * 10;
                var_y = 'R52';
                parameters.monomers(1).K.(var_x) = new_x;
                parameters.monomers(2).K.(var_y) = new_y;
                parameters.x_axis = new_x;
                parameters.y_axis = new_y;
                %-----------------------------------------%
                %-------- Customise figure prefix --------%
                monomers = parameters.monomers;
                temp_string = '';
                for t = 1:size(monomers,2)
                    temp_string = [temp_string, monomers(t).name, '/', num2str(monomers(t).conc), ' ']; %#ok<AGROW>
                end
                parameters.prefix = [parameters.prefix, ' - monomers: ', temp_string, newline];
                disp(parameters.prefix)
                %-----------------------------------------%
                %------------- Run the model -------------%
                
                results(i,j) = run(parameters);
            end
        end
        %------------------------------------------------------------------------------------
        
        heatmap_plot(results, var_x, var_y,  'gel_i')
        
        %------------------------------------------------------------------------------------
        %}
    end
    disp(end_results)
end

%------------------------------------------------------------------------------------


%% reminders
%{

NPM polymerization ref: Polym. Chem., 2017, 8, 6909; Toward alternating copolymerization of maleimide and vinyl acetate driven by hydrogen bonding


python functions/options are a thing

order = py.dict(pyargs('soup',3.57,'bread',2.29,'bacon',3.91,'salad',5.00));


~

%}

run_time = datetime('now') - starting_time;
disp([newline, 'RUN MAIN --- run time: ', datestr(run_time,'HH:MM:SS'), ' - Finished at; ', datestr( datetime('now'),'HH:MM:SS' )])
disp([newline,newline])

