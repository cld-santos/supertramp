import re 
from .solver import (
    Node,
    SolveAllPaths,
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


class Exit(Command):
    def __init__(self):
        self.pattern = 'exit'

    def match(self, command):
        return command.lower().strip() == self.pattern

    def _run(self):
        print('leaving the graph solver')
        exit()


class CreateGraph(Command):
    def __init__(self):
        super().__init__('^(?P<parameter>([A-Z][A-Z][0-9]{1,9}\s?)+)?$')

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


class PathDistance(Command):
    def __init__(self, graph):
        self.graph = graph
        super().__init__('^distance\sof\sthis\spath\s(?P<parameter>[A-Z?\-?]+)$')

    def _run(self):
        path_params = self.parameter.split('-')
        try:
            solve_all_paths = SolveAllPaths()
            return solve_all_paths.distance_from([self.graph[path] for path in path_params])
        except Exception as e:
            return str(e)


class ShortestPath(Command):
    def __init__(self, graph):
        self.graph = graph
        super().__init__('^shortest\spath\s(?P<parameter>[A-Z?\-?]+)$')

    def _run(self):
        path = self.parameter.split('-')
        solve_all_paths = SolveAllPaths()
        paths = solve_all_paths.solve_path_between(self.graph[path[0]], self.graph[path[1]])
        shortest_path = paths[0]
        for path in paths:
            if path.get_distance() < shortest_path.get_distance():
                shortest_path = path

        return shortest_path.get_distance()


class CommandWithWeight(Command):
    def match(self, command):
        _match = re.match(self.pattern, command)

        if not _match:
            return False

        self.from_node = self.graph[_match.group('from_node')]
        self.to_node = self.graph[_match.group('to_node')]
        self.weight = int(_match.group('weight'))
        return True


class PathsByDistance(CommandWithWeight):
    def __init__(self, graph):
        self.graph = graph
        super().__init__('^paths\sof\smaximum\sdistance\s(?P<weight>[0-9]{1,9})\sbetween\s(?P<from_node>[A-Z])\sand\s(?P<to_node>[A-Z])')

    def _run(self):
        paths = find_path_less_than_distance(self.from_node, self.to_node, self.weight)
        return len(paths)


class PathsOfExactlyStops(CommandWithWeight):
    def __init__(self, graph):
        self.graph = graph
        super().__init__('^paths\sfrom\s(?P<from_node>[A-Z])\sto\s(?P<to_node>[A-Z])\sof\sexactly\s(?P<weight>[0-9]{1,9})\sstops$')

    def _run(self):
        paths = find_path_exactly_stops(self.from_node, self.to_node, self.weight)
        return len(paths)


class PathsByStops(CommandWithWeight):
    def __init__(self, graph):
        self.graph = graph
        super().__init__('^paths\sfrom\s(?P<from_node>[A-Z])\sto\s(?P<to_node>[A-Z])\sof\s(?P<weight>[0-9]{1,9})\sstops$')

    def _run(self):
        paths = find_path_maximum_stops(self.from_node, self.to_node, self.weight)
        return len(paths)
