from games.tictactoe import TTT
from qlearning.environment import Environment


def test_Environment():

    tie = 5
    win = 8
    lose = -10
    invalid = -50
    neutral = 2

    rewards = rewards = {
        'tie': tie,
        'win': win,
        'lose': lose,
        'invalid': invalid,
        'neutral': neutral,
    }

    env = Environment(TTT, rewards=rewards)

    assert env.act(0, 0) == {
        0: neutral,
        1: 0,
    }
    assert env.act(0, 0) == {
        0: 0,
        1: 0,
    }
    assert env.act(0, 1) == {
        0: 0,
        1: invalid,
    }
    assert env.act(1, 1) == {
        0: 0,
        1: neutral,
    }
    assert env.act(3, 0) == {
        0: neutral,
        1: 0,
    }
    assert env.act(2, 1) == {
        0: 0,
        1: neutral,
    }
    assert env.act(6, 0) == {
        0: win,
        1: lose,
    }
    assert env.act(2, 1) == {
        0: 0,
        1: 0,
    }

    env.reset()
    assert env.act(0, 0) == {
        0: neutral,
        1: 0,
    }
    assert env.act(1, 1) == {
        0: 0,
        1: neutral,
    }
    assert env.act(2, 0) == {
        0: neutral,
        1: 0,
    }
    assert env.act(4, 1) == {
        0: 0,
        1: neutral,
    }
    assert env.act(3, 0) == {
        0: neutral,
        1: 0,
    }
    assert env.act(6, 1) == {
        0: 0,
        1: neutral,
    }
    assert env.act(5, 0) == {
        0: neutral,
        1: 0,
    }
    assert env.act(8, 1) == {
        0: 0,
        1: neutral,
    }
    assert env.act(7, 0) == {
        0: tie,
        1: tie,
    }
