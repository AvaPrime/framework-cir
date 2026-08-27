class CompletelyOrdinaryBuilder:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, name, fn):
        self.nodes[name] = fn

    def add_edge(self, src, dst):
        self.edges.append((src, dst))

    def route(self, name):
        return self.nodes.get(name)
