import numpy as np


class Solver():
    def gauss(self, kgRestrito, forcasRestrito):
        """
            Resolve uma equação de matrizes usando o método de Gauss.
        """

        x = [0] * len(forcasRestrito)

        passa = True
        iteracoes = 0

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

            iteracoes += 1

        return x, iteracoes

    def jacobi(self, kgRestrito, forcasRestrito):
        """
            Resolve uma equação de matrizes usando o método de Jacobi.
        """

        xList = [0] * len(forcasRestrito)

        passa = True
        iteracoes = 0

        while passa:
            newXList = xList.copy()
            for i in range(0, len(forcasRestrito)):
                sub = 0
                for j in range(0, len(forcasRestrito)):
                    if j != i:
                        sub -= kgRestrito[i][j] * xList[j]
                newXList[i] = (forcasRestrito[i] + sub) / kgRestrito[i][i]

            dif = 0
            for i in range(len(newXList)):
                if newXList[i] != 0:
                    dif += abs((newXList[i] - xList[i]) / newXList[i])

            if dif < 1e-10:
                passa = False
                break
            else:
                x = newXList.copy()

            if iteracoes >= 2000:
                passa = False
                break

            iteracoes += 1

        return x, iteracoes
