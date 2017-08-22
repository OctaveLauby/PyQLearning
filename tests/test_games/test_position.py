from games.position import Position


def test_Position():

    assert Position(0) == Position(0, 0)
    assert Position(1) == Position(1, 0)
    assert Position(2) == Position(2, 0)
    assert Position(3) == Position(0, 1)
    assert Position(4) == Position(1, 1)
    assert Position(5) == Position(2, 1)
    assert Position(6) == Position(0, 2)
    assert Position(7) == Position(1, 2)
    assert Position(8) == Position(2, 2)

    assert str(Position(3)) == "Position(0, 1)"
