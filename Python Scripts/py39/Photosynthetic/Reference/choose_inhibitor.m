function [inhibitor] = choose_inhibitor(input, conc, type)
%CHOOSE_INHIBITOR Summary returns a struct containing the inhibitor specifications
% by inputting the abreviation of the inhibitor
%   eps_x = molar absorbtion coefficient for X nm

%{
%     ref 1 = Photoinitiators for Polymer Synthesis: Scope, Reactivity, and
Efficiency; p.244
%}


inhibitor.name = input;

if strcmp(input,'test')
    inhibitor.state = 'Imaginary';
    inhibitor.pmax     = 1;       % max number of radicals generated per inhibitor molecule
    inhibitor.M        = 10;      % g/mol
    inhibitor.dens     = -1;      % g/mL at 25 °C
    inhibitor.eps      = 1;       % M^-1 cm^-1
    inhibitor.nu       = -100;    % wavelength
elseif strcmp(input, 'o-Cl-HABI')
    inhibitor.state    ='Solid';
    inhibitor.pmax     = 2;                  
    inhibitor.M        = 659.6;                 
    inhibitor.dens     = [];
    inhibitor.eps_366  = 400;    % ref 1
    inhibitor.eps_469  = 5.69;   % ref zotero eps
    inhibitor.eps_405  = 219;    % ref zotero eps 
    inhibitor.eps_365  = 376;    % ref zotero eps 
    
    inhibitor.nu       = 366e-9;
end

if strcmp(type, 'mol')
    inhibitor.conc     = conc;
elseif strcmp(type, 'g')
    conc_ = conc/inhibitor.M;
    inhibitor.conc     = conc_;
else
    disp("That input type is not supported")
end