from structure import Structure
import argparse

if __name__ == "__main__":
    # Configurando o Argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="run the software in debug mode", action="store_true")
    requiredArgs = parser.add_argument_group("required arguments")
    requiredArgs.add_argument("-s", "--solver", help="solving method", type=str, choices=["gauss", "jacobi", "numpy"], required=True)
    requiredArgs.add_argument("-i", "--input", help="name of the input file", required=True)
    requiredArgs.add_argument("-o", "--output", help="name of the output file", required=True)
    args = parser.parse_args()

    # Criando o objeto.
    structure = Structure(args.input, outputFilename=args.output, solvingMethod=args.solver, debug=args.debug)

    # Criando a lista de elementos.
    structure.criarListaDeElementos()

    # Criando a matriz Kg sem as restrições aplicadas.
    structure.criarKg()

    # Aplicando as restrições na matriz Kg.
    structure.aplicarRestricoes()

    # Calculando o deslocamento.
    structure.calcularDeslocamento()

    # Calculando as reações de apoio.
    structure.calcularReacoesDeApoio()

    # Calcular as deformações, tensões internas e forças internas.
    structure.calcularResto()

    # Gerando o arquivo de saída.
    structure.gerarSaida()

    # Calcula o peso da estrutura.
    structure.calculaPeso()

    # Verifica se a estrutura está dentro das limitações.
    structure.checaLimitacoes()

    # Plota os pontos.
    structure.plota()
