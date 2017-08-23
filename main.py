import os
from datetime import datetime

from games.tictactoe import TTT
from qlearning.agent import Agent
from qlearning.environment import OldEnvironment
from qlearning.experience import Experience
from parameters import RESULT_DIR


def play_game(env, agents):
    """Play a game between the 2 agents, and learn from the game."""

    history = {0: {}, 1: {}}
    game_rewards = {0: 0, 1: 0}
    while not env.game.is_over():
        for player_n, agent in agents.items():
            if history[player_n]:
                exp = Experience(
                    state=history[player_n]['state'],
                    action=history[player_n]['action'],
                    reward=history[player_n]['reward'],
                    next_state=env.state(),
                )
                agent.update_qvalue(exp)
            state = env.state()
            action = agent.pick_action(state)
            rewards = env.act(action, agent.number)

            game_rewards[0] += rewards[0]
            game_rewards[1] += rewards[1]

            history[player_n] = {
                'state': state,
                'action': action,
                'reward': rewards[player_n],
            }

            other_player = 1 - player_n
            if history[other_player]:
                history[other_player]['reward'] += rewards[other_player]

    state = env.state()
    for player_n, hist in history.items():
        if hist:
            exp = Experience(
                state=hist['state'],
                action=hist['action'],
                reward=hist['reward'],
                next_state=env.state(),
            )
            agents[player_n].update_qvalue(exp)

    for agent in agents.values():
        agent.update_params()

    return game_rewards


def main(iterations, load_dir, params):
    """Play games to teach 2 agents how to play."""

    # Create agents and list of cumulated rewards
    if load_dir:
        agents = {
            0: Agent(TTT, params=params),
            1: Agent(TTT, params=params),
        }
        agents[0].load(os.path.join(load_dir, "0"))
        agents[1].load(os.path.join(load_dir, "1"))
    else:
        agents = {
            0: Agent(TTT, params=params),
            1: Agent(TTT, params=params),
        }
    rewards_per_game = {0: [], 1: []}
    total_rewards = {0: [], 1: []}

    # OldEnvironment for learning
    env = OldEnvironment(
        TTT,
        rewards={
            'tie': 3,
            'win': 10,
            'lose': -10,
            'invalid': -20,
            'neutral': 0
        },
    )

    # Iterations
    try:
        for i in range(iterations):
            env.reset()
            print("\r%s / %s" % (i+1, iterations), end="")
            game_rewards = play_game(env, agents)
            for player_n in [0, 1]:
                rewards_per_game[player_n].append(game_rewards[player_n])
                total_rewards[player_n].append(
                    agents[player_n].extras['cumul_reward']
                )
    except KeyboardInterrupt:
        pass
    print()

    # Save agents
    date_str = "{:%Y-%m-%dT%HH%M}".format(datetime.now())
    directory = os.path.join(RESULT_DIR, date_str)
    for agent_n, agent in agents.items():
        agent.save(os.path.join(directory, str(agent_n)))

    # ----------------------------------------------------------------------- #
    # Plot

    # Display cumulated rewards
    import matplotlib.pyplot as plt
    plt.plot(rewards_per_game[0], label="GameReward_%s" % agents[0])
    plt.plot(rewards_per_game[1], label="GameReward_%s" % agents[1])
    plt.legend()
    plt.show()

    plt.plot(total_rewards[0], label="CumulReward_%s" % agents[0])
    plt.plot(total_rewards[1], label="CumulReward_%s" % agents[1])
    plt.legend()
    plt.show()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("Train two agents on TicTacToe.")
    parser.add_argument(
        "-i", "--iterations", type=int, required=False, default=1000,
        help="Number of iterations."
    )
    parser.add_argument(
        "-l", "--load_dir", type=str, required=False, default=None,
        help="Directory from where to load agents, optional."
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
    main(iterations=args.iterations, load_dir=args.load_dir, params=params)
