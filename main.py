from structure import Structure

if __name__ == "__main__":
    structure = Structure("entrada-aulas-5-6.xlsx", outputFilename="saida-aulas-5-6-grupo14.txt", debug=True)
    # structure = Structure("entrada-atividade-aula-10.xlsx", outputFilename="saida-atividade-aula-10.txt", debug=True)
    # structure = Structure("entrada-entrega.xlsx", outputFilename="saida-entrega-grupo14.txt", debug=True)

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

    # Plota os pontos.
    structure.plota()
