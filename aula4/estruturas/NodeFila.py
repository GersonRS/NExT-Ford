class NodeFila:
    """Esta classe representa um node de uma lista encadeada"""
    def __init__(self, dado=0, proximo_node=None):
        self.dado = dado
        self.proximo = proximo_node

    def __repr__(self):
        return '%s -> %s' % (self.dado, self.proximo)