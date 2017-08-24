import json
import os

from parameters import LOG_LEVEL
from utils.log import create_logger

KWARGS_FILE = "kwargs.json"


class Game(object):

    def __init__(self, **kwargs):
        self.cls = self.__class__
        self.log = create_logger(
            self.__class__.__name__,
            log_level=LOG_LEVEL
        )
        self.kwargs = kwargs
        self.kwargs['cls'] = self.__class__.__name__

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

    def save(self, directory):
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        path = os.path.join(directory, KWARGS_FILE)
        self.log.info("Save kwargs at '%s'")
        with open(path, "w") as file:
            json.dump(self.kwargs, file)

    def __str__(self):
        return self.__class__.__name__
