# Pilha
#protocolo da pilha -> o ultimo a entrar é o primeiro a sair
from estruturas.NodePilha import NodePilha


class PilhaEncadeada:
    """Esta classe representa uma lista encadeada"""
    def __init__(self):
        self.topo = None
    
    def __repr__(self):
        return '[' + str(self.topo) + ']'

    def push(self, novo_dado):
        """Insere um elemento no topo da pilha"""
        # Cria um novo node com o dado a ser armazenado
        novo_node = NodePilha(novo_dado)
        # Faz com que o novo node seja o topo da pilha
        novo_node.anterior = self.topo
        # Faz com que o topo da pilha referencie o novo node
        self.topo = novo_node

    def pop(self) -> int:
        """Remove o elemento que esta no topo da pilha"""
        assert self.topo, "Impossível remover valor de pilha vazia."
        dado = self.topo.dado
        self.topo = self.topo.anterior
        return dado