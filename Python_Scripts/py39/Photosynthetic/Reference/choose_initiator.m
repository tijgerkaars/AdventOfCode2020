function [initiator] = choose_initiator(input, conc, type, eps)
%CHOOSE_INITIATOR returns a struct containing the initiator specifications
% by inputting the abreviation of the initiator
%   dens = [] if solid
%   eps_x = molar absorbtion coefficient for X nm

initiator.name = input;

if strcmp(input,'test')
    initiator.state = 'Imaginary';
    initiator.pmax     = 1;       % max number of radicals on a monomer unit
    initiator.M        = 10;      % g/mol
    initiator.dens     = -1;      % g/mL at 25 °C
    initiator.eps      = 1;       % M^-1 cm^-1 || cm^−1 /(mol/L)
    initiator.nu       = -100;    % wavelength nm
elseif strcmp(input, 'CQ')
    initiator.state = 'Solid';
    initiator.pmax     = 4;                  
    initiator.M        = 166.22;                 
    initiator.dens     = [];
    initiator.eps_458  = 40;      % cm^−1 /(mol/L)
    initiator.eps_469  = 46;      % cm^−1 /(mol/L)
    % initiator.eps_469  = 51.4;    % ref zotero eps
    initiator.eps_405  = 6.80;    % ref zotero eps
    initiator.eps_365  = 2.05;    % ref zotero eps
    initiator.nu       = eps*1e-9;
end

if strcmp(type, 'mol')
    initiator.conc     = conc;
elseif strcmp(type, 'g')
    conc_ = conc/initiator.M;
    initiator.conc     = conc_;
else
    disp("That input type is not supported")
end

initiator.eps = initiator.(['eps_', num2str(eps)]);

