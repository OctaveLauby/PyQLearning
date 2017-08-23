from parameters import LOG_LEVEL
from utils.log import create_logger


class Game(object):

    states = None
    actions = None

    def __init__(self):
        self.cls = self.__class__

        self.log = create_logger(
            self.__class__.__name__,
            log_level=LOG_LEVEL
        )

    def is_over(self):
        raise NotImplementedError

    def act(self, action, player):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def state(self):
        raise NotImplementedError
