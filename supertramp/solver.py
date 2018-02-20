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


class SolverPath():

    def distance_between(self, from_node, to_node):
        for edge in from_node.edges:
            if edge.to_node.id == to_node.id:
                return edge.weight
        raise Exception("NO SUCH ROUTE")

    def distance_from(self, nodes):
        total_distance = 0

        for idx in range(len(nodes)-1):
            total_distance += self.distance_between(nodes[idx], nodes[idx+1])
        return total_distance

    def solve_path_between(self, from_node, to_node, path=None):
        amount_paths = []

        for edge in from_node.edges:
            if not path:
                path = Path(from_node)

            _path = Path(
                edge.to_node,
                parent=path,
                distance=path.distance+edge.weight if path else edge.weight,
                stops=path.stops+1 if path else 1)

            checked_path = self._check(_path, to_node)
            if checked_path:
                amount_paths.append(checked_path)
                continue 

            amount_paths.extend(find_all_paths(edge.to_node, to_node, path=_path))

        return amount_paths

    def _check(self, path, to_node):
        raise NotImplementedError()


class SolveAllPaths(SolverPath):
    def __init__(self):
        self.visited = {}

    def _check(self, path, to_node):
        key = '{0}-{1}'.format(path.parent.node.id, path.node.id)
        checked_path = None
        if self.visited.get(key, None):
            checked_path = deepcopy(self.visited[key])
            checked_path.parent = path
        self.visited[key] = path

        if path.node.id == to_node.id:
            checked_path = path

        return checked_path


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

        if _path.stops > number_of_stops:
            continue 

        if edge.to_node.id == to_node.id:
            if _path.stops == number_of_stops:
                amount_paths.append(_path)

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
