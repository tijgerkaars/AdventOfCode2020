function [co_initiator] = choose_co_initiator(input,conc, type)
%CHOOSE_INITIATOR returns a struct containing the initiator specifications
% by inputting the abreviation of the initiator
%   Detailed explanation goes here

co_initiator.name = input;

if strcmp(input,'test')
    co_initiator.pmax = 1;                  % max number of radicals on a monomer unit
    co_initiator.M    = 10;                 % g/mol
    co_initiator.dens = 1;                  % g/mL at 25 °C
    co_initiator.eps  = 1;                  % M^-1 cm^-1
    co_initiator.visc = [];                 % mPa s
elseif strcmp(input, 'EDAB') % solid
    co_initiator.pmax = 1;                  
    co_initiator.M    = 193.24;                 
    co_initiator.dens = 1.04;
    co_initiator.eps  = [];
    co_initiator.visc = [];
elseif strcmp(input, 'MDEA')
    co_initiator.pmax = 1;                  
    co_initiator.M    = 119.163;                 
    co_initiator.dens = 1.04;
    co_initiator.eps  = [];
    co_initiator.visc = 101;
end

if strcmp(type, 'mol')
    co_initiator.conc     = conc;
elseif strcmp(type, 'g')
    conc_ = conc/co_initiator.M;
    co_initiator.conc     = conc_;
else
    disp("That input type is not supported")
end

