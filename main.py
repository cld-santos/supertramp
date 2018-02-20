from supertramp.commands import (
    Exit,
    CreateGraph,
    ShortestPath,
    PathsByDistance,
    PathsOfExactlyStops,
    PathsByStops,
    PathDistance,
)


def run(commands, command):
    for item in commands:
        if item.match(command):
            result = item.run(command)
            return result

    raise Exception('Command not found.')


def print_samples():
    print('# Command samples:')
    print('  shortest path A-C')
    print('  paths of maximum distance 30 between C and C')
    print('  paths from A to C of exactly 4 stops')
    print('  paths from A to C of 4 stops')
    print('  distance of this path A-B-C')
    print('  exit')


def print_error(e):
    print('#################################')
    print('### ERROR:', e, '###')
    print('#################################')


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Solve paths in a graph.')
    parser.add_argument('-e', '--edges', nargs='+', help='edges to create the graph')

    graph = None
    args = parser.parse_args()
    if args.edges:
        edges = [edge.replace(',', '').strip() for edge in args.edges]
        creator = CreateGraph()
        graph = creator.run(" ".join(edges))
    else:
        creator = CreateGraph()
        while graph is None:
            print('Type the edges of your graph (AB5 BC4 CD8 DC8 DE6 AD5 CE2 EB3 AE7):')
            graph_param = input()
            try:
                graph = creator.run(graph_param)
            except Exception as e:
                print_error(e)
                graph = None


    if graph:
        print('# Info: Graph built.')

    commands = [
        Exit(),
        ShortestPath(graph),
        PathsByDistance(graph),
        PathsOfExactlyStops(graph),
        PathsByStops(graph),
        PathDistance(graph)
    ]

    instructions = [
        'distance of this path A-B-C',
        'distance of this path A-D',
        'distance of this path A-D-C',
        'distance of this path A-E-B-C-D',
        'distance of this path A-E-D',
        'paths from C to C of 3 stops',
        'paths from A to C of exactly 4 stops',
        'shortest path A-C',
        'shortest path B-B',
        'paths of maximum distance 30 between C and C',
    ]

    for instruction in instructions:
        print(instruction)
        result = run(commands, instruction)
        print(result)

    print_samples()
    while True:
        print('Type a command:')
        try:
            command = input()
            result = run(commands, command)
            print(result)
        except Exception as e:
            print_error(e)
            print_samples()
