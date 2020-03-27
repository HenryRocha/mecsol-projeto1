import numpy as np
from math import sqrt


class Element():
    def __init__(self, node1, node2, E, A, index):
        """
            Esse função é executada na criação do objeto elemento.
            Server paara guardar todas as informações de um elemento,
            além de calcular sua matriz.

            @param node1 nó 1 do elemento
            @param node2 nó 2 do elemento
            @param E E[Pa]
            @param A A[m2]
            @param index index do elemento
        """
        self.node1 = node1
        self.node2 = node2
        self.E = E
        self.A = A
        self.index = index

        # Criando uma lista de números dos graus de liberdade
        # desse elemento.
        self.degrees = [self.node1.gdlX, self.node1.gdlY,
                        self.node2.gdlX, self.node2.gdlY]

        # Calculando o comprimento do elemento.
        self.L = sqrt((self.node2.x - self.node1.x)**2 +
                      (self.node2.y - self.node1.y)**2)

        # Calculando o seno e o coseno do elemento.
        self.s = (self.node2.y - self.node1.y) / self.L
        self.c = (self.node2.x - self.node1.x) / self.L

        # Criando a matriz M, usada para calcular a deformação,
        # força e tensão.
        self.m = np.array([- self.c, - self.s, self.c, self.s], float)

        # Criando a matrix Ke.
        self.calculateKe()

    def calculateKe(self):
        """
            Cria a matriz Ke do elemento.
        """
        self.k = np.array([
            [self.c**2, self.c*self.s, -self.c**2, -self.c*self.s],
            [self.c*self.s, self.s**2, -self.c*self.s, -self.s**2],
            [- self.c**2, - self.c*self.s, self.c**2, self.c*self.s],
            [- self.c*self.s, - self.s ** 2, self.c*self.s, self.s**2]
        ])

        self.ke = np.multiply(self.E * self.A / self.L, self.k)

    def __str__(self):
        """
            Essa função é chamada quando se tenta printar
            um objeto elemento.
        """

        out = f"Número: {self.index}\n"
        out += f"No 1:\n{self.node1}\n"
        out += f"No 2:\n{self.node2}\n"
        out += f"E: {self.E}\n"
        out += f"A: {self.A}\n"
        out += f"Ke:\n{self.ke}\n"
        return out
