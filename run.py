import os
from datetime import datetime

from games.nkgame import NKGame
from qlearning.qlearner import QLearner
from qlearning.environment import Environment
from parameters import RESULT_DIR


def main(game, iterations, params):
    """Play games to teach 2 agents how to play."""

    # OldEnvironment for learning
    env = Environment(
        game,
        rewards={
            'tie': 3,
            'win': 10,
            'lose': -10,
            'invalid': -20,
            'neutral': 0
        },
        qlearner_kwargs={'params': params}
    )

    # Iterations
    try:
        env.train(iterations)
    except KeyboardInterrupt:
        pass
    print()

    # Save environment
    date_str = "{:%Y-%m-%dT%HH%M}".format(datetime.now())
    directory = os.path.join(RESULT_DIR, date_str)
    env.save(directory)

    # ----------------------------------------------------------------------- #
    # Plot

    # Display cumulated rewards
    env.plot_hist()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("Train two agents on TicTacToe.")
    parser.add_argument(
        "-i", "--iterations", type=int, required=False, default=1000,
        help="Number of iterations, default is 1000."
    )
    parser.add_argument(
        "-n", "--size", type=int, required=False, default=3,
        help="Size of game, default is 3."
    )
    parser.add_argument(
        "-k", "--wincase", type=int, required=False, default=3,
        help="Number of successive cells to win, default is 3."
    )
    for key, default in QLearner.params.items():
        parser.add_argument(
            "--%s" % key, type=type(default),
            required=False, default=default,
            help="%s, default is %s." % (key.replace("_", " "), default)
        )
    args = parser.parse_args()
    params = {
        key: eval("args.%s" % key)
        for key in QLearner.params
    }
    game = NKGame(args.size, args.wincase)
    main(game=game, iterations=args.iterations, params=params)
