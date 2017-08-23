import pytest

import games.exceptions as exc
from games.nkgame import NKGame
from qlearning.qlearner import QLearner
from parameters import INVALID_REWARD


def test_QLearner():

    game = NKGame(3, 3)
    actions = game.actions_all()
    params = {
        'discount_rate': 1,
        'learning_rate': 0.1,
        'exploration_rate': 0,
        'exploration_decay': 0,
        'exploration_min': 0,
    }

    qlearners = {
        0: QLearner(
            name="player_0",
            actions=actions,
            hist_size=10,
            params=params
        ),
        1: QLearner(
            name="player_1",
            actions=actions,
            hist_size=10,
            params=params
        ),
    }

    assert str(qlearners[0]) == "QLearner(player_0)"
    assert str(qlearners[1]) == "QLearner(player_1)"

    player = 0
    while not game.is_over():
        action = qlearners[player].pick_action(game.state())
        try:
            game.act(action, player)
        except exc.InvalidPlay:
            qlearners[player].reward(INVALID_REWARD, None)
        else:
            player = 1 - player
            if not game.is_over():
                qlearners[player].reward(0, game.state())
    winner = game.winner
    for player in [0, 1]:
        if winner is None:
            qlearners[player].reward(0, game.state())
        elif player == winner:
            qlearners[player].reward(+1, game.state())
        else:
            qlearners[player].reward(-1, game.state())
        qlearners[player].update()
    game.display()

    assert qlearners[0].get_qvalue(
        (0, 1, 0, 1, 0, 1, None, None, None), 6
    ) == pytest.approx(0.1)
    assert qlearners[0].get_qvalue(
        (0, 1, 0, 1, None, None, None, None, None), 4
    ) == pytest.approx(0.01)
    assert qlearners[0].get_qvalue(
        (0, 1, None, None, None, None, None, None, None), 2
    ) == pytest.approx(0.001)
    assert qlearners[0].get_qvalue(
        (None, None, None, None, None, None, None, None, None), 0
    ) == pytest.approx(0.0001)
    assert qlearners[1].get_qvalue(
        (0, 1, 0, 1, 0, None, None, None, None), 5
    ) == pytest.approx(- 0.1)
    assert qlearners[1].get_qvalue(
        (0, 1, 0, None, None, None, None, None, None), 3
    ) == pytest.approx(0)
    assert qlearners[1].get_qvalue(
        (0, None, None, None, None, None, None, None, None), 1
    ) == pytest.approx(0)
