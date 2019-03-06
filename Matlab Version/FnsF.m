function  FnsF( T,P1D,P2D ) %[ Porcentaje ] =
    Total =  length(T);
    for elemento = 1: Total
        for i = 1:length(PID)
            T(T(elemento)== P1D(i)) = 0;
        end
        for i = 1:length(P2D)
            T(T(elemento)== P2D(i)) = 0;
        end
    end
end

