clc 
clear all
[~,SheetNames]  = xlsfinfo('Tortuosidad_de_Elementos.xlsx')
nSheets = length(SheetNames);
 for i = 1:nSheets
    Name = SheetNames{i}; 
    Datos = xlsread('Tortuosidad_de_Elementos.xlsx',i);
    [y1,x1] = hist(Datos(:,3),0:0.005:10);
    indices = find(x1(1,:) <= 3);
    x1 = x1(:,indices);
    y1 = y1(:,indices);
    indices = find(x1(1,:) >= 1);
    ValoresX = x1(:,indices);
    ValoresY = y1(:,indices);
    indices = find(ValoresY(1,:) >= 1);
    ValoresX = ValoresX(:,indices);
    ValoresY = ValoresY(:,indices);
%     figure(i)
%     subplot(3,1,1)
%     plot(ValoresX,ValoresY*100/sum(ValoresY))
%     subplot(3,1,2)
%     plot(ValoresX,smooth((ValoresY*100/sum(ValoresY))))
%     subplot(3,1,3)
%     bar(ValoresX,ValoresY*100/sum(ValoresY))
    xlswrite('Tortuosidad_de_Elementos_Acumulativa.xlsx',[ValoresX',ValoresY'.*100/sum(ValoresY)],i);
 end