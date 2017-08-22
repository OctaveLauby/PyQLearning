from games.tictactoe import TTT
from qlearning.agent import Agent
from qlearning.environment import Environment
from qlearning.experience import Experience


def play_game(env, agents):

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


if __name__ == "__main__":
    agents = {
        0: Agent(TTT),
        1: Agent(TTT),
    }
    rewards = {0: [], 1: []}

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

    iterations = 1000
    try:
        for i in range(iterations):
            env.reset()
            print("\r%s / %s" % (i, iterations), end="")
            play_game(env, agents)
            for reward_l, agent in zip(rewards.values(), agents.values()):
                reward_l.append(agent.cumul_reward)
    except KeyboardInterrupt:
        pass

    import matplotlib.pyplot as plt
    plt.plot(rewards[0], label="Creward_%s" % agents[0])
    plt.plot(rewards[1], label="Creward_%s" % agents[1])
    plt.legend()
    plt.show()
