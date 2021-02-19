function [species, valid_species, species_header, indexes] = create_species(monomers)
%CREATE_SPECIES Summary of this function goes here
%   Detailed explanation goes here

%% Find max dimensions for concentration matrix

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

species                   = zeros(resin_monomers, vmax +1, pmax +1, nmax +1, nmax +1, nmax +1);
temp                      = zeros(resin_monomers, vmax +1, pmax +1, nmax +1, nmax +1, nmax +1);
valid_species             = zeros(resin_monomers, vmax +1, pmax +1, nmax +1, nmax +1, nmax +1);
species_header            = strings(resin_monomers, vmax +1, pmax +1, nmax +1, nmax +1, nmax +1);
chemicallly_valid_species = zeros(resin_monomers, vmax +1, pmax +1, nmax +1, nmax +1, nmax +1); 


%% Set initial concentration

for i = 1:resin_monomers
    monomer = monomers(i);
    species(i, monomer.vmax+1, 1, 1, 1, 1) = monomer.conc;
    temp(i, monomer.vmax+1, 1, 1, 1, 1) = 1;
end

temp = reshape(temp, [], 1);
indexes.free_monomer_indexes = find(temp > 0);
clear temp

%% Create all possible species


resin_monomers = size(monomers,2);

for i = 1:resin_monomers                                  % all the monomers
    monomer = monomers(i);                                % all the species for a monomer
    for v = 1:monomer.vmax +1                             % vinyl_groups
        for p = 1:monomer.pmax +1                         % radicals
            for b_in = 1:monomer.nmax +1                  % outgoing bonds  (monomer/polymer radical attacks other monomer/polymer vinyl)
                for b_out = 1:monomer.nmax +1             % incomming bonds (monomer/polymer vinyl is attacked by other monomer/polymer radical)
                    for b_neutral = 1:monomer.nmax +1     % neutral bonds   (monomer/polymer radical termination, either disproportionation or combination)
                        b_tot = b_in-1 + b_out-1 + b_neutral-1;
                        string = [num2str(i          ), ... 1 , indexes to name of species
                                  num2str(v        -1), ... 2
                                  num2str(p        -1), ... 3
                                  num2str(b_in     -1), ... 4
                                  num2str(b_out    -1), ... 5
                                  num2str(b_neutral-1)];  % 6
                        species_header(i,v,p,b_in, b_out, b_neutral) = string;
                        %{
                        % v = 2, p = 0, b = 0 == valid
                        % v = 0, p = 2, b = 0 == valid
                        % v = 0, p = 2, b = 2 == valid
                        % v = 0, p = 0, b = 4 == valid (if monomer.nmax = 4)
                        % v = 1, p = 1, b = 1 == valid
                        % ----
                        % v = 0, p = 0, b = 0 == not valid
                        % v = 1, p = 0, 2 >= b >= 1 == valid
                        % |
                        % -> (vmax - (v-1)) - b_in == 0 
                        % -> (v-1) *2 + (p-1) - b_tot == 0
                        % v = 1, p = 1, b = 2 == not valid
                        % v = 1, p = 2, b = 0 == not valid
                        % b_in > nmax/2       == not valid
                        %#v = 0, p = 1, => b_in >= 1 && 
                        %#                 b_out < 2 && 
                        %#                 b_neutral < 2 && 
                        %#                 b_tot = at least 1 in, maybe 2, and 0 or 1 out, 1< b_tot <3
                        %}
                        if      ((v-1)*2) + (p-1) + b_tot <= monomer.nmax   && ...
                                monomer.vmax - (v-1) == (b_in -1)           && ...
                                (b_in-1) - ( (b_out-1) + (b_neutral-1) ) == (p-1)%
                           chemicallly_valid_species(i,v,p,b_in, b_out, b_neutral) = 1;        
                        else
                           chemicallly_valid_species(i,v,p,b_in, b_out, b_neutral) = 0;
                        end
                        if     (v-1) * 2 + (p-1) + b_tot <= monomer.nmax  && ...
                               (p-1)+(v-1) <= monomer.vmax                && ...
                               (b_out-1) + b_neutral-1 <= monomer.vmax    && ...
                               (b_in - 1) <= monomer.vmax                 && ...
                               (true || monomer.vmax - (v-1) <= (b_in -1))     %
                            valid_species(i,v,p,b_in, b_out, b_neutral) = 1;
                        else
                            valid_species(i,v,p,b_in, b_out, b_neutral) = 0;
                        end
                    end
                end
            end
        end
    end
end

% state_zero
% 1  = CQ-ground state, 2  = Co-Initiator, 3  = CQ-Singlet, 4  = CQ-Triplet, 5  = Exciplex, 6  = Active Initiator species, 
% 7  = Monomer activating Co-initiator species, 8  = Degredation products, 9 = Inhibitor, 10 = Inhibitor radical, 
% 11 = vinyl groups, 12 = Polymer radicals, 13 = bonds, 14 = Oxygen, 15 = Peroxide, 16 = Reduced Co-Initiator

species        = reshape(species        ,[],1);
valid_species  = reshape(valid_species  ,[],1);
species_header = reshape(species_header ,[],1);

temp = cell2mat( convertStringsToChars ( species_header ) );
indexes.vinyl_indexes = find(temp(:,2) ~= '0');
indexes.radical_indexes = find(temp(:,3) ~= '0');

%% Notes
%{
        if (p-1) == 1 && (v-1) == 0 && ... 2 & 1 for non zero_index
                    (b_in-1)     == 0 && ... if the pol-/monomer has a radical but no in_bond
                    (b_out-1)     > 1 && ... if the pol-/monomer has a radical and more than 1 outgoing bond
                    (b_neutral-1) > 1 && ... if the pol-/monomer has a radical and more than 1 termination
                    (b_tot-1)<1 && (v_tot-1)<3
            valid_species(i,v,p,b_in, b_out, b_neutral) = -1;  
        else





    if (v-1) * 2 + (p-1) + b_tot <= monomer.nmax   && ...       % there is maximum number of 'attributes' a monomer can have
                    (v-1) + (p-1) <= monomer.vmax   && ...       % the monomer can have no more then 2 vinyl or radicals combined
                        (b_in-1) <= monomer.nmax/2 && ...       % the monomer can have no more then 2 incomming bonds, since an incomming bond places a radical there that can either form an outgoing bond or be lost through termination
                        (b_out-1) <= monomer.nmax/2 && ...       % the monomer can have no more then 2 outgoing bonds, since the vinyl group can produce only 1 attacking radical !!!!
                            b_in >= b_out          && ...
        (p-1) + (b_out -1) + (b_neutral -1) <= monomer.pmax      % the sum of p, b_out, and b_neutral should <= 




%}

end