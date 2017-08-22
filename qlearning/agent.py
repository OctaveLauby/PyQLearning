import numpy as np
import random

from parameters import LOG_LEVEL
from utils.log import create_logger
from .history import History


class Agent(object):
    """Agent of QLearing."""

    agents_n = 0

    def __init__(self, game_cls):
        """Create an agent given a game class."""

        self.number = Agent.agents_n
        Agent.agents_n += 1

        self.states = game_cls.states
        self.actions = game_cls.actions
        self.action_size = len(self.actions)

        self.qvalues = [
            [0 for action in self.actions]
            for state in self.states
        ]
        self.cumul_reward = 0
        self.history = History(10)

        self.discount_rate = 0.95
        self.learning_rate = 0.001
        self.exploration_rate = 1
        self.exploration_decay = 0.995
        self.exploration_min = 0.01

        self.log = create_logger(str(self), log_level=LOG_LEVEL)

    def update(self, experience):
        """Update agent given an experience.

        Args:
            experience (qlearning.experience.Experience)
        """
        self.log.debug("Updating %s with %s.", self, experience)
        self.qupdate(experience)
        self.exploration_rate = max(
            self.exploration_rate * self.exploration_decay,
            self.exploration_min
        )

    def pick_action(self, state):
        """Return an action given a state.

        Compromise between qvalue and exploration rate.
        """
        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)
        else:
            return self.predict(state)

    def predict(self, state):
        """Return best action given the current qvalue."""
        values = self.qvalues[state]
        return values.index(max(values))

    def qupdate(self, experience):
        """Update qvalue given an experience.

        Args:
            experience (qlearning.experience.Experience)
        """
        exp = experience
        self.cumul_reward += exp.reward
        next_action = self.predict(exp.next_state)
        update = (
            self.learning_rate * (
                exp.reward
                + (
                    self.discount_rate
                    * self.qvalues[exp.next_state][next_action]
                )
                - self.qvalues[exp.state][exp.action]
            )
        )
        self.qvalues[exp.state][exp.action] += update
        self.history.append(exp)

    def __str__(self):
        return "Agent%s" % self.number
