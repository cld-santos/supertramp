import re 


class Command():
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def match(self, command):
        _match = re.match(self.pattern, command)

        if not _match:
            return False

        self.parameter = _match.group('parameter')
        return True

    def run(self, *parameters):
        raise NotImplementedError()


class CreateGraph(Command):
    def __init__(self):
        super().__init__('^create\sgraph\s(?P<parameter>([A-Z][A-Z][0-9]{1,9}\s?)+)?$')


class ShortestPath(Command):
    def __init__(self):
        super().__init__('^shortest\spath\s(?P<parameter>[A-Z?\-?]+)$')


class PathsByDistance(Command):
    def __init__(self):
        super().__init__('^paths\sof\smaximum\sdistance\s(?P<parameter>[0-9]{1,9})$')


class PathsOfExactlyStops(Command):
    def __init__(self):
        super().__init__('^paths\sof\sexactly\s(?P<parameter>[0-9]{1,9})\sstops$')


class PathsByStops(Command):
    def __init__(self):
        super().__init__('^paths\sof\s(?P<parameter>[0-9]{1,9})\sstops$')
