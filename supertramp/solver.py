from copy import deepcopy 


class WeightBeyondThanRequiredException(Exception):
    pass


class Path():
    def __init__(self, node, parent=None, distance=0, stops=0):
        self.node = node
        self.parent = parent
        self.distance = distance
        self.stops = stops
        self.next = None

    def get_path(self):
        path = ['N:{0}, D:{1}'.format(self.node.id, self.distance)]
        if self.parent:
            path.extend(self.parent.get_path())

        return path

    def go_down(self):
        path = [self.node.id]
        if self.next:
            path.extend(self.next.go_down())

        return path

    def update_next(self):
        if self.parent:
            self.parent.next = self
            self.parent.update_next()

    def get_leaf(self):
        if self.next:
            return self.next.get_leaf()
        else:
            return self

    def get_distance(self):
        total_distance = self.distance 
        if self.parent:
            total_distance += self.parent.get_distance()
        return total_distance


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
                distance=edge.weight,
                stops=path.stops+1 if path else 1)

            result = self._check(_path, to_node)

            if result and result.get('path', None):
                amount_paths.append(result['path'])

            if result and result.get('continue', None):
                continue 

            amount_paths.extend(self.solve_path_between(edge.to_node, to_node, path=_path))

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
            checked_path = deepcopy(self.visited[key].next if self.visited[key].next else self.visited[key])
            checked_path.parent = path
            leaf = checked_path.get_leaf()
            return {'path': leaf, 'continue': True}

        self.visited[key] = path

        if path.node.id == to_node.id:
            path.update_next()
            checked_path = path

        return {'path': checked_path, 'continue': checked_path is not None}


class SolverPathByStop(SolverPath):

    def __init__(self, number_of_stops):
        self.number_of_stops = number_of_stops

    def _check(self, path, to_node):
        if path.stops > self.number_of_stops:
            return {'continue': True}

        if path.node.id == to_node.id:
            if path.stops == self.number_of_stops:
                return {'path': path, 'continue': True}


class SolverPathByMaxStops(SolverPath):

    def __init__(self, max_stops):
        self.max_stops = max_stops

    def _check(self, path, to_node):
        if path.node.id == to_node.id:
            if path.stops <= self.max_stops:
                return {'path': path, 'continue': True}
            return {'continue': True}


class SolverPathByDistance(SolverPath):

    def __init__(self, max_distance):
        self.max_distance = max_distance

    def _check(self, path, to_node):
        if path.get_distance() > self.max_distance:
            return {'continue': True}

        if path.node.id == to_node.id:
            if path.get_distance() < self.max_distance:
                return {'path': path, 'continue': False}
