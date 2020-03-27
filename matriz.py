import numpy as np
from math import sqrt

def matriz_elemento(x_inicio, x_fim, y_inicio, y_fim, E, A):
    L = sqrt((x_fim - x_inicio)**2 + (y_fim - y_inicio)**2)

    sen = (y_fim - y_inicio) / L
    cos = (x_fim - x_inicio) / L

    matriz = np.array([
        [cos**2, cos*sen, -cos**2, -cos*sen],
        [cos*sen, sen**2, -cos*sen, -sen**2],
        [- cos**2, - cos*sen, cos**2, cos*sen],
        [- cos*sen, - sen **2, cos*sen, sen**2]
    ])
    
    return np.multiply(E * A / L, matriz)

def matriz_restricoes(ke, vetor_forcas, vetor_restricoes):
    list(vetor_restricoes).reverse()

    vetor_forcas = np.delete(vetor_forcas, vetor_restricoes, 0)

    ke = np.delete(ke, vetor_restricoes, 0)
    ke = np.delete(ke, vetor_restricoes, 1)

    return ke, vetor_forcas
