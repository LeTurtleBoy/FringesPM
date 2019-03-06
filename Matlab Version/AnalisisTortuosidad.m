function [Valores, MPdata,Cte,NonCEle] = AnalisisTortuosidad(imagen)
    Imagen = imread(imagen);
    imbin = imbinarize(Imagen,0.5);
    %------------------------------------------
    Improcesar = not(imbin);
    a = strfind( imagen , "450kx" );% []
    b = strfind( imagen , "590kx" );% 11
    c = strfind( imagen , "690kx" );% []
    
    M450kx = isempty(b) && isempty(c); % 1 && 0 = 0
    M590kx = isempty(a) && isempty(c); % 1 && 1 = 1 
    M690kx = isempty(a) && isempty(b); % 1 && 0 = 0
   
    if M690kx == 1
       Elementosdeinteres = bwareaopen(Improcesar, 22); % En el peor de los casos se tiene diagonal perfecta 21.41
       Cte = 62.7;
    end
    if M590kx == 1
        Elementosdeinteres = bwareaopen(Improcesar, 19); % En el peor de los casos se tiene diagonal perfecta 18.31
        Cte = 53.6;
    end
    if M450kx == 1
       Elementosdeinteres = bwareaopen(Improcesar, 14); % En el peor de los casos se tiene diagonal perfecta 13.93 
       Cte = 40.8;
    end
    L=bwlabel(Elementosdeinteres);
    MPdata = regionprops(Elementosdeinteres,'all');
    Valores = zeros(length(MPdata),3);
    C = 0;
    for K = 1:length(MPdata)
        %%%%%%%%%%%%%%%%%%%%%%%
        %     Tortuosidad     %
        %%%%%%%%%%%%%%%%%%%%%%%
        I = MPdata(K).Image;
        S = size(I);
        base = zeros(S(1)+2,S(2)+2);
        for i = 1:S(1)
            for j = 1:S(2)
                base(i+1,j+1) = I(i,j);
            end
        end
        S = size(base);
        NumPix = 0;
        V=zeros(S(1),S(2));
        for i = 1:S(1)
            for j = 1:S(2)
                Pij = base(i,j);
                if (Pij == 1)
                    V(i,j) = base(i-1,j-1) + base(i-1,j) + base(i-1,j+1) + base(i,j-1) + base(i+1,j-1) + base(i+1,j) + base(i+1,j+1) + base(i,j+1);
                    NumPix = NumPix + 1;
                end
            end
        end
        [Alpha,Omega] = find(V==1);
        Arriba = 0;
        ArribaDerecha = 0;
        Derecha = 0;
        AbajoDerecha = 0;
        Abajo = 0;
        AbajoIzquierda = 0;
        Izquierda = 0;
        ArribaIzquierda = 0;
        CoordActual = [0,0];
        if length(Alpha) == 2
            L = Distancia_Pitagorica(Alpha(1),Alpha(2),Omega(1),Omega(2));
            CoordInicio = [Alpha(1),Omega(1)];
            It = 1;
            while (NumPix >= 0 )
                if It == 1
                    CoordActual = CoordInicio;
                    NumPix = NumPix-1;
                    C = 0;
                    It = It+1;
                else
                    y = CoordActual(1);
                    x = CoordActual(2);
                    Arriba = base(y-1,x);
                    ArribaDerecha = base(y-1,x+1);
                    Derecha = base(y,x+1);
                    AbajoDerecha = base(y+1,x+1);
                    Abajo = base(y+1,x);
                    AbajoIzquierda = base(y+1,x-1);
                    Izquierda = base(y,x-1);
                    ArribaIzquierda = base(y-1,x-1);
                    if Abajo == 1 
                        C = C + 1;
                        base(y,x) = 0;
                        CoordActual = [y+1,x];
                    elseif Derecha == 1
                        C = C + 1;
                        base(y,x) = 0;
                        CoordActual = [y,x+1]; 
                    elseif Izquierda == 1 
                        C = C + 1;
                        base(y,x) = 0;
                        CoordActual = [y,x-1];
                    elseif Arriba == 1 
                        C = C + 1;
                        base(y,x) = 0;
                        CoordActual = [y-1,x] ;
                    elseif AbajoDerecha == 1
                        C = C + sqrt(2);
                        base(y,x) = 0;
                        CoordActual = [y+1,x+1];
                    elseif AbajoIzquierda == 1
                        C = C + sqrt(2);
                        base(y,x) = 0;
                        CoordActual = [y+1,x-1];
                    elseif ArribaDerecha == 1
                        C = C + sqrt(2);
                        base(y,x) = 0;
                        CoordActual = [y-1,x+1];
                    elseif ArribaIzquierda == 1
                        C = C + sqrt(2);
                        base(y,x) = 0;
                        CoordActual = [y-1,x-1];
                    end
                end
                    NumPix = NumPix-1;
            end
            Valores(K,:) = [C/Cte,L/Cte,C/L];
            if Valores(K,1) < 0.483
              Valores(K,:) = [0,0,0];
            end
            if Valores(K,3) > 2
              Valores(K,:) = [0,0,0];
            end
            if Valores(K,3) < 1
              Valores(K,:) = [0,0,0];
            end
        end
    end
    NonCEle = find(Valores(:,1) ~= 0);
end