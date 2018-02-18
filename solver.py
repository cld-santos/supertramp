class Edge():
    def __init__(self, from_node, to_node, weight=0):
        self.from_node = from_node
        self.to_node = to_node 
        self.weight = weight


class Node():
    def __init__(self, id):
        self.id = id
        self.edges = []

    def connect(self, node, distance):
        self.edges.append(Edge(self, node, weight=distance))


def find_path(from_node, to_node):
    for edge in from_node.edges:
        return edge.weight if edge.to_node.id == to_node.id else None
