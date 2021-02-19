function [monomer] = choose_monomer(input,conc,type)
%CHOOSE_MONOMER returns a struct containing the specifications for the
%monomer by inputting the name of the wanted monomer
%   Molarmass and densitys from Sigma Aldrich
%   RMG sources from estimation software https://rmg.mit.edu
%   RMG 1: reduced-PEGDA-230-prop | indege/ !outedge

kdummy = 1e4;

if strcmp(input, 'test') || strcmp(input, '-1')
    %%
    monomer.name   = 'test';           % store the monomer for graphs etc
    monomer.tag    = '-1';             % numerical tag to make picking the Rij easier
    monomer.vmax   = 2;                % max number of vinyl groups in monomer
    monomer.pmax   = 2;                % max number of radicals on a monomer unit
    monomer.nmax   = 2 * monomer.vmax; % max number of bonds per monomer unit
    monomer.M      = 50;               % g/mol
    monomer.dens   = 1;                % g/mL at 25 °C
    monomer.K.Rii  = 1;                % always 1 as reactivity with itself is 1
    monomer.K.Rij  = 1;                % the reactivity rate of the reaction between radical i and monomer j
    monomer.K.init = 7*kdummy;
    monomer.K.prop = kdummy;           % the propogation rate of this monomer
    monomer.K.tr   = kdummy;           % the recombination termination rate of this monomer
    monomer.K.td   = kdummy;           % the disproportionation termination rate of this monomer
elseif strcmp(input, 'BPAEDA') || strcmp(input, '1')
    %%
    monomer.name   = 'BPAEDA';
    monomer.tag    = '1';
    monomer.vmax   = 2;
    monomer.pmax   = 2;
    monomer.nmax   = 2 * monomer.vmax;
    monomer.M      = 688;
    monomer.dens   = 1.15;
    monomer.K.R11  = 1;
    monomer.K.R12  = 1;
    monomer.K.R13  = 1;
    monomer.K.R14  = 1;
    monomer.K.R15  = 1;
    monomer.K.R16  = 1;
    monomer.K.R17  = 1;
    monomer.K.init = 7*kdummy;
    monomer.K.prop = 7*kdummy;
    monomer.K.tr   = 100*kdummy;
    monomer.K.td   = 100*kdummy;
elseif strcmp(input, 'TEGDMA')  || strcmp(input, '2')
    %%
    monomer.name   = 'TEGDMA';
    monomer.tag    = '2';
    monomer.vmax   = 2;
    monomer.pmax   = 2;
    monomer.nmax   = 2 * monomer.vmax;
    monomer.M      = 286.32;
    monomer.dens   = 1.092;
    monomer.K.R22  = 1;
    monomer.K.R21  = 1;
    monomer.K.R23  = 1;
    monomer.K.R24  = 1;
    monomer.K.R25  = 1;
    monomer.K.R26  = 1;
    monomer.K.R27  = 1;
    monomer.K.init = 7*kdummy;
    monomer.K.prop = 7*kdummy;
    monomer.K.tr   = 100*kdummy;
    monomer.K.td   = 100*kdummy;
elseif strcmp(input, 'bisGMA') || strcmp(input, '3')
    %%
    monomer.name   = 'bisGMA';
    monomer.tag    = '3';
    monomer.vmax   = 2;
    monomer.pmax   = 2;
    monomer.nmax   = 2 * monomer.vmax;
    monomer.M      = 512.59;
    monomer.dens   = 1.161;
    monomer.K.R33  = 1;
    monomer.K.R31  = 1;
    monomer.K.R32  = 1;
    monomer.K.R34  = 1;
    monomer.K.R35  = 1;
    monomer.K.R36  = 1;
    monomer.K.R37  = 1;
    monomer.K.init = 5*kdummy;
    monomer.K.prop = 1*kdummy;
    monomer.K.tr   = 100*kdummy;
    monomer.K.td   = 100*kdummy;
elseif strcmp(input, 'TEGDVE') || strcmp(input, '4')
    %%
    monomer.name   = 'TEGDVE';
    monomer.tag    = '4';
    monomer.vmax   = 2;
    monomer.pmax   = 2;
    monomer.nmax   = 2 * monomer.vmax;
    monomer.M      = 202.25;
    monomer.dens   = 0.99;
    monomer.K.R44  = 1;
    monomer.K.R41  = 1;
    monomer.K.R42  = 1;
    monomer.K.R43  = 1;
    monomer.K.R45  = 1;
    monomer.K.R46  = 1;
    monomer.K.R47  = 1;
    monomer.K.init = 5*kdummy;
    monomer.K.prop = 1*kdummy;
    monomer.K.tr   = 100*kdummy;
    monomer.K.td   = 100*kdummy;
elseif strcmp(input, 'NPM')    || strcmp(input, '5')
    %%
    monomer.name   = 'NPM'; % N-Propylmaleimide
    monomer.tag    = '5';
    monomer.vmax   = 1;
    monomer.pmax   = 1;
    monomer.nmax   = 2 * monomer.vmax;
    monomer.M      = 139.15;
    monomer.dens   = 1.112;
    monomer.K.R55  = 1;
    monomer.K.R51  = 1;
    monomer.K.R52  = 1;
    monomer.K.R53  = 1;
    monomer.K.R54  = 1;
    monomer.K.R56  = 1;
    monomer.K.R57  = 1;
    monomer.K.init = 3*kdummy;
    monomer.K.prop = 3*kdummy;
    monomer.K.tr   = 100*kdummy;
    monomer.K.td   = 100*kdummy;
elseif strcmp(input, 'PEGDA')  || strcmp(input, '6')
    %%
    monomer.name   = 'PEGDA';
    monomer.tag    = '6';
    monomer.vmax   = 2;
    monomer.pmax   = 2;
    monomer.nmax   = 2 * monomer.vmax;
    monomer.M      = 360.18;
    monomer.dens   = 1.11;
    monomer.K.R66  = 1;
    monomer.K.R61  = 1;
    monomer.K.R62  = 1;
    monomer.K.R63  = 1;
    monomer.K.R64  = 1;
    monomer.K.R65  = 1;
    monomer.K.R67  = 1;
    monomer.K.init = 5.787e+05;  % L/mol s %% rmg
    monomer.K.prop = 2.878e+04; % + 227.6 + 250.5; % L/mol s %% rmg 1!: R 173, 174, 196
    % monomer.K.tr   = 8.658e+8;  % L/mol s %% rmg
    % monomer.K.td   = 1.21e+9;   % L/mol s %% rmg RMG 1: R 291
    monomer.K.tr   = 4.3955e7;
    monomer.K.td   = 4.3955e7;
elseif strcmp(input, 'HDDA')  || strcmp(input, '7')
    %%
    monomer.name   = 'HDDA';
    monomer.tag    = '7';
    monomer.vmax   = 2;
    monomer.pmax   = 2;
    monomer.nmax   = 2 * monomer.vmax;
    monomer.M      = 226.27;
    monomer.dens   = 1.01;
    monomer.K.R77  = 1;
    monomer.K.R71  = 1;
    monomer.K.R72  = 1;
    monomer.K.R73  = 1;
    monomer.K.R74  = 1;
    monomer.K.R75  = 1;
    monomer.K.R76  = 1;
    monomer.K.init = 6.1197e4;
    monomer.K.prop = 6.1197e4;
    monomer.K.tr   = 4.3955e7;
    monomer.K.td   = 4.3955e7;
else
    disp('This monomer has not yet been added, did you type it right dummy?')
end


if strcmp(type, 'mol')
    monomer.conc     = conc;
elseif strcmp(type, 'g')
    conc_ = conc/monomer.M;
    monomer.conc     = conc_;
else
    disp("That input type is not supported")
end