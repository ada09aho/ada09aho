function [varX, avgX] = variation (X, Z, S, P, CI, C)
% Computation of variation as of how many vehicles that are either a
% decrease or an increase of the amount of cars of each street within the system.
% In: X is the green phase time of every TLI. S holds cycle times.
% Z has the particular index for each TLI-composition in X.
% Out: varX is the variation of the average evacuation of street cars. 

TFO = zeros(4,6);
TFI = zeros(4,6);
for i=0:5
    R(:,i*4+1:i*4+4) = X(:,:,Z(i+1),i+1) / S(Z(i+1), i+1); % creates green phase ratio of full cycle
    PR(:,i*4+1:i*4+4) = P(:,i*4+1:i*4+4) .* R(:,i*4+1:i*4+4); % total probability for each direction
    TFO(:,i+1) = PR(:,i*4+1:i*4+4) * CI(:,i+1); % number of pcu's going out of TLI
    TFI(:,i+1) = sum(PR(:,i*4+1:i*4+4))' .* CI(:,i+1); % number of pcu's going into TLI (out of streets)
end

% SC is a digital control matrix to decide which streets belong to system.
SC=[0 0 0 1 1 1;
    1 1 0 1 1 0;
    1 1 1 0 0 0;
    0 1 1 0 1 1];

% TFS is a rearranged TFO (onto streets) in order to fit subtraction with TFI
TFS =   [0 0 0 TFO(3) TFO(6) TFO(11);
        TFO(8) TFO(12) 0 TFO(20) TFO(24) 0;
        TFO(13) TFO(17) TFO(21) 0 0 0;
        0 TFO(2) TFO(6) 0 TFO(14) TFO(18)];

DIFF = (TFS - TFI) .* SC;
EVA = ((C + DIFF) ./ C) .* SC; % EVAcuation of streets respectively

E = find(EVA); % finds indices of all nonzero elements
WS = EVA(E); % column vector with nonzero values of EVA
avgX = mean(WS); % mean value of WS
varX = mean((WS-avgX).^2); % Variance of WS

return
end
