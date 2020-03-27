import numpy as np

# Gauss
def solver_gauss(Kg, F):

    x = [0]*len(F)

    passa = True
    interacoes = 0

    while passa:

        for i in range(0, len(F)):
            sub = 0
            for j in range(0, len(F)):
                if j != i:
                    sub -= Kg[i][j]*x[j]
            new_x = (F[i] + sub)/Kg[i][i]

            if new_x != 0:
                dif = abs((new_x - x[i])/new_x)

                if dif < 1e-10: 
                    passa = False
                    break
                
                x[i] = new_x
        interacoes += 1

    return x, interacoes

# ------------------------------------------------------ #

# Jacobi
def solver_jacobi(Kg, F):

    x = [0]*len(F)

    passa = True
    interacoes = 0

    while passa:

        new_x = x.copy()

        for i in range(0, len(F)):
            sub = 0
            for j in range(0, len(F)):
                if j != i:
                    sub -= Kg[i][j]*x[j]
            new_value = (F[i] + sub)/Kg[i][i]
            new_x[i] = new_value
        
        dif = 0
        for i in range(len(new_x)):
            if new_x[i] != 0:
                dif += abs((new_x[i] - x[i])/new_x[i])

        if dif < 1e-10: 
            passa = False
            break

        x = new_x.copy()
        interacoes += 1

    return x, interacoes