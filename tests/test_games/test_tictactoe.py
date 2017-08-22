import pytest

from games.tictactoe import TTT
from games.exceptions import GameOver, InvalidPlay, InvalidPlayer


def test_TTT():

    # ----------------------------------------------------------------------- #
    # Player 0 wins

    game = TTT()
    states = TTT.states

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
