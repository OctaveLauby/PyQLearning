class Game(object):

    states = None
    actions = None

    def __init__(self):
        self.cls = self.__class__

    def is_over(self):
        raise NotImplementedError

    def act(self, action, player):
        raise NotImplementedError

    def state(self):
        raise NotImplementedError
