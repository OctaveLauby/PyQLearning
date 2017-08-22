from games.tictactoe import TTT
from qlearning.agent import Agent
from qlearning.environment import Environment
from qlearning.experience import Experience


def play_game(env, agents):
    """Play a game between the 2 agents, and learn from the game."""

    history = {0: {}, 1: {}}
    while not env.game.is_over():
        for player_n, agent in agents.items():
            if history[player_n]:
                exp = Experience(
                    state=history[player_n]['state'],
                    action=history[player_n]['action'],
                    reward=history[player_n]['reward'],
                    next_state=env.state(),
                )
                agent.update(exp)
            state = env.state()
            action = agent.pick_action(state)
            rewards = env.act(action, agent.number)

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
            agents[player_n].update(exp)


def main(iterations):
    """Play games to teach 2 agents how to play."""

    # Create agents and list of cumulated rewards
    agents = {
        0: Agent(TTT),
        1: Agent(TTT),
    }
    rewards = {0: [], 1: []}

    # Environment for learning
    env = Environment(
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
            play_game(env, agents)
            for reward_l, agent in zip(rewards.values(), agents.values()):
                reward_l.append(agent.cumul_reward)
    except KeyboardInterrupt:
        pass

    # Display cumulated rewards
    import matplotlib.pyplot as plt
    plt.plot(rewards[0], label="Creward_%s" % agents[0])
    plt.plot(rewards[1], label="Creward_%s" % agents[1])
    plt.legend()
    plt.show()


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("Train two agents on TicTacToe.")
    parser.add_argument(
        "-i", "--iterations", type=int, required=False, default=1000,
        help="Number of iterations."
    )
    args = parser.parse_args()
    main(args.iterations)
