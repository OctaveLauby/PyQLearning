import os
from datetime import datetime

from games.nkgame import NKGame
from qlearning.agent import Agent
from qlearning.environment import Environment
from parameters import RESULT_DIR


def main(iterations, params):
    """Play games to teach 2 agents how to play."""

    # OldEnvironment for learning
    env = Environment(
        NKGame(3, 3),
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

    # Save agents
    date_str = "{:%Y-%m-%dT%HH%M}".format(datetime.now())
    directory = os.path.join(RESULT_DIR, date_str)
    env.save_agents(directory)

    # ----------------------------------------------------------------------- #
    # Plot

    # Display cumulated rewards
    env.plot_hist()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("Train two agents on TicTacToe.")
    parser.add_argument(
        "-i", "--iterations", type=int, required=False, default=1000,
        help="Number of iterations."
    )
    for key, default in Agent.params.items():
        parser.add_argument(
            "--%s" % key, type=type(default),
            required=False, default=default,
            help="%s, default is %s." % (key.replace("_", " "), default)
        )
    args = parser.parse_args()
    params = {
        key: eval("args.%s" % key)
        for key in Agent.params
    }
    main(iterations=args.iterations, params=params)
