function Sol = FDIF(Vector)
    clear Sol
    AUX1 = 1;
    pos = 0;
    Limit = size(Vector);
    flag = 0;
    for i = 1:Limit(1)
        if  i > 1
            a = Vector(i,2);
            b = Vector(i-1,2);
            if  a~=b
                pos(AUX1) = i;
                AUX1 = AUX1 + 1;
            end
        else
            pos = 1;
        end
        ind = 0;
        for j = 1:Limit(1)
            if Vector(i,2) == Vector(j,2)
                ind = ind + 1;
                X1 = Vector(i,3);
                X2 = Vector(j,5);
                Y1 = Vector(i,4);
                Y2 = Vector(j,6);
                a(ind) = Distancia_Pitagorica(X1,X2,Y1,Y2);
                flag = 1;
            end
        end
        ind = 0;
        DisR(i) = min(a);
    end
    if flag ~= 0
        sol = zeros(AUX1,3);
        Limites = zeros(AUX1+1,1);
        if pos == 1
            Limites = [1,Limit(1)];
        else
            auxirefoquinliar = [1;pos(:);Limit(1)];
            Limites = auxirefoquinliar';
        end
        %Limit(1)
        for x = 1:(length(Limites)-1)
            La = Limites(x);
            Lb = Limites(x+1);
            Data2Mean = DisR(La:Lb);
            Sol(x,:) = [mean(Data2Mean),Vector(La,1),Vector(La,2)];
        end
    end   
end