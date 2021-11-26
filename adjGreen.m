% Makes each position in G-matrix a multiple of k
function [aG] = adjGreen (XG, k)
[m, n] = size(XG);
aG = zeros(m, n);
for i = 1:m
    for j = 1:n
        rest = mod(XG(i,j),k);
        if rest >= k/2
            aG(i,j) = XG(i,j) - rest + k;
        else
            aG(i,j) = XG(i,j) - rest;
        end
    end
end