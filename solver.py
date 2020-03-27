import numpy as np


class Solver():
    def gauss(self, kgRestrito, forcasRestrito):
        """
            Resolve uma equação de matrizes usando o método de Gauss. 
        """

        x = [0] * len(forcasRestrito)

        passa = True
        interacoes = 0

        while passa:
            for i in range(0, len(forcasRestrito)):
                sub = 0
                for j in range(0, len(forcasRestrito)):
                    if j != i:
                        sub -= kgRestrito[i][j] * x[j]
                new_x = (forcasRestrito[i] + sub) / kgRestrito[i][i]

                if new_x != 0:
                    if abs((new_x - x[i]) / new_x) < 1e-10:
                        passa = False
                        break

                    x[i] = new_x

            interacoes += 1

        return x, interacoes
