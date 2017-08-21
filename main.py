from games.common import InvalidPlay
from games.tictactoe import TTT
from qlearning.agent import Agent
from qlearning.experience import Experience


def play_game(game, agent0, agent1):
    agent = agent0
    previous = {}
    current = {}
    while not game.is_over():
        current = {}
        current['state'] = game.state()
        current['action'] = agent.pick_action(current['state'])
        try:
            current['reward'] = game.act(current['action'], agent.number)
        except InvalidPlay:
            current['reward'] = -10
            break

        agent = agent0 if agent == agent1 else agent1
        if previous:
            exp = Experience(
                state=previous['state'],
                action=previous['action'],
                reward=previous['reward'] - current['reward'],
                next_state=current['state'],
            )
            agent.update(exp)

        previous.update(current)

    other_agent = agent0 if agent == agent1 else agent1
    if current:
        exp = Experience(
            state=current['state'],
            action=current['action'],
            reward=current['reward'],
            next_state=game.state(),
        )
        other_agent.update(exp)


if __name__ == "__main__":
    agent0 = Agent(TTT)
    agent1 = Agent(TTT)
    rewards0 = []
    rewards1 = []
    iterations = 100000

    try:
        for i in range(iterations):
            print("\r%s / %s" % (i, iterations), end="")
            play_game(TTT(), agent0, agent1)
            rewards0.append(agent0.cumul_reward)
            rewards1.append(agent1.cumul_reward)
    except KeyboardInterrupt:
        pass

    import matplotlib.pyplot as plt
    plt.plot(rewards0, label="Creward_%s" % agent0)
    plt.plot(rewards1, label="Creward_%s" % agent1)
    plt.legend()
    plt.show()
