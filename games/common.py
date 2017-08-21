class InvalidPlay(Exception):
    pass


class Position(object):

    def __init__(self, i, j=None):
        if isinstance(i, Position):
            i = i.i
            j = i.j
        elif j is None:
            i = i % 3
            j = i // 3
        self.i = i
        self.j = j

    def __str__(self):
        return "Position(%s, %s)" % (self.i, self.j)

    def __repr__(self):
        return self.__str__()

