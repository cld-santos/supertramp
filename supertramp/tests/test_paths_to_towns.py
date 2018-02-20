import pytest
from ..solver import (
    Node,
    SolveAllPaths,
    SolverPathByStop,
    SolverPathByMaxStops,
    SolverPathByDistance,
)


def test_find_path_atob():
    node_a = Node('A')
    node_b = Node('B')
    node_a.connect(node_b, distance=5)
    solve_all_paths = SolveAllPaths()
    assert solve_all_paths.distance_between(node_a, node_b) == 5


def test_dont_find_path_atob():
    node_a = Node('A')
    node_b = Node('B')
    solve_all_paths = SolveAllPaths()

    with pytest.raises(Exception):
        solve_all_paths.distance_between(node_a, node_b) == 0


def test_get_distance_from_path():
    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    node_a.connect(node_b, distance=5)
    node_b.connect(node_c, distance=4)
    solve_all_paths = SolveAllPaths()
    assert solve_all_paths.distance_from([node_a, node_b, node_c]) == 9


def test_dont_get_distance_from_path():
    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    node_a.connect(node_b, distance=5) # AB5
    solve_all_paths = SolveAllPaths()

    with pytest.raises(Exception) as e:
        solve_all_paths.distance_from([node_a, node_b, node_c]) == 9
        assert e.value == 'Path not found.'


def test_get_all_paths_from():
    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    node_d = Node('D')
    node_e = Node('E')
    node_a.connect(node_b, distance=5) # AB5
    node_b.connect(node_c, distance=4) # BC4
    node_c.connect(node_d, distance=8) # CD8
    node_d.connect(node_c, distance=8) # DC8
    node_d.connect(node_e, distance=6) # DE6
    node_a.connect(node_d, distance=5) # AD5
    node_c.connect(node_e, distance=2) # CE2
    node_e.connect(node_b, distance=3) # EB3
    node_a.connect(node_e, distance=7) # AE7
    solve_all_paths = SolveAllPaths()
    
    paths = solve_all_paths.solve_path_between(node_b, node_b)
    assert len(paths) == 4
    for path in paths:
        _path = path.get_path()
        print(_path, path.distance, path.stops)


def test_get_all_paths_of_exactly_number_of_stops():
    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    node_d = Node('D')
    node_e = Node('E')
    node_a.connect(node_b, distance=5) # AB5
    node_b.connect(node_c, distance=4) # BC4
    node_c.connect(node_d, distance=8) # CD8
    node_d.connect(node_c, distance=8) # DC8
    node_d.connect(node_e, distance=6) # DE6
    node_a.connect(node_d, distance=5) # AD5
    node_c.connect(node_e, distance=2) # CE2
    node_e.connect(node_b, distance=3) # EB3
    node_a.connect(node_e, distance=7) # AE7
    
    solver_path_by_stop = SolverPathByStop(4)
    paths = solver_path_by_stop.solve_path_between(node_b, node_b)
    assert len(paths) == 1
    for path in paths:
        _path = path.get_path()
        print(_path, path.distance, path.stops)


def test_get_all_paths_at_least_stops():
    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    node_d = Node('D')
    node_e = Node('E')
    node_a.connect(node_b, distance=5) # AB5
    node_b.connect(node_c, distance=4) # BC4
    node_c.connect(node_d, distance=8) # CD8
    node_d.connect(node_c, distance=8) # DC8
    node_d.connect(node_e, distance=6) # DE6
    node_a.connect(node_d, distance=5) # AD5
    node_c.connect(node_e, distance=2) # CE2
    node_e.connect(node_b, distance=3) # EB3
    node_a.connect(node_e, distance=7) # AE7

    solver_path_by_max_stops = SolverPathByMaxStops(3)
    paths = solver_path_by_max_stops.solve_path_between(node_c, node_c)
    assert len(paths) == 2
    for path in paths:
        _path = path.get_path()
        print(_path, path.distance, path.stops)


def test_get_all_paths_max_distance():
    node_a = Node('A')
    node_b = Node('B')
    node_c = Node('C')
    node_d = Node('D')
    node_e = Node('E')
    node_a.connect(node_b, distance=5) # AB5
    node_b.connect(node_c, distance=4) # BC4
    node_c.connect(node_d, distance=8) # CD8
    node_d.connect(node_c, distance=8) # DC8
    node_d.connect(node_e, distance=6) # DE6
    node_a.connect(node_d, distance=5) # AD5
    node_c.connect(node_e, distance=2) # CE2
    node_e.connect(node_b, distance=3) # EB3
    node_a.connect(node_e, distance=7) # AE7
    solver_path_by_distance = SolverPathByDistance(30)
    paths = solver_path_by_distance.solve_path_between(node_c, node_c)
    assert len(paths) == 7
    for path in paths:
        _path = path.get_path()
        print(_path, path.distance, path.stops)

