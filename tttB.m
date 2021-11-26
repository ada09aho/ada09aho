timerVal=tic;
pcu=4.0;
d=1.5;
vpm=1/(d*pcu); % vehicles per meter (vpm=1/6 as initial value)
% Start and stop of gren phases as percentage of real sampled time value
percBase = 50; percTop = 150;
% Iteration range
start = 31; step = -3; stop = 1;
% Variable for calculation and display purposes
roof = (max(start, stop)-1)/abs(step) + 1;
% Lowest deviation value / Highest index in LIST
least = 1; last = 200;
% Table with values of deviation and indices of X, i.e. each green phase
LIST = zeros(last, 8);
% Initial inbound distance for each intersection, di
di=200;

% D is a vector with distance to/from neighbour TLI (S).
D1=[470; 890; 570; 395]; 
D3=[520; 670; 630; 890];
D5=[530; 0; 760; 670];
D6=[570; 915; 735; 230];
D9=[630; 690; 725; 915];
D11=[760; 305; 670; 690];
% Deduction of intermediate TLI (50 m) and pedestrian crossings (12 m)
D1=D1-[0; 50; 0; 0];
D3=D3-[0; 12; 12; 50];
D5=D5-[0; 0; 0; 12];
D6=D6-[0; 12+50+50; 0; 0];
D9=D9-[12; 50; 0; 12+50+50];
D11=D11-[0; 0; 0; 50];
D=[D1 D3 D5 D6 D9 D11];

% DI is a vector with initializing distance di to/from neighbour TLI (S).
DI1=di*[1; 1; 1; 1];
DI3=di*[1; 1; 1; 1];
DI5=di*[1; 0; 1; 1];
DI6=di*[1; 1; 1; 1];
DI9=di*[1; 1; 1; 1];
DI11=di*[1; 1; 1; 1];
DI=[DI1 DI3 DI5 DI6 DI9 DI11];

% L is a vector with the number of lanes inbound from neighbour TLI.
L1=[2; 3; 3; 3];
L3=[3; 3; 2; 2];
L5=[3; 0; 3; 3];
L6=[2; 3; 4; 3];
L9=[2; 3; 2; 3];
L11=[4; 2; 3; 3];
L=[L1 L3 L5 L6 L9 L11];

% C is a "mass"-vector with vehicles going into each intersection.
C1=vpm*(D1.*L1);
C3=vpm*(D3.*L3);
C5=vpm*(D5.*L5); C5(2)=1; % To avoid later division by zero.
C6=vpm*(D6.*L6);
C9=vpm*(D9.*L9);
C11=vpm*(D11.*L11);
C=[C1 C3 C5 C6 C9 C11];

% CI is an initial "mass"-vector with vehicles going into each intersection.
CI1=vpm*(DI1.*L1);
CI3=vpm*(DI3.*L3);
CI5=vpm*(DI5.*L5); CI5(2)=1; % To avoid later division by zero.
CI6=vpm*(DI6.*L6);
CI9=vpm*(DI9.*L9);
CI11=vpm*(DI11.*L11);
CI=[CI1 CI3 CI5 CI6 CI9 CI11];

% P is a matrix with directional ratio relative to inbound number of lanes.
P1=[0 1/6 2/5 3/10; 3/7 0 1/5 5/10; 5/14 2/6 0 1/10; 3/14 3/6 2/5 1/10];
P3=[0 0 2/5 1/10; 1/6 1/10 1/5 3/5; 3/6 3/10 1/10 1/5; 2/6 3/5 3/10 1/10];
P5=[0 0 3/4 9/8; 0 0 0 0; 5/8 0 1/8 1/4; 3/8 0 1/8 1/8];
P6=[1/10 1/5 5/8 2/5; 3/10 1/10 1/8 2/5; 2/5 3/10 0 1/5; 1/5 2/5 1/4 0];
P9=[0 1/5 1/3 2/5; 1/3 0 1/3 2/5; 3/6 2/5 0 1/5; 1/6 2/5 1/3 0];
P11=[0 1/3 3/5 1/4; 3/8 0 1/5 3/4; 5/8 1/6 0 0; 0 3/6 1/5 0];
P=[P1 P3 P5 P6 P9 P11];

% G is the green light time (incl 3 s of yellow) in each direction per TLI
G1=[0 78 39 45; 36 0 66 54; 39 36 0 75; 90 42 36 45];
G3=[0 0 51 39; 39 39 93 60; 51 39 39 93; 93 60 39 39];
G5=[0 0 81 45; 0 0 0 0; 81 0 51 45; 45 0 51 45];
G6=[45 102 42 30; 45 30 42 42; 42 30 0 102; 102 42 45 0];
G9=[0 57 75 33; 24 0 75 42; 75 33 0 57; 75 42 24 0];
G11=[0 45 45 45; 45 0 45 45; 45 45 0 0; 0 45 45 0];
G=[G1 G3 G5 G6 G9 G11];

% i is a 4-bit truth table, i.e. a 16x4 digital matrix, multiplied by ...
i=((percTop-percBase)/200)*[0 0 0 0; 0 0 0 1; 0 0 1 0; 0 0 1 1; 0 1 0 0; 0 1 0 1; 0 1 1 0; 0 1 1 1;
    1 0 0 0; 1 0 0 1; 1 0 1 0; 1 0 1 1; 1 1 0 0; 1 1 0 1; 1 1 1 0; 1 1 1 1];
% K contains all possible combinations in one TLI, given the 4 phases below.
K=zeros(31,4); % To avoid repetitive values the original K(16) are reduced below
K(1:16,:)=(percBase/100)*ones(16,4)+i;
K(16:31,:)=(((percTop-percBase)/2+percBase)/100)*ones(16,4)+i;
% A case is 1 of 4 green light phases. There are more phases IRL.
case1=[0 0 1 0; 0 0 1 0; 1 0 0 0; 1 0 0 0];
case2=[1 0 0 0; 1 0 0 0; 0 0 1 0; 0 0 1 0];
case3=[0 1 0 0; 0 0 0 1; 0 0 0 1; 0 1 0 0];
case4=[0 0 0 1; 0 1 0 0; 0 1 0 0; 0 0 0 1];
% X contains all various G as X=[G(:,:), i(m)*cases, TLI(s)]
X=zeros(4,4,31,6);
% S contains the calculated cycle time of every TLI and actual case as of i
S=zeros(31,6);
% X(in,out,scenario,TLI) contains all scenarios for all TLIs. It's based on
% 4 cases. All combinations of cases decide every cycle time, S. To avoid
% car crashes, too long right turns are adjusted before saving to X.
for m=1:31 % number of scenarios
    for s=0:5 % number of TLIs
        Gs=G(:,s*4+1:s*4+4); % selection of G
        x=Gs.*(K(m,1)*case1+K(m,2)*case2+K(m,3)*case3+K(m,4)*case4);
        tempS = max(x(3,1),x(1,3))+max(x(2,1),x(4,3))+max(x(4,2),x(2,4))+max(x(3,2),x(1,4));
        S(m,s+1)= tempS;
        corrR = tempS - [x(1,3); x(2,4); x(3,1); x(4,2)];
        x(1,2) = min( x(1,2), corrR(1) );
        x(2,3) = min( x(2,3), corrR(2) );
        x(3,4) = min( x(3,4), corrR(3) );
        x(4,1) = min( x(4,1), corrR(4) );
        X(:,:,m,s+1) = x;
    end
end

plotIndex=0;
avgSum=0;
varSum=0;
index = 1; % of LIST
updates = 1; % LIST updates
s2Round = roof^4;
plotRound = roof^3;
LOWAVG = zeros(10,8);
lowestAvg = 0.996;
avgIndex = 1;
PLOTLIST=zeros(plotRound,2);
disp(['This run starts at ', num2str(K(start,1)*100), ' % and ends at ', num2str(K(stop,4)*100), ' % of the measured phasetimes.']);
for s1 = start:step:stop
    for s2 = start:step:stop
        tic
        for s3 = start:step:stop
            for s4 = start:step:stop
                for s5 = start:step:stop
                    for s6 = start:step:stop
                        Z = [s1, s2, s3, s4, s5, s6];
                        [var, avg] = variation(X, Z, S, P, CI, C);
                        avgSum = avgSum + avg;
                        varSum = varSum + var;
                        if avg < lowestAvg
                            row = mod(avgIndex,10)+1;
                            LOWAVG(row,:) = [avg Z avgIndex];
                            disp(['E(X) = ', num2str(avg), ' at Z = [ ', num2str(Z), ' ].']);
                            lowestAvg = avg;
                            avgIndex = avgIndex + 1;
                        end
                        if var < least && avg < 1
                            dev = sqrt(var);
                            if index < last
                                LIST(index,:) = [dev Z plotIndex];
                                least = var;
                                index = index + 1;
                            else
                                LIST(last,:) = [dev Z plotIndex];
                                least = var;
                                sortrows(LIST);
                            end
                            disp(['Update: ', num2str(updates),'. E(X) = ',num2str(avg),', d(X) = ', num2str(dev), '. Z = [ ', num2str(Z), ' ].']);
                            updates = updates + 1;
                        end
                    end
                end
            end
            plotIndex = plotIndex + 1;
            PLOTLIST(plotIndex,1) = sqrt(varSum / plotRound);
            PLOTLIST(plotIndex,2) = avgSum / plotRound;
            avgSum = 0;
            varSum = 0;
        end
        disp(['This round with s1/s2 = ', num2str(s1), '/', num2str(s2), ' and ', num2str(s2Round), ' comparisons took: ', num2str(toc), ' s. E(X) = ', num2str(PLOTLIST(plotIndex,2)), ', d(X) = ', num2str(PLOTLIST(plotIndex,1))]);
    end
end

TOP5DEV = sortrows(LIST(find(LIST(:,1)),:));
disp(TOP5DEV(1:5,:))
TOP5AVG = sortrows(LOWAVG(find(LOWAVG(:,1)),:));
disp(TOP5AVG(1:5,:));
toc(timerVal)

plot (LIST(:,8),LIST(:,1),'b');