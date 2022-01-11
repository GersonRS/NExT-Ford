class NodePilha:
    """Esta classe representa um node de uma lista encadeada"""
    def __init__(self, dado=0, anterior_node=None):
        self.dado = dado
        self.anterior = anterior_node

    def __repr__(self):
        return '%s -> %s' % (self.dado, self.anterior)