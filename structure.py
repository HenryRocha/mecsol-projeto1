import numpy as np
from math import sqrt
from funcoesTermosol import importa, geraSaida
from element import Element
from solver import Solver
from node import Node


class Structure():
    def __init__(self, filename, outputFilename="grupo14.txt", debug=False):
        # Salvando o nome do arquivo.
        self.filename = filename

        # Salvando o nome do arquivo de saída.
        self.outputFilename = outputFilename

        # Se o modo debug está ativado ou não.
        self.debug = debug

        # Pegando todas as informações da entrada.
        self.numero_nos, self.matriz_nos, self.numero_elementos, self.matriz_conexoes, self.numero_forcas, self.vetor_forcas, self.numero_restricoes, self.vetor_restricoes = importa(
            self.filename)

        # Transformando todas as matrizes de entrada em arrays
        # do numpy para evitar erros.
        self.matriz_nos = np.array(self.matriz_nos, float)
        self.matriz_conexoes = np.array(self.matriz_conexoes, float)
        self.vetor_forcas = np.array(self.vetor_forcas, float)
        self.vetor_restricoes = np.array(self.vetor_restricoes, int)

    def criarListaDeElementos(self):
        """
            Cria a lista de elementos.
        """

        # Criando a lista de elementos.
        self.elementos = []
        for i in range(self.numero_elementos):
            # Index do nó 1 do elemento.
            indexNo1 = int(self.matriz_conexoes[i][0]) - 1

            # Criando o objeto nó do nó 1 do elemento, passando seu x,
            # y e index do grau de liberdade em x e index do grau de
            # liberdade em y.
            node1 = Node(self.matriz_nos[0][indexNo1],
                         self.matriz_nos[1][indexNo1],
                         (indexNo1) * 2,
                         (indexNo1) * 2 + 1)

            # Index do nó 2 do elemento.
            indexNo2 = int(self.matriz_conexoes[i][1]) - 1

            # Criando o objeto nó do nó 2 do elemento, passando seu x,
            # y e index do grau de liberdade em x e index do grau de
            # liberdade em y.
            node2 = Node(self.matriz_nos[0][indexNo2],
                         self.matriz_nos[1][indexNo2],
                         (indexNo2) * 2,
                         (indexNo2) * 2 + 1)

            # Pegando as variáveis E a A.
            E = self.matriz_conexoes[i][2]
            A = self.matriz_conexoes[i][3]

            # Criando o elemento e adicionando ele na lista de elementos.
            self.elementos.append(Element(node1, node2, E, A, i))

            # Para debugging.
            self.log(f"\nElemento: \n{self.elementos[i]}")

    def criarKg(self):
        """
            Cria a matriz Kg as restrições aplicadas a partir
            da lista de elementos.
        """

        # Criando uma matriz NxN de zeros.
        self.kg = np.zeros((self.numero_nos * 2, self.numero_nos * 2))

        # Passando por todos os elementos e seus respectivos nós e graus de
        # liberdade e somando parte da sua matriz Ke à matriz Kg.
        for elemento in self.elementos:
            self.kg[elemento.node1.gdlX:elemento.node1.gdlX + 2,
                    elemento.node1.gdlX:elemento.node1.gdlX + 2] += elemento.ke[:2, :2]
            self.kg[elemento.node1.gdlX:elemento.node1.gdlX + 2,
                    elemento.node2.gdlX:elemento.node2.gdlX + 2] += elemento.ke[2:, :2]
            self.kg[elemento.node2.gdlX:elemento.node2.gdlX + 2,
                    elemento.node1.gdlX:elemento.node1.gdlX + 2] += elemento.ke[:2, 2:]
            self.kg[elemento.node2.gdlX:elemento.node2.gdlX + 2,
                    elemento.node2.gdlX:elemento.node2.gdlX + 2] += elemento.ke[2:, 2:]

        # Para debugging.
        self.log(f"\nKg não restringido:\n{self.kg}")

    def aplicarRestricoes(self):
        """
            Essa funções cria dois atributos novos: kgRestrito e
            forcasRestrito. Ambos são criados aplicando as restrições,
            ou seja, removendo linhas ou colunas das matrizes kg e
            vetor_forcas.
        """

        # Removendo linhas do vetor de forças.
        self.forcasRestrito = np.delete(
            self.vetor_forcas, self.vetor_restricoes, 0)

        # Removendo linhas da matriz Kg.
        self.kgRestrito = np.delete(self.kg, self.vetor_restricoes, 0)

        # Removendo colunas da matriz KgRestrito.
        self.kgRestrito = np.delete(self.kgRestrito, self.vetor_restricoes, 1)

        # Para debugging.
        self.log(f"\nKg restringido:\n{self.kgRestrito}")
        self.log(f"\nForcas restringido:\n{self.forcasRestrito}")

    def calcularDeslocamento(self):
        """
            Calcula o deslocamento usando o método de Gauss,
            que foi implementado em aula.
        """

        # Criando o objeto solver.
        solver = Solver()

        # Calculando o deslocamento a partir do KgRestrito e ForcasRestrito.
        resultado, _ = solver.gauss(self.kgRestrito, self.forcasRestrito)
        
        # Caso queira usar o Numpy para resolver a equação, descomentas o
        # código abaixo.
        # resultado = np.linalg.solve(self.kgRestrito, self.forcasRestrito)
        # resultado = list(resultado)

        # Expandindo o resultado, ou seja, retirando as restrições.
        # Para fazer isso basta inserir na lista os índices que foram retirados
        # pelas restrições.
        for i in self.vetor_restricoes:
            resultado.insert(int(i), 0)

        # Transformando o resultado em um array do numpy para evitar erros.
        self.deslocamento = np.vstack(np.array(resultado, float))

        # Para debugging.
        self.log(f"\nDeslocamento:\n{self.deslocamento}")

    def calcularReacoesDeApoio(self):
        """
            Calcula as reações de apoio.
        """

        # Calculando as reações de apoio.
        self.reacoesDeApoio = self.kg.dot(self.deslocamento)

        # Para debugging.
        self.log(f"\nReações de Apoio:\n{self.reacoesDeApoio}")

    def calcularResto(self):
        """
            Calcula a deformação, tensão e força em cada elemento.
        """

        # Criando os vetores de deformação, tensão e forças internas.
        self.deformacao = []
        self.tensoes = []
        self.forcas = []

        for elemento in self.elementos:
            # Pegando o deslocamento dos graus de liberdade do elemento.
            deslocamentoDoElemento = np.array(
                [self.deslocamento[grau] for grau in elemento.degrees])

            # Calculando a deformação específica do elemento.
            deformacaoEspecificaNoElemento = np.matmul(
                elemento.m, deslocamentoDoElemento) / elemento.L

            # Calculando as tensões internas do elemento.
            tensoesDoElemento = deformacaoEspecificaNoElemento * elemento.E

            # Calculando as forças internas do elemento.
            forcasDoElemento = tensoesDoElemento * elemento.A

            # Adicionando as variáveis calculadas na lista global.
            self.deformacao.append(deformacaoEspecificaNoElemento)
            self.tensoes.append(tensoesDoElemento)
            self.forcas.append(forcasDoElemento)

        # Transformando todos os vetores em arrays do numpy.
        self.deformacao = np.array(self.deformacao, float)
        self.tensoes = np.array(self.tensoes, float)
        self.forcas = np.array(self.forcas, float)

        # Para debugging.
        self.log(f"\nDeformações:\n{self.deformacao}")
        self.log(f"\nForças internas:\n{self.forcas}")
        self.log(f"\nTensões internas:\n{self.tensoes}")

    def gerarSaida(self):
        """
            Chama a função gerar saída do módulo fornecido
            pelos professores.
        """

        geraSaida(self.outputFilename, self.reacoesDeApoio,
                   self.deslocamento, self.deformacao, self.forcas, self.tensoes)

    def log(self, output):
        """
            Função usada para facilitar o debug do código.
        """

        # Se o modo debug estiver ativado, printar o output.
        if self.debug:
            print(output)
