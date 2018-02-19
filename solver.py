from copy import deepcopy 


class Path():
    def __init__(self, node, parent=None, distance=0, stops=0):
        self.node = node
        self.parent = parent
        self.distance = distance
        self.stops = stops

    def get_path(self):
        path = [self.node.id]
        if self.parent:
            path.extend(self.parent.get_path())

        return path


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

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Node({0})".format(str(self.id)) + ("{" + ", ".join([str(node.to_node.id) for node in self.edges]) + "}" if self.edges else "")


def find_path(from_node, to_node):
    for edge in from_node.edges:
        if edge.to_node.id == to_node.id:
            return edge.weight
    raise Exception("Path not found.")


def find_paths(nodes):
    total_distance = 0

    for idx in range(len(nodes)-1):
        total_distance += find_path(nodes[idx], nodes[idx+1])
    return total_distance


def find_all_paths(from_node, to_node, visited={}, path=None):
    amount_paths = []

    for edge in from_node.edges:
        if not path:
            path = Path(from_node)

        _path = Path(
            edge.to_node,
            parent=path,
            distance=path.distance+edge.weight if path else edge.weight,
            stops=path.stops+1 if path else 1)

        key = '{0}-{1}'.format(edge.from_node.id, edge.to_node.id)
        if visited.get(key, None):
            _aux = deepcopy(visited[key])
            _aux.parent = _path
            amount_paths.append(_aux)
            continue

        visited[key] = []

        if edge.to_node.id == to_node.id:
            amount_paths.append(_path)
            continue

        amount_paths.extend(find_all_paths(edge.to_node, to_node, visited, path=_path))
        visited[key] = _path

    return amount_paths


def find_path_exactly_stops(from_node, to_node, number_of_stops, path=None):
    amount_paths = []

    for edge in from_node.edges:
        if not path:
            path = Path(from_node)

        _path = Path(
            edge.to_node,
            parent=path,
            distance=path.distance+edge.weight if path else edge.weight,
            stops=path.stops+1 if path else 1)

        if edge.to_node.id == to_node.id:
            if _path.stops == number_of_stops:
                amount_paths.append(_path)
            continue

        amount_paths.extend(find_path_exactly_stops(edge.to_node, to_node, number_of_stops, path=_path))

    return amount_paths


def find_path_maximum_stops(from_node, to_node, max_stops, path=None):
    amount_paths = []

    for edge in from_node.edges:
        if not path:
            path = Path(from_node)

        _path = Path(
            edge.to_node,
            parent=path,
            distance=path.distance+edge.weight if path else edge.weight,
            stops=path.stops+1 if path else 1)

        if edge.to_node.id == to_node.id:
            if _path.stops <= max_stops:
                amount_paths.append(_path)
            continue

        amount_paths.extend(find_path_maximum_stops(edge.to_node, to_node, max_stops, path=_path))

    return amount_paths


def find_path_less_than_distance(from_node, to_node, max_distance, path=None):
    amount_paths = []

    for edge in from_node.edges:
        if not path:
            path = Path(from_node)

        _path = Path(edge.to_node, parent=path, distance=path.distance+edge.weight, stops=path.stops+1)

        if _path.distance > max_distance:
            continue 

        if edge.to_node.id == to_node.id:
            if _path.distance < max_distance:
                amount_paths.append(_path)

        amount_paths.extend(find_path_less_than_distance(edge.to_node, to_node, max_distance, path=_path))

    return amount_paths
