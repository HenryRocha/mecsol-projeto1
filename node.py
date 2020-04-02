class Node():
    def __init__(self, x, y, gdlX, gdlY, index):
        """
            Essa função é executada na criação do objeto Nó.
            Serve para guardar todas as informações de um nó.

            @param x posição x do nó
            @param y posição y do nó
            @param gdlX número do grau de liberdade em X
            @param gdlY número do grau de liberdade em Y
        """

        self.x = x
        self.y = y
        self.gdlX = gdlX
        self.gdlY = gdlY
        self.index = index

    def __str__(self):
        """
            Essa função é chamada quando se tenta printar
            um objeto nó.
        """

        out = f"x: {self.x} gdl: {self.gdlX}\n"
        out += f"y: {self.y} gdl: {self.gdlY}"
        return out
