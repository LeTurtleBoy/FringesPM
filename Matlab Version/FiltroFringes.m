function [Valores] = FiltroFringes(D1,D2,Banderita)
    if Banderita == 1
        Distancias = [D1;D2];
        indices = find(Distancias(:,3) < 0.6);
        Valores = Distancias(indices,:);
        indices = find(Valores(:,3) > 0.3354);
        Valores = Valores(indices,:);
    end
    if Banderita == 2
        Distancias = [D1];
        indices = find(Distancias(:,3) < 0.6);
        Valores = Distancias(indices,:);
        indices = find(Valores(:,3) > 0.3354);
        Valores = Valores(indices,:);
    end
    if Banderita == 3
        Distancias = [D2];
        indices = find(Distancias(:,3) < 0.6);
        Valores = Distancias(indices,:);
        indices = find(Valores(:,3) > 0.3354);
        Valores = Valores(indices,:);
    end
end

