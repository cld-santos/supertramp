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


def test_shortest_path_parameters():
    command = ShortestPath()
    assert command.match('shortest path A-B-C') is True
    assert command.parameter == 'A-B-C'


def test_create_graph_parameters():
    command = CreateGraph()
    assert command.match('create graph AB5 BC12') is True
    assert len(command.parameter.split(' ')) == 2


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
