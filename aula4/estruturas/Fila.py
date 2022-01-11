# Fila
#protocolo da fila -> o primeiro a entra é o primeiro a sair
from estruturas.NodeFila import NodeFila

class FilaEncadeada:
    """Esta classe representa um Fila usando uma estrutura encadeada"""

    def __init__(self):
        self.primeiro = None
        self.ultimo = None

    def __repr__(self):
        return '[' + str(self.primeiro) + ']'

    def enqueue(self, novo_dado):
        """Inserir um elemento no final da fila"""
        novo_node = NodeFila(novo_dado)

        if self.primeiro == None:
            self.primeiro = novo_node
            self.ultimo = novo_node
        else:
            # Faz com que o novo node seja o ultimo da fila
            self.ultimo.proximo = novo_node
            # Faz com que o ultimo da fila referencie o novo node
            self.ultimo = novo_node

    def dequeue(self):
        """Remove o o primeiro elemento da Fila"""
        assert self.primeiro != None, "Impossível remover um elemento da Fila vazia"

        dado = self.primeiro.dado
        
        self.primeiro = self.primeiro.proximo

        if self.primeiro == None:
            self.ultimo = None

        return dado