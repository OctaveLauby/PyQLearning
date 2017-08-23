from parameters import LOG_LEVEL
from utils.log import create_logger


class Game(object):

    def __init__(self):
        self.cls = self.__class__
        self.log = create_logger(
            self.__class__.__name__,
            log_level=LOG_LEVEL
        )

    def is_over(self):
        """Return whether game is over."""
        raise NotImplementedError

    def act(self, action, player):
        """Act for player."""
        raise NotImplementedError

    def reset(self):
        """Restart game."""
        raise NotImplementedError

    def actions(self):
        """Possible actions given the state"""
        raise NotImplementedError

    def actions_all(self):
        """All possible actions."""
        raise NotImplementedError

    def state(self):
        """Current state."""
        raise NotImplementedError
