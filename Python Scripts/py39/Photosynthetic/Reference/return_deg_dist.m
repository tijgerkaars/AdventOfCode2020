function [degree, degree_header,typed_degree, typed_degree_header] = return_deg_dist(t,y,monomers)
%RETURN_DEG_DIST Summary of this function goes here
%   Detailed explanation goes here


size(t);
size(y);


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

% species_conc= zeros(resin_monomers, vmax +1, pmax +1, nmax+1, nmax +1, nmax +1);
species_conc = reshape(y, size(t,1), resin_monomers, vmax +1, pmax +1, nmax+1, nmax +1, nmax +1);
%%
degree = zeros(size(t,1), 3 * (nmax+1));
degree_header = strings(1, 3 * (nmax+1));

% gives names matching the degree distribution
for b = 1 : 3* (nmax+1)
    degree_header(b) = strcat(num2str(b-1), ' bonds');
end
%%
% contains the typed bonds (in,out,neutral) over time
typed_degree        = zeros(size(t,1), nmax +1, nmax +1, nmax +1);
typed_degree_header = strings(nmax +1, nmax +1, nmax +1);

% gives names matching the degree distribution
for bi = 1: nmax +1
    for bo = 1: nmax +1
        for bn = 1: nmax +1
            typed_degree_header(bi,bo,bn) = [num2str(bi-1), num2str(bo-1), num2str(bn-1)];
        end
    end
end
%%


for i = 1:resin_monomers                                           % all the monomers
    monomer = monomers(i);                                         % all the species for a monomer
    for v = 1:monomer.vmax +1                                      % vinyl_groups
        for p = 1:monomer.pmax +1                                  % radicals
            for b_in = 1:monomer.nmax +1                           % outgoing bonds  (monomer/polymer radical attacks other monomer/polymer vinyl)
                for b_out = 1:monomer.nmax +1                      % incomming bonds (monomer/polymer vinyl is attacked by other monomer/polymer radical)
                    for b_neutral = 1:monomer.nmax +1              % neutral bonds   (monomer/polymer radical termination, either disproportionation or combination)
                        b_tot = b_in-1 + b_out-1 + b_neutral-1;
                        degree(:, b_tot+1) = degree(:, b_tot+1) + species_conc(:,i,v,p,b_in,b_out,b_neutral);
                        typed_degree(:,b_in, b_out, b_neutral) = typed_degree(:,b_in, b_out, b_neutral) + reshape(species_conc(:,i,v,p,b_in,b_out,b_neutral),size(t,1),1,1);
                    end
                end
            end
        end
    end
end


[y_,~] = size(degree);
max_bonds = zeros(size(degree,1),1);

for i = 1:y_
    for b = 1:size(degree(i,:),2)
        max_bonds(i) = max_bonds(i) + (b-1) * degree(i, b);
    end
end

% the conversion?
degree_ = degree;
for i = 1:y_
    degree_(i,:) = degree(i,:)/ (2 * extract_field_summed(monomers, "conc") * extract_field_summed(monomers, "vmax")');
end



%  extract_field_summed(monomers, "conc") * extract_field_summed(monomers, "vmax")' 


end