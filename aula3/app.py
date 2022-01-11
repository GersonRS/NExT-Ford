lista = ["A","B","C","D","E"]
               
lista.insert(2, "Z")

del(lista[2])

"""equivalencia em JAVA"""

# import System.Util.ArrayList;
# public int[] lista_arranjo = new int[10];
# ArrayList<int> lista_interos = new ArrayList<int>();

class Nodelista:
    """Esta classe representa um node de uma lista encadeada"""
    def __init__(self, dado=0, proximo_node=None):
        self.dado = dado
        self.proximo = proximo_node

    def __repr__(self):
        return '%s -> %s' % (self.dado, self.proximo)

class ListaEncadeada:
    """Esta classe representa uma lista encadeada"""
    def __init__(self):
        self.cabeca = None

    # @staticmethod
    # def criar_objeto2(valor1, valor2):
    #     lista = ListaEncadeada(valor1, valor2)
    #     return lista

    def insere_no_inicio(self, novo_dado):
        """Insere um elemento no começo da lista"""
        # cria um novo node com o dado a ser armazenado
        novo_node = Nodelista(novo_dado)
        # faz com que o novo node seja a cabeça da lista
        novo_node.proximo = self.cabeca
        # faz com que a cabeça da lista referencie o novo node
        self.cabeca = novo_node

    def insere_depois(self, valor, novo_dado):
        # gera uma exceção caso a variavel seja None(nulo do JAVA)
        valor_encontrado = self.busca(valor)

        assert valor_encontrado, "Node anterior precisa existir na lista"
        # cria um novo node com o dado desejado
        novo_node = Nodelista(novo_dado)
        # faz o proximo do novo node ser o proximo do node anterios
        novo_node.proximo = valor_encontrado.proximo
        # faz com que o novo node seja o proximo do node anterior
        valor_encontrado.proximo = novo_node

    def busca(self, valor):
        """assert é como se fosse um if que da erro caso falso"""
        assert valor != 0, "valor incorreto"
        corrente = self.cabeca
        while corrente and corrente.dado != valor:
            corrente = corrente.proximo
        return corrente

    def remove(self, valor):
        assert self.cabeca, "Impossivel remover valor de lista vazia"

        # Node a ser removido é a cabeça da lista
        if self.cabeca.dado == valor:
            self.cabeca = self.cabeca.proximo
        else:
            # Encontrar a posição do elemento a ser removido
            anterio = None
            corrente = self.cabeca
            while corrente and corrente.dado != valor:
                anterio = corrente
                corrente = corrente.proximo
            # o node corrente é o node a ser removido
            if corrente:
                anterio.proximo = corrente.proximo
            else:
                # o node corrente é o ultimo elemento
                anterio.proximo = None

    def __repr__(self):
        return '[' + str(self.cabeca) + ']'

lista_encadeada = ListaEncadeada()
lista_encadeada.insere_no_inicio(5)
print(lista_encadeada)
lista_encadeada.insere_no_inicio(10)
print(lista_encadeada)

lista_encadeada.insere_depois(10, 15)
print(lista_encadeada)

# print(lista_encadeada.busca(15))

lista_encadeada.remove(15)
print(lista_encadeada)