import json
import numpy as np
import os
import pickle
import random

from parameters import LOG_LEVEL, INVALID_REWARD
from utils.log import create_logger
from .history import History
from .experience import Experience


KWARGS_FILE = "kwargs.json"
QVALUES_FILE = "qvalues.pkl"
PARAMS_FILE = "params.json"
EXTRAS_FILE = "extras.json"


class QLearner(object):
    """QLearner of QLearing."""

    agents_n = 0
    params = {
        'discount_rate': 0.95,
        'learning_rate': 0.001,
        'exploration_rate': 1.,
        'exploration_decay': 0.995,
        'exploration_min': 0.01,
        'hist_size': 10,
    }

    def __init__(self, name, actions, params={}):
        """Create an agent given a game class.

        Args:
            params (dict):
                discount_rate       default is 0.95
                learning_rate       default is 0.001
                exploration_rate    default is 1
                exploration_decay   default is 0.995
                exploration_min     default is 0.01

        """
        self.name = name
        self.log = create_logger(str(self), log_level=LOG_LEVEL)

        self.kwargs = {
            'name': name,
            'actions': actions,
        }
        self.log.info("Created with kwargs: %s.", self.kwargs)

        self.actions = actions
        self.action_size = len(self.actions)

        self.default_sqvalue = [0 for action in self.actions]
        self.qvalues = {
            # # Dict of (state, list_of_qvalues)
            # Where list_of_qvalues_i if qvalue for actions_i
        }

        self.init_params(params)

        self.last_action = None
        self.last_state = None
        self.hist = History(self.params['hist_size'])

        # More info
        self.extras = {
            'cls': self.__class__.__name__,
            'or_params': dict(self.params),
            'iterations': 0,
        }

    # ----------------------------------------------------------------------- #
    # Set, Get

    def init_qvalues(self, qvalues):
        self.qvalues = {}
        self.qvalues.update(qvalues)

    def init_params(self, params):
        self.params = dict(QLearner.params)
        self.params.update(params)
        self.log.info("Initialized with params: %s.", self.params)

    def get_qvalue(self, state, action):
        """Return qvalue(state, action)."""
        return self.get_state_qvals(state)[action]

    def get_state_qvals(self, state):
        """Return qvalues for state."""
        return self.qvalues.get(state, self.default_sqvalue)

    def set_qvalue(self, state, action, value):
        """Set qvalue(sate, action)."""
        self.log.debug(
            "Set qvalue(%s, %s) with %s"
            % (state, action, value)
        )
        if state not in self.qvalues:
            self.qvalues[state] = list(self.default_sqvalue)
        self.qvalues[state][action] = value

    def increment_qvalue(self, state, action, value):
        """Set qvalue(sate, action)."""
        self.log.debug(
            "Increment qvalue(%s, %s) with %s"
            % (state, action, value)
        )
        if state not in self.qvalues:
            self.qvalues[state] = list(self.default_sqvalue)
        self.qvalues[state][action] += value

    # ----------------------------------------------------------------------- #
    # Actions

    def pick_action(self, state):
        """Return an action given a state.

        Compromise between qvalue and exploration rate.
        """
        if np.random.rand() <= self.params['exploration_rate']:
            # Pick within possible actions
            action = random.choice([
                action_i
                for action_i, qvalue in enumerate(self.get_state_qvals(state))
                if qvalue != INVALID_REWARD
            ])
        else:
            action = self.predict(state)
        self.last_action = action
        self.last_state = state
        return action

    def predict(self, state):
        """Return best action given the current qvalue."""
        values = self.get_state_qvals(state)
        return values.index(max(values))

    # ----------------------------------------------------------------------- #
    # Learning

    def punish(self, state, action):
        self.set_qvalue(state, action, INVALID_REWARD)

    def reward(self, reward, new_state):
        """Reward QLearner for last action he took."""
        if reward == INVALID_REWARD:
            self.log.debug(
                "Learning invalid move %s when state is %s"
                % (self.last_action, self.last_state)
            )
            self.set_qvalue(self.last_state, self.last_action, INVALID_REWARD)
            return

        if self.last_state is None or self.last_action is None:
            self.log.debug(
                "Receiving reward when no previous action was taken"
            )
            return

        experience = Experience(
            state=self.last_state,
            action=self.last_action,
            reward=reward,
            next_state=new_state,
        )

        if self.hist.is_full():
            self.learn()
        else:
            self.hist.append(experience)

    def learn(self):
        """Learn from history."""
        self.log.debug("Learning from history (len is %s)" % len(self.hist))
        while not self.hist.is_empty():
            experience = self.hist.pop()
            self.learn_exp(experience)

    def learn_exp(self, exp):
        """Learn from experience

        Args:
            exp (qlearning.experience.Experience)
        """
        self.log.debug("Updating qvalue with %s.", exp)

        # Gather informations
        current_qvalue = self.get_qvalue(exp.state, exp.action)
        next_action = self.predict(exp.next_state)
        next_qvalue = self.get_qvalue(exp.next_state, next_action)

        # Update
        update = (
            self.params['learning_rate'] * (
                exp.reward
                + (
                    self.params['discount_rate']
                    * next_qvalue
                )
                - current_qvalue
            )
        )
        self.increment_qvalue(exp.state, exp.action, update)

    def update(self):
        self.extras['iterations'] += 1
        self.learn()
        self.params['exploration_rate'] = max(
            self.params['exploration_rate'] * self.params['exploration_decay'],
            self.params['exploration_min']
        )

    # ----------------------------------------------------------------------- #
    # Load / Save

    @ staticmethod
    def load(directory):
        """Load agent from directory."""
        path = os.path.join(directory, KWARGS_FILE)
        with open(path) as file:
            kwargs = json.load(file)

        path = os.path.join(directory, PARAMS_FILE)
        with open(path) as file:
            kwargs['params'] = json.load(file)

        qlearner = QLearner(**kwargs)

        path = os.path.join(directory, QVALUES_FILE)
        qlearner.log.info("Loading qvalues at '%s'", path)
        with open(path, "rb") as file:
            qvalues = pickle.load(file)
        qlearner.init_qvalues(qvalues)

        path = os.path.join(directory, EXTRAS_FILE)
        qlearner.log.info("Saving extras at '%s'", path)
        with open(path) as file:
            extras = json.load(file)
        qlearner.extras = extras

        return qlearner

    def save(self, directory):
        """Save agent to directory."""
        if directory and not os.path.exists(directory):
            self.log.info("Creating directory '%s'", directory)
            os.makedirs(directory)

        path = os.path.join(directory, KWARGS_FILE)
        self.log.info("Saving kwargs at '%s'", path)
        with open(path, "w") as file:
            json.dump(self.kwargs, file)

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
        return "QLearner(%s)" % self.name
