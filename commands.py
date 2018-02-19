import re 
from .solver import (
    Node,
    find_path,
    find_paths,
    find_all_paths,
    find_path_exactly_stops,
    find_path_maximum_stops,
    find_path_less_than_distance,
)


class Command():
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def match(self, command):
        _match = re.match(self.pattern, command)

        if not _match:
            return False

        self.parameter = _match.group('parameter')
        return True

    def run(self, command):
        if self.match(command):
            return self._run()

    def _run(self):
        raise NotImplementedError()


class CreateGraph(Command):
    def __init__(self):
        super().__init__('^create\sgraph\s(?P<parameter>([A-Z][A-Z][0-9]{1,9}\s?)+)?$')

    def _run(self):
        graph = {}
        edges = self.parameter.split(' ')
        for edge in edges:
            from_node = edge[0]
            to_node = edge[1]
            weight = edge[2:]
            if not graph.get(from_node, None):
                graph[from_node] = Node(from_node)
            if not graph.get(to_node, None):
                graph[to_node] = Node(to_node)
            graph[from_node].connect(graph[to_node], int(weight))
        return graph


class ShortestPath(Command):
    def __init__(self, graph):
        self.graph = graph
        super().__init__('^shortest\spath\s(?P<parameter>[A-Z?\-?]+)$')

    def _run(self):
        path = self.parameter.split('-')
        paths = find_all_paths(self.graph[path[0]], self.graph[path[1]])
        shortest_path = paths[0]
        for path in paths:
            if path.distance < shortest_path.distance:
                shortest_path = path

        return shortest_path


class PathsByDistance(Command):
    def __init__(self):
        super().__init__('^paths\sof\smaximum\sdistance\s(?P<parameter>[0-9]{1,9})$')


class PathsOfExactlyStops(Command):
    def __init__(self):
        super().__init__('^paths\sof\sexactly\s(?P<parameter>[0-9]{1,9})\sstops$')


class PathsByStops(Command):
    def __init__(self):
        super().__init__('^paths\sof\s(?P<parameter>[0-9]{1,9})\sstops$')
