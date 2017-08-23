import games.exceptions as exc
import games.nkgame as nkgame
import pytest


# # Indexes: n=3 Case
# 0 1 2
# 3 4 5
# 6 7 8

# # Indexes: n=4 Case
# 0  1  2  3
# 4  5  6  7
# 8  9  10 11
# 12 13 14 15


def test_build_diags():

    assert nkgame.build_diags(3, 3) == [
        [0, 4, 8], [2, 4, 6]
    ]

    assert nkgame.build_diags(4, 3) == [
        [0, 5, 10, 15],
        [1, 6, 11],
        [4, 9, 14],
        [2, 5, 8],
        [3, 6, 9, 12],
        [7, 10, 13],
    ]


def test_winners():

    assert nkgame.winners([0, 1, 1, 0, None, 0, 0, 0, 1, 1, None], 2) == {
        1, 0
    }

    assert nkgame.winners([None, 0, 0, 0], 3) == {0}
    assert nkgame.winners([0, 0, 0, None], 3) == {0}


def test_NKGame():

    # ---- 4, 4

    game = nkgame.NKGame(4, 3)
    assert game.indexes == {
        'row': [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15],
        ],
        'col': [
            [0, 4, 8, 12],
            [1, 5, 9, 13],
            [2, 6, 10, 14],
            [3, 7, 11, 15],
        ],
        'diag': [
            [0, 5, 10, 15],
            [1, 6, 11],
            [4, 9, 14],
            [2, 5, 8],
            [3, 6, 9, 12],
            [7, 10, 13],
        ],
    }
    assert game.symbols() == [
        [" " for j in range(4)]
        for i in range(4)
    ]
    assert game.string() == (
        "   |   |   |   \n"
        "---+---+---+---\n"
        "   |   |   |   \n"
        "---+---+---+---\n"
        "   |   |   |   \n"
        "---+---+---+---\n"
        "   |   |   |   "
    )

    game.act(1, 0)

    with pytest.raises(exc.InvalidPlayer):
        game.act(2, 0)

    with pytest.raises(exc.InvalidPlay):
        game.act(1, 1)

    game.act(14, 1)
    game.act(2, 0)
    game.act(15, 1)
    game.act(3, 0)

    with pytest.raises(exc.GameOver):
        game.act(0, 1)

    assert game.string() == (
        "   | 0 | 0 | 0 \n"
        "---+---+---+---\n"
        "   |   |   |   \n"
        "---+---+---+---\n"
        "   |   |   |   \n"
        "---+---+---+---\n"
        "   |   | 1 | 1 "
    )

    # ----------------------------------------------------------------------- #
    # ---- 3, 3

    game = nkgame.NKGame(3, 3)

    assert game.state() == (
        None, None, None, None, None, None, None, None, None
    )

    # Wrong starter
    with pytest.raises(exc.InvalidPlayer):
        game.act(0, 1)

    game.act(0, 0)
    game.act(1, 1)
    game.act(3, 0)

    # Wrong player
    with pytest.raises(exc.InvalidPlayer):
        game.act(2, 0)

    # Playing when already played
    with pytest.raises(exc.InvalidPlay):
        game.act(0, 1)

    assert game.state() == (0, 1, None, 0, None, None, None, None, None)

    game.act(2, 1)
    game.act(6, 0)

    # Game over
    with pytest.raises(exc.GameOver):
        game.act(4, 1)

    assert game.state() == (0, 1, 1, 0, None, None, 0, None, None)
    assert game.winner == 0

    assert game.string() == (
        " 0 | 1 | 1 \n"
        "---+---+---\n"
        " 0 |   |   \n"
        "---+---+---\n"
        " 0 |   |   "
    )

    # ---- Tie Game
    game.reset()

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

    # ---- Double win

    # Diag

    game.reset()
    game.act(0, 0)
    game.act(1, 1)
    game.act(2, 0)
    game.act(7, 1)
    game.act(8, 0)
    game.act(5, 1)
    game.act(6, 0)
    game.act(3, 1)
    game.act(4, 0)

    assert game.state() == (0, 1, 0, 1, 0, 1, 0, 1, 0)
    assert game.string() == (
        " 0 | 1 | 0 \n"
        "---+---+---\n"
        " 1 | 0 | 1 \n"
        "---+---+---\n"
        " 0 | 1 | 0 "
    )
    assert game.winner == 0
