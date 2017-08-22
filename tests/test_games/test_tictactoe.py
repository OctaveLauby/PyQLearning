import pytest

from games.tictactoe import states_filter, TTT
from games.exceptions import GameOver, InvalidPlay, InvalidPlayer


def test_states_filter():

    # Okay
    assert states_filter((-1, -1, -1, -1, -1, -1, -1, -1, -1)) is True
    assert states_filter((0, 0, -1, -1, -1, -1, -1, -1, 1)) is True
    assert states_filter((0, 1, 0, 1, 0, 1, -1, -1, -1)) is True

    # Too much
    assert states_filter((0, 0, 0, 1, -1, -1, -1, -1, -1)) is False
    assert states_filter((0, 0, 1, 1, 1, -1, -1, -1, -1)) is False

    # Double winner
    assert states_filter((0, 0, 0, 1, 1, 1, -1, -1, -1)) is False
    assert states_filter((-1, -1, -1, 1, 1, 1, 0, 0, 0)) is False
    assert states_filter((0, 1, -1, 0, 1, -1, 0, 1, -1)) is False
    assert states_filter((-1, 1, 0, -1, 1, 0, -1, 1, 0)) is False


def test_TTT():

    # ----------------------------------------------------------------------- #
    # Player 0 wins

    game = TTT()
    states = TTT.states

    assert len(states) == 5890
    assert states[game.state()] == (-1, -1, -1, -1, -1, -1, -1, -1, -1)

    # Wrong starter
    with pytest.raises(InvalidPlayer):
        game.act(0, 1)

    game.act(0, 0)
    game.act(1, 1)
    game.act(3, 0)

    # Wrong player
    with pytest.raises(InvalidPlayer):
        game.act(2, 0)

    # Playing when already played
    with pytest.raises(InvalidPlay):
        game.act(0, 1)

    assert states[game.state()] == (0, 1, -1, 0, -1, -1, -1, -1, -1)

    game.act(2, 1)
    game.act(6, 0)

    # Game over
    with pytest.raises(GameOver):
        game.act(4, 1)

    assert states[game.state()] == (0, 1, 1, 0, -1, -1, 0, -1, -1)
    assert game.winner.number == 0

    assert game.string() == (
        " X | O | O \n"
        "---+---+---\n"
        " X |   |   \n"
        "---+---+---\n"
        " X |   |   "
    )

    # ----------------------------------------------------------------------- #
    # Tie Game
    game = TTT()

    game.act(0, 0)
    game.act(1, 1)
    game.act(2, 0)
    game.act(4, 1)
    game.act(3, 0)
    game.act(6, 1)
    game.act(5, 0)
    game.act(8, 1)
    game.act(7, 0)
    assert game.is_over()
    assert game.winner is None

    # ----------------------------------------------------------------------- #
    # Double win

    # ---- Diag

    game = TTT()
    game.act(0, 0)
    game.act(1, 1)
    game.act(2, 0)
    game.act(7, 1)
    game.act(8, 0)
    game.act(5, 1)
    game.act(6, 0)
    game.act(3, 1)
    game.act(4, 0)

    assert states[game.state()] == (0, 1, 0, 1, 0, 1, 0, 1, 0)
    assert game.string() == (
        " X | O | X \n"
        "---+---+---\n"
        " O | X | O \n"
        "---+---+---\n"
        " X | O | X "
    )

    # ---- Col row
    # Make sure exists
    game.state_index((0, 0, 0, 0, 1, 1, 0, 1, 1))

    # ---- Diff Color
    with pytest.raises(ValueError):
        game.state_index((0, 0, 0, 1, 1, 1, -1, -1, -1))

    with pytest.raises(ValueError):
        game.state_index((0, 1, -1, 0, 1, -1, 0, 1, -1))
