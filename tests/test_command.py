from ..commands import (
    Command,
    CreateGraph,
    ShortestPath,
    PathsByDistance,
    PathsOfExactlyStops,
    PathsByStops,
)


def test_must_match_a_pattern_from_command():
    command = Command('^shortest\spath\s(?P<parameter>[A-Z?\-?]+)$')
    assert command.match('shortest path A-B-C') is True
    assert command.parameter == 'A-B-C'


def test_create_graph_parameters():
    command = CreateGraph()
    assert command.match('create graph AB5 BC12') is True
    assert len(command.parameter.split(' ')) == 2


def test_create_graph():
    command = CreateGraph()
    graph = command.run('create graph AB5 BC12')
    assert len(graph) == 3

    assert graph['A'].edges[0].to_node.id == 'B'
    assert graph['A'].edges[0].weight == 5

    assert graph['B'].edges[0].to_node.id == 'C'
    assert graph['B'].edges[0].weight == 12


def test_shortest_path_parameters():
    command = CreateGraph()
    graph = command.run('create graph AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7')
    command = ShortestPath(graph)
    shortest_path = command.run('shortest path A-C')
    assert 'A-B-C' == "-".join(sorted(shortest_path.get_path()))


def test_solve_shortest_path():
    command = ShortestPath(None)
    assert command.match('shortest path A-B-C') is True
    assert command.parameter == 'A-B-C'


def test_paths_of_maximum_distace():
    command = PathsByDistance()
    assert command.match('paths of maximum distance 30') is True
    assert command.parameter == '30'


def test_paths_of_exactly_stops():
    command = PathsOfExactlyStops()
    assert command.match('paths of exactly 4 stops') is True
    assert command.parameter == '4'


def test_paths_of_stops():
    command = PathsByStops()
    assert command.match('paths of 4 stops') is True
    assert command.parameter == '4'
