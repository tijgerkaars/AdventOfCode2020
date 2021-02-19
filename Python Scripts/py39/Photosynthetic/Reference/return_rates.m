function [ k ] = return_rates(parameters)
%RETURN_RATES returns the reaction rates for the species
%   each element in k reprecents te reaction rate of 1 reaction that can
%   occur in the system, references needed for accurate rates. now they were chosen at random ;)


% ref 1: Polymer 44 (2003) 5219–5226
% ref 2: Chemical Engineering Science; Volume 57, Issue 5, March 2002, Pages 887-900
% ref 3: Helvetica Chimica Acta ± Vol. 84 (2001) 
% ref 4: Macromolecules 1995, 28, 636-641; ESR Study of Lophyl Free Radicals in Dry Films
% ref 5: Journal of Luminescence 63 (1995) 183-l 88

%% constants

%{
k = return_dummy_rates(parameters);

return
%}

initiator = parameters.initiator;
inhibitor = parameters.inhibiter;
monomers  = parameters.monomers;


nA = 6.023e23;  % Avagadro?s number
c  = 2.998e8;   % speed of light
h  = 6.626e-34; % plancs constant



E_Initiator_photon  =   nA*h*c/initiator.nu;       % JK E = N_A*h*c/lambda
I_light_init        =   parameters.init_intensity; % mW / cm^2
phi_init            =   1; % #ref 3# initiator concentration?    % G&B


%### eps                 =   36.5*2.3;  % Oce  == monomer.eps_458 ?
%# ref 2; eq 8 -> Ri = eps*I*[Initator] / E'
%  E' is the energy per mole of photons

Igs                 =   initiator.eps * phi_init * I_light_init/E_Initiator_photon;


%% formation of active species from Photo-Initiator (CQ) and Co-Initiator
% rates in form: k . (I)nitiator (g)round to (s)inglet
%k.Igs = 2.303 * I0 * epsi(I)

% Materials for the Direct Restoration of Teeth 2016, Pages 37-67 suggest
% that 4 radicals  are formed per CQ, the image shows CQ reacting with
% oxygen. The main reaction however should be with the Co-Initiator, so it
% should generate 2 radicals

k.Igs = Igs;                         % #ref 2#  CQ-Ground  -> CQ-Singlet
% k.Igs = 0.1296; % test value
k.Isg = 0;                           % #ref 1, p.5222#  CQ-Singlet -> CQ-Ground
k.Ist = 1.7e5;                       % #ref 5, p.186 #  CQ-Singlet -> CQ-Triplet
k.Itg = 1/19;                        % #ref 5, p.186 #  CQ-Triplet -> CQ-Ground   (1/kp)
k.Ideg = 0;                          % #NOREF#  degredation (/oxidation only?)


k.Ilost = 0;
%{
a = 0;                               % #NOREF#  small a means small loss of initator through degredation(/oxidation/peroxide formation?)
k.Itg = (1-a)*k.Ideg;                %          (1-a)k3  CQ-Triplet -> CQ-Ground              %quenching
k.Ilost = a * k.Ideg;                %          ak3      CQ-Triplet -> degredation products
%# k.ItgM                            % physical quenching by the monomer 
%}
% beta  = factor that becomes active species
% gamma = factor that losses radical and returns to ground state
% 1-beta-gamma = loss of I and CoI through degredation (oxygen dependend?)
beta = 0.5; gamma = 0.5;             % #NOREF#

% one source doesn't mention the Ise 
k.Ite = 2.0 * 10^8;                  % #ref 1#  CQ-triplet -> singlet-exciplex
% k.Ise = 1.5 * 10^9;                  % #ref 1#  CQ-singlet -> triplet-exciplex

%{
% k.ESform = k.Ise;                    %          Singlet exciplex formation
% k.ETform = k.Ite;                    %          Triplet exciplex formation
%}

k.Eform = k.Ite;
k.Eact = beta * k.Eform;             %          Active species formation
k.Edeact = gamma * k.Eform;          %          Deactivation
k.Elost = (1-beta-gamma) * k.Eform;  %          Degredation products

%% Inhibitor



E_inhibitor_photon       =   nA*h*c/inhibitor.nu  ;     % JK E = N_A*h*c/lambda
I_light_inhi             =   parameters.inhi_intensity; % mW / cm^2
phi_inhi                 =   1; % #NOREF# inhibitor concentration?    % G&B

IHgr                     =   inhibitor.eps_366 * phi_inhi * I_light_inhi/E_inhibitor_photon;

k.IHgr  = IHgr;    % #ref ?#  IN-ground   -> 2 IN-r
k.IHrg  = 10 / 2;  % #ref 4#  2 + IN-r    -> IN-ground;       2k  10—100 M-1*s-1

% as a guess; take the fastest propogation rate times 100 for inhibition
for i = 1:size(monomers,2)
    temp(i) = monomers(i).K.prop;
end
if max([temp]) > 0
    k.IHpol = max([temp])*100;     % #NOREF#  POLr + IN-r -> POL-IN
else
    k.IHpol = 100;
end


%% formation of polymer
% now included in the monomers themself
% to facilitate copolymerization
%{
        %{
        k.Pinit = 5;

        rate at which the initiator activates monomer
        rate at which the monomer/polymer radicals propogate
        rate                                       terminate by recombination
        rate                                       terminate by disproportination (assume new double bond is not reactive enough to reinitiate)

        %}

    k.Pinit = 2;                         % #NOREF#  Eact + V    -> POLr
    k.Pprop = 3;                         % #NOREF#  POLr + V    -> POLr + B
    k.Ptr = 1;                           % #NOREF#  POLr + POLr -> B
    k.Ptd = 1;                           % #NOREF#  POLr + POLr -> POL + POL
%}

%% oxygen

% CQ-Triplet + O2 -> CQ-OO' k = 2 * 10^8 #ref 1/3#

k.Oop = 2e8; %  #ref 1#

end

