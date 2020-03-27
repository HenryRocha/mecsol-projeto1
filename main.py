from funcoesTermosol import importa, geraSaida
from matriz import matriz_restricoes, matriz_elemento
import numpy as np
from solver import solver_gauss

numero_nos, matriz_nos, numero_elementos, matriz_conexoes, numero_forcas, vetor_forcas, numero_restricoes, vetor_restricoes = importa('entrada.xlsx')

ke = np.zeros((numero_nos*2, numero_nos*2))

for conexoes in matriz_conexoes:
    no_1 = int(conexoes[0]) - 1
    grau_0 = no_1*2
    grau_1 = no_1*2 + 1
    
    no_2 = int(conexoes[1]) - 1
    grau_2 = no_2*2
    grau_3 = no_2*2 + 1
    
    x_inicio = matriz_nos[0][no_1]
    y_inicio = matriz_nos[1][no_1]
    
    x_fim = matriz_nos[0][no_2]
    y_fim = matriz_nos[1][no_2]
    
    E = conexoes[2]
    A = conexoes[3]

    matriz = matriz_elemento(x_inicio, x_fim, y_inicio, y_fim, E, A)
    ke[grau_0:grau_0+2, grau_0:grau_0+2] += matriz[:2, :2]
    ke[grau_0:grau_0+2, grau_2:grau_2+2] += matriz[2:, :2]
    ke[grau_2:grau_2+2, grau_0:grau_0+2] += matriz[:2, 2:]
    ke[grau_2:grau_2+2, grau_2:grau_2+2] += matriz[2:, 2:]

kg, vetor_forcas_restrito = matriz_restricoes(ke, vetor_forcas, vetor_restricoes)

vetor_deslocamento, _ = solver_gauss(kg, vetor_forcas_restrito)
deslocamento_full = vetor_deslocamento.copy()

for i in vetor_restricoes:
    deslocamento_full.insert(int(i), 0)

reacoes_apoio = np.array(ke).dot(np.array(deslocamento_full))

delete_indexes = []
for i in range(len(reacoes_apoio)):
    if i not in vetor_restricoes:
        delete_indexes.append(i)

reacoes_apoio = np.delete(reacoes_apoio, delete_indexes, 0)

geraSaida("grupo414", reacoes_apoio, vetor_deslocamento, deformacoes, forcas_internas, tensoes_internas)