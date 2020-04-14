# transcal-projeto1
Repositório para o projeto 1 de Transferência de Calor e Mecânica dos Sólidos. Software que simula as forças em uma estrutura de treliças.


## Argumentos
O software usa da biblioteca Argparse para ter uma melhor integração com a linha de comando. Todos os argumentos possíveis estão listados abaixo:
```
usage: python3 main.py [-h] [-d] -s {gauss,jacobi,numpy} -i INPUT -o OUTPUT

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           run the software in debug mode

required arguments:
  -s {gauss,jacobi,numpy}, --solver {gauss,jacobi,numpy}
                        solving method
  -i INPUT, --input INPUT
                        name of the input file
  -o OUTPUT, --output OUTPUT
                        name of the output file
```

Essas mesmas informações podem ser obtidas rodando o comando a seguir:
```
python3 main.py --help
```

## Como executar
Seguindo as informações do tópico anterior, podemos rodar o software com o seguinte comando:
```
python3 main.py -s gauss -i entrada-ponte.xlsx -o saida-ponte.txt
```
