function [ k ] = return_dummy_rates(parameters)
%RETURN_RATES returns the reaction rates for the species
%   each element in k reprecents te reaction rate of 1 reaction that can
%   occur in the system, references needed for accurate rates. now they were chosen at random ;)


% ref 1: Polymer 44 (2003) 5219–5226
% ref 2: Chemical Engineering Science; Volume 57, Issue 5, March 2002, Pages 887-900
% ref 3: Helvetica Chimica Acta ± Vol. 84 (2001) 


%% constants

initiator = parameters.initiator;

nA = 6.023e23;  % Avagadro?s number
c  = 2.998e8;   % speed of light
h  = 6.626e-34; % plancs constant



E_Initiator_photon  =   nA*h*c/initiator.nu; % JK E = N_A*h*c/lambda
I_light             =   100; % mW / cm^2
phi                 =   1; % #NOREF# initiator concentration?    % G&B
eps                 =   36.5*2.3;  % Oce  == monomer.eps_458 ?

%# ref 2; eq 8 -> Ri = eps*I*[Initator] / E'
%  E' is the energy per mole of photons

Igs         =   initiator.eps_458 * phi * I_light/E_Initiator_photon;


%% formation of active species from Photo-Initiator (CQ) and Co-Initiator
% rates in form: k . (I)nitiator (g)round to (s)inglet
%k.Igs = 2.303 * I0 * epsi(I)

k.Igs = 10;                  % #ref 2#  CQ-Ground  -> CQ-Singlet
k.Isg = 0;                   % #ref 1, p.5222#  CQ-Singlet -> CQ-Ground
k.Ist = 10;                 % #ref 3, p.2584#  CQ-Singlet -> CQ-Triplet
k.Ideg = 0;                          % #NOREF#  degredation (/oxidation only?)

a = 0;                               % #NOREF#  small a means small loss of initator through degredation(/oxidation/peroxide formation?)
k.Itg = (1-a)*k.Ideg;                %          (1-a)k3  CQ-Triplet -> CQ-Ground              %quenching
k.Ilost = a * k.Ideg;                %          ak3      CQ-Triplet -> degredation products
%# k.ItgM physical quenching by the monomer 

% beta  = factor that becomes active species
% gamma = factor that losses radical and returns to ground state
% 1-beta-gamma = loss of I and CoI through degredation

beta = 0.5; gamma = 0.5; 

k.Ite = 50;                  % CQ-triplet -> singlet-exciplex
k.Ise = 5;                  % CQ-singlet -> triplet-exciplex

k.Eform = k.Ite;
k.Eact = beta * k.Eform;             %          Active species formation
k.Edeact = gamma * k.Eform;          %          Deactivation
k.Elost = (1-beta-gamma) * k.Eform;  %          Degredation products

%% Inhibitor

k.IHgr  = 100;     % IN-ground   -> 2 IN-r
k.IHrg  = 5;      % 2 + IN-r    -> IN-ground
k.IHpol = 100;     % POLr + IN-r -> POL-IN
 

%% formation of polymer

k.Pinit = 20;  % Eact + V    -> POLr
k.Pprop = 10; % POLr + V    -> POLr + B
k.Ptr = 5;    % POLr + POLr -> B
k.Ptd = 1;    % POLr + POLr -> POL + POL

%% Interaction with Oxygen

k.Oop = 2e8; %  #ref 1#


end

