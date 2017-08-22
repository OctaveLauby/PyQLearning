class Position(object):

    def __init__(self, first, second=None):
        if isinstance(first, Position):
            self.i = first.i
            self.j = first.j
        elif second is None:
            self.i = first % 3
            self.j = first // 3
        else:
            self.i = first
            self.j = second

    def __eq__(self, other):
        return (self.i, self.j) == (other.i, other.j)

    def __str__(self):
        return "Position(%s, %s)" % (self.i, self.j)

    def __repr__(self):
        return self.__str__()
