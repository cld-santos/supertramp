from ..solver import Node, find_path


def test_find_path_atob():
    node_a = Node('A')
    node_b = Node('B')
    node_a.connect(node_b, distance=5)
    assert find_path(node_a, node_b) == 5
