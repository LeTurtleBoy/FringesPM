
function [Distancias, NumeroElementos] =  DistanciaEntreFringes (Elementos, Data, Cte,Ori)
NumeroElementos = length(Elementos);
K = 0;
K2 = 0;
PetitSolution = [6,6,6];
for i=1:NumeroElementos
    Distanci = PetitSolution;
    Elemento_principal = Data(Elementos(i));
    flag = 0;
    K = 0;
    for j = (i+1):NumeroElementos
        Elemento_Actual = Data(Elementos(j));
        %Buscamos el mas pequenho
        if Elemento_principal.Area <= Elemento_Actual.Area
            E1 = Elemento_principal;
            E2 = Elemento_Actual;
        else
            E2 = Elemento_principal;
            E1 = Elemento_Actual;
        end
        
        %Ahora vamos a ver cuales tienen mismas Filas o Columnas
        if i == 190
            if j == 193
                i
            end
        end
        if Ori == "Horizontal"
            for pix=1:length(E1.PixelList)          % para cada pixel en el mas pequeno
                for Corresp =1:length(E2.PixelList)  % en cada pixel del mas grande
                    Cond1 = E1.PixelList(pix,:);    % tomo el valor del pixel
                    Cond2 = E2.PixelList(Corresp,:);% tomo el valor del pixel
                    if Cond1(1) ==  Cond2(1)
                        K = K+1;
                        flag = 1;
                        Disprevia(K,:) = [i,j,Cond1,Cond2]; % (x1,y1,x2,y2)
                        
                    end
                end
                
            end
        else %Es Vertical
            for pix=1:length(E1.PixelList)          % para cada pixel en el mas pequeno
                for Corresp =1:length(E2.PixelList)  % en cada pixel del mas grande
                    Cond1 = E1.PixelList(pix,:);    % tomo el valor del pixel
                    Cond2 = E2.PixelList(Corresp,:);% tomo el valor del pixel
                    if Cond1(2) ==  Cond2(2)
                        K = K+1;
                        flag = 1;
                        Disprevia(K,:) = [i,j,Cond1,Cond2]; % (Imagen1, Imagen2 x1,y1,x2,y2)
                    end
                end
                 
            end
        end
        
        
    end
    if flag  == 1
            flag = 0;
            K2 = K2+1;
            aux = size(Disprevia);
            Dreporte(:,:) = FDIF(Disprevia);
            PetitSolution = [PetitSolution;Dreporte];
            clear Dreporte Disprevia
        end
end
[m,n] = size(PetitSolution);
for i = 2:m %Termino la estructura con ID de los elementos involucrados y la distancia entre ellos
    Distancias(i-1,:) = [Elementos(PetitSolution(i,2)),Elementos(PetitSolution(i,3)),PetitSolution(i,1)/Cte];
end
end