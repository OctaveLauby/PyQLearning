
from games.exceptions import GameOver, InvalidPlay, InvalidPlayer

from utils.log import create_logger
from parameters import LOG_LEVEL


class Environment(object):

    rewards = {
        'tie': 3,
        'win': 10,
        'lose': -10,
        'invalid': -20,
        'neutral': 0
    }

    def __init__(self, game_cls, rewards=None):
        self.log = create_logger(self.__class__.__name__, LOG_LEVEL)
        self.rewards = dict(Environment.rewards)
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
        self.game = self.game_cls()
