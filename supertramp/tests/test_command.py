from ..commands import (
    Command,
    CreateGraph,
    ShortestPath,
    PathsByDistance,
    PathsOfExactlyStops,
    PathsByStops,
    PathDistance,
)


def test_must_match_a_pattern_from_command():
    command = Command('^shortest\spath\s(?P<parameter>[A-Z?\-?]+)$')
    assert command.match('shortest path A-B-C') is True
    assert command.parameter == 'A-B-C'


def test_create_graph_parameters():
    command = CreateGraph()
    assert command.match('AB5 BC12') is True
    assert len(command.parameter.split(' ')) == 2


def test_create_graph():
    command = CreateGraph()
    graph = command.run('AB5 BC12')
    assert len(graph) == 3

    assert graph['A'].edges[0].to_node.id == 'B'
    assert graph['A'].edges[0].weight == 5

    assert graph['B'].edges[0].to_node.id == 'C'
    assert graph['B'].edges[0].weight == 12


def test_shortest_path_parameters():
    command = ShortestPath(None)
    assert command.match('shortest path A-B-C') is True
    assert command.parameter == 'A-B-C'


def test_paths_of_maximum_distace():
    command = CreateGraph()
    graph = command.run('AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7')
    command = PathsByDistance(graph)
    assert command.match('paths of maximum distance 30 between A and C') is True
    assert command.from_node.id == graph['A'].id
    assert command.to_node.id == graph['C'].id
    assert command.weight == 30


def test_paths_of_exactly_stops():
    command = CreateGraph()
    graph = command.run('AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7')
    command = PathsOfExactlyStops(graph)
    assert command.match('paths from A to C of exactly 4 stops') is True
    assert command.from_node.id == graph['A'].id
    assert command.to_node.id == graph['C'].id
    assert command.weight == 4


def test_paths_of_stops():
    command = CreateGraph()
    graph = command.run('AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7')
    command = PathsByStops(graph)
    result = command.match('paths from A to C of 4 stops')
    assert result is True
    assert command.from_node.id == graph['A'].id
    assert command.to_node.id == graph['C'].id
    assert command.weight == 4


def test_solve_shortest_path():
    command = CreateGraph()
    graph = command.run('AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7')
    command = ShortestPath(graph)
    result = command.run('shortest path B-B')
    assert result == 9


def test_solve_paths_of_maximum_distace():
    command = CreateGraph()
    graph = command.run('AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7')
    command = PathsByDistance(graph)
    result = command.run('paths of maximum distance 30 between C and C')
    assert result == 7


def test_solve_paths_of_exactly_stops():
    command = CreateGraph()
    graph = command.run('AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7')
    command = PathsOfExactlyStops(graph)
    result = command.run('paths from A to C of exactly 4 stops')
    assert result == 3


def test_solve_paths_of_stops():
    command = CreateGraph()
    graph = command.run('AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7')
    command = PathsByStops(graph)
    result = command.run('paths from A to C of 4 stops')
    assert result == 4


def test_get_distance_from_path():
    command = CreateGraph()
    graph = command.run('AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7')
    command = PathDistance(graph)
    result = command.run('distance of this path A-B-C')
    assert result == 9 
