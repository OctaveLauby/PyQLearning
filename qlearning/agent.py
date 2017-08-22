import json
import numpy as np
import os
import pickle
import random

from parameters import LOG_LEVEL
from utils.log import create_logger
from .history import History


QVALUES_FILE = "qvalues.pkl"
PARAMS_FILE = "params.json"
EXTRAS_FILE = "extras.json"


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
        self.extras = {
            'cumul_reward': 0,
            'updates_n': 0,
        }
        self.history = History(10)

        self.params = {
            'discount_rate': 0.95,
            'learning_rate': 0.001,
            'exploration_rate': 1,
            'exploration_decay': 0.995,
            'exploration_min': 0.01,
        }

        self.log = create_logger(str(self), log_level=LOG_LEVEL)

    def set_extras(self, **extras):
        self.extras.update(extras)

    def set_qvalues(self, qvalues):
        assert len(qvalues) == len(self.qvalues)
        assert len(qvalues[0]) == len(self.qvalues[0])
        self.qvalues = qvalues

    def set_params(self, **params):
        self.params.update(params)

    def pick_action(self, state):
        """Return an action given a state.

        Compromise between qvalue and exploration rate.
        """
        if np.random.rand() <= self.params['exploration_rate']:
            return random.randrange(self.action_size)
        else:
            return self.predict(state)

    def predict(self, state):
        """Return best action given the current qvalue."""
        values = self.qvalues[state]
        return values.index(max(values))

    def update_params(self):
        self.extras['cumul_reward'] += self.history.total_reward()
        self.extras['updates_n'] += 1
        self.history.clean()
        self.params['exploration_rate'] = max(
            self.params['exploration_rate'] * self.params['exploration_decay'],
            self.params['exploration_min']
        )

    def update_qvalue(self, experience):
        """Update qvalue given an experience.

        Args:
            experience (qlearning.experience.Experience)
        """
        self.log.debug("Updating qvalue with %s.", experience)
        exp = experience
        next_action = self.predict(exp.next_state)
        update = (
            self.params['learning_rate'] * (
                exp.reward
                + (
                    self.params['discount_rate']
                    * self.qvalues[exp.next_state][next_action]
                )
                - self.qvalues[exp.state][exp.action]
            )
        )
        self.qvalues[exp.state][exp.action] += update
        self.history.append(exp)

    def load(self, directory):
        """Load agent from directory."""
        path = os.path.join(directory, QVALUES_FILE)
        self.log.info("Loading qvalues at '%s'", path)
        with open(path, "rb") as file:
            qvalues = pickle.load(file)
        self.set_qvalues(qvalues)

        path = os.path.join(directory, PARAMS_FILE)
        self.log.info("Loading params at '%s'", path)
        with open(path) as file:
            params = json.load(file)
        self.set_params(**params)

        path = os.path.join(directory, EXTRAS_FILE)
        self.log.info("Loading params at '%s'", path)
        with open(path) as file:
            extras = json.load(file)
        self.set_extras(**extras)

    def save(self, directory):
        """Save agent to directory."""
        if directory and not os.path.exists(directory):
            self.log.info("Creating directory '%s'", directory)
            os.makedirs(directory)

        path = os.path.join(directory, QVALUES_FILE)
        self.log.info("Saving qvalues at '%s'", path)
        with open(path, "wb") as file:
            pickle.dump(self.qvalues, file)

        path = os.path.join(directory, PARAMS_FILE)
        self.log.info("Saving params at '%s'", path)
        with open(path, "w") as file:
            json.dump(self.params, file)

        path = os.path.join(directory, EXTRAS_FILE)
        self.log.info("Saving extras at '%s'", path)
        with open(path, "w") as file:
            json.dump(self.extras, file)

    def __str__(self):
        return "Agent%s" % self.number
