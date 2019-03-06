clc
clear all
archivos = dir('*.tif');
for i = 1 : size(archivos)
    Nombre = archivos(i).name;
    [V,MpData,Cte,NCE] = AnalisisTortuosidad(Nombre);
    xlswrite('Tortuosidad_de_Elementos.xlsx',V,i);
    Info = xlsread('Tortuosidad_de_Elementos.xlsx', i, 'A:A');
    Info = find(Info ~= 0 );
    MpData = MpData(Info);
    Verticales = find(([MpData.Orientation] >= 45)|([MpData.Orientation] <= -45));
    Horizontales = find(([MpData.Orientation] < 45)&([MpData.Orientation] > -45));
    BandVer = 0;
    BandHor = 0;
    if not(isempty(Verticales))
        [D1,Num1] = DistanciaEntreFringes(Verticales, MpData,Cte,"Vertical");
    else
        D1 = [0];
        BandVer = 1; 
    end
    if not(isempty(Horizontales))
       [D2,Num2] = DistanciaEntreFringes(Horizontales, MpData,Cte,"Horizontal");
    else
        D2 = [0];
        BandHor = 1;
    end
    
    if ((BandVer == 0) && (BandHor == 0))
        DistanciasInterplanaresValidas = FiltroFringes(D1,D2,1);
    end
    if ((BandVer == 0) && (BandHor == 1))
        DistanciasInterplanaresValidas = FiltroFringes(D1,D2,2);
    end
    if ((BandVer == 1) && (BandHor == 0))
        DistanciasInterplanaresValidas = FiltroFringes(D1,D2,3);
    end
    xlswrite('DistanciasInterplanares.xlsx',DistanciasInterplanaresValidas,i);
%     FnsF(NCE,DistanciasInterplanaresValidas(:,1),DistanciasInterplanaresValidas(:,2));
end