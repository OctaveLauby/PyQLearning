import matplotlib.pyplot as plt
import os

from games.exceptions import GameOver, InvalidPlay, InvalidPlayer
from parameters import INVALID_REWARD, LOG_LEVEL
from utils.log import create_logger
from .qlearner import QLearner


class Environment(object):

    rewards = {
        'tie': 3,
        'win': 10,
        'lose': -10,
        'neutral': 0,
        'invalid': -20,
    }

    def __init__(self, game, rewards, qlearner_kwargs={}):
        """Create an environnemnt for training.

        Args:
            game (games.game.Game)
            rewards (dict): @see Environment.rewards
        """
        self.log = create_logger(self.__class__.__name__, LOG_LEVEL)
        self.game = game

        # History
        self.hist = {
            'rewards_per_game': {0: [], 1: []},
            'cumulated_rewards': {0: [], 1: []},
        }

        # Rewards
        self.rewards = dict(OldEnvironment.rewards)
        if rewards:
            self.rewards.update(rewards)
        self.log.info("Playing %s with %s." % (game, self.rewards))

        # Agents
        actions = game.actions_all()
        self.agents = {
            0: QLearner("player_0", actions, **qlearner_kwargs),
            1: QLearner("player_1", actions, **qlearner_kwargs),
        }

    def play_game(self):
        self.game.reset()

        game_rewards = {
            0: 0, 1: 0
        }

        # Playing game
        while not self.game.is_over():
            player = self.game.player_n
            action = self.agents[player].pick_action(self.game.state())
            try:
                self.game.act(action, player)
            except InvalidPlay:
                self.agents[player].reward(INVALID_REWARD, None)
                game_rewards[player] += self.rewards['invalid']
            else:
                player = 1 - player
                if not self.game.is_over():
                    self.agents[player].reward(
                        self.rewards['neutral'], self.game.state()
                    )
                    game_rewards[player] += self.rewards['neutral']

        # Final rewards
        winner = self.game.winner
        state = self.game.state()
        for player in [0, 1]:
            if winner is None:
                self.agents[player].reward(self.rewards['tie'], state)
                game_rewards[player] += self.rewards['tie']
            elif player == winner:
                self.agents[player].reward(self.rewards['win'], state)
                game_rewards[player] += self.rewards['win']
            else:
                self.agents[player].reward(self.rewards['lose'], state)
                game_rewards[player] += self.rewards['lose']
            self.agents[player].update()

        for player, reward in game_rewards.items():
            self.hist['rewards_per_game'][player].append(reward)
            cumulated_rewards = self.hist['cumulated_rewards'][player]
            previous_cumul = (
                0 if len(cumulated_rewards) == 0 else cumulated_rewards[-1]
            )
            cumulated_rewards.append(previous_cumul + reward)

        return game_rewards

    def train(self, iterations):
        for i in range(iterations):
            print("\r%s / %s" % (i+1, iterations), end="")
            self.play_game()

    # ----------------------------------------------------------------------- #
    # Utils

    def plot_hist(self):
        plt.plot(
            self.hist['rewards_per_game'][0],
            label="GameReward_%s" % self.agents[0]
        )
        plt.plot(
            self.hist['rewards_per_game'][1],
            label="GameReward_%s" % self.agents[1]
        )
        plt.legend()
        plt.show()

        plt.plot(
            self.hist['cumulated_rewards'][0],
            label="CumulReward_%s" % self.agents[0]
        )
        plt.plot(
            self.hist['cumulated_rewards'][1],
            label="CumulReward_%s" % self.agents[1]
        )
        plt.legend()
        plt.show()

    def save(self, directory):
        self.save_agents(directory)
        self.save_game(
            os.path.join(directory, "game")
        )

    def save_agents(self, directory):
        for agent_n, agent in self.agents.items():
            agent.save(os.path.join(directory, str(agent_n)))

    def save_game(self, directory):
        self.game.save(directory)


class OldEnvironment(object):
    """OldEnvironment for learning."""

    rewards = {
        'tie': 3,
        'win': 10,
        'lose': -10,
        'invalid': -20,
        'neutral': 0
    }

    def __init__(self, game_cls, rewards=None):
        """Create an environnemnt given a game class.

        Args:
            game_cls (cls of games.game.Game)
            rewards (dict): @see OldEnvironment.rewards
        """
        self.log = create_logger(self.__class__.__name__, LOG_LEVEL)
        self.rewards = dict(OldEnvironment.rewards)
        if rewards:
            self.rewards.update(rewards)
        self.log.info(
            "Playing %s with %s."
            % (game_cls.__name__, self.rewards)
        )
        self.game_cls = game_cls
        self.game = game_cls()

    def state(self):
        """Return current state of game."""
        return self.game.state()

    def act(self, action_n, player_n):
        """Play action for player and return rewards of all players.

        Ignore InvalidPlayer and GameOver cases (returns 0 rewards)
        """
        rewards = {
            player.number: 0
            for player in self.game.players
        }

        try:
            self.game.act(action_n, player_n)
        except InvalidPlay:
            rewards[player_n] = self.rewards['invalid']
            return rewards
        except GameOver:
            return rewards
        except InvalidPlayer:
            return rewards

        # Update rewards
        rewards[player_n] = self.rewards['neutral']
        for player in self.game.players:
            if not self.game.is_over():
                pass
            elif self.game.winner is None:  # Tie game
                rewards[player.number] = self.rewards['tie']
            elif self.game.winner.number is player.number:
                rewards[player.number] = self.rewards['win']
            else:
                rewards[player.number] = self.rewards['lose']
        return rewards

    def reset(self):
        """Restart game."""
        self.game = self.game_cls()
