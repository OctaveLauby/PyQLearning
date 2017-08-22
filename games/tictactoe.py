from collections import defaultdict
from itertools import product

from parameters import LOG_LEVEL
from utils.list import are_same
from utils.log import create_logger
from .common import InvalidPlay, Position
from .game import Game


class Player(object):

    def __init__(self, number, symbol):
        self.symbol = symbol
        self.number = number

    def __hash__(self):
        # So we can use player as dictionary key
        return self.symbol.__hash__()

    def __str__(self):
        return "Player%s" % self.symbol

    def __repr__(self):
        return self.__str__()


class Cell(object):

    def __init__(self, i, j):
        self.content = None
        self.position = Position(i, j)

        self.log = create_logger(self.__class__.__name__, log_level=LOG_LEVEL)

    @property
    def symbol(self):
        if self.content is None:
            return " "
        else:
            return self.content.symbol

    @property
    def number(self):
        if self.content is None:
            return -1
        return self.content.number

    def is_empty(self):
        return self.content is None

    def play(self, player):
        if self.content:
            msg = (
                "Cell at %s already played by %s"
                % (self.position, self.content)
            )
            self.log.info(msg)
            raise InvalidPlay(msg)
        self.content = player

    def __eq__(self, other):
        return self.content == other.content

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.__str__()


def states_filter(state):
    """Return whether state is possible."""

    if state.count(0) < state.count(1) or state.count(1) < state.count(0) - 1:
        return False

    rows = [[i, i+1, i+2] for i in range(0, 3, 6)]
    cols = [[i, i+3, i+6] for i in range(0, 1, 2)]

    winner_cases = []

    for row_indexes in rows:
        row = [state[ind] for ind in row_indexes]
        if row[0] >= 0 and are_same(row):
            winner_cases.append(row_indexes)

    for col_indexes in cols:
        col = [state[ind] for ind in col_indexes]
        if col[0] >= 0 and are_same(col):
            winner_cases.append(col_indexes)

    diags = [
        [i + i * 3 for i in range(3)],
        [3 * i + (2 - i) for i in range(3)]
    ]
    for diag_indexes in diags:
        diag = [state[ind] for ind in diag_indexes]
        if diag[0] >= 0 and are_same(diag):
            winner_cases.append(diag_indexes)

    return len(winner_cases) <= 1


class TTT(Game):

    actions = list(range(9))
    states = list(filter(
        states_filter,
        product(
            *[[-1, 0, 1] for cell_n in range(9)]
        )
    ))

    def __init__(self):
        super().__init__()
        self.board = []
        for row in range(3):
            for col in range(3):
                self.board.append(Cell(row, col))
        self.history = defaultdict(list)
        self.winner = None
        self.ended = False
        self.players = [Player(0, "X"), Player(1, "O")]

        self.log = create_logger(self.__class__.__name__, log_level=LOG_LEVEL)

    def is_over(self):
        return self.ended

    def cell(self, *args):
        pos = Position(*args)
        return self.cells[pos.i + pos.j * 3]

    @property
    def cells(self):
        return self.board

    @property
    def cols(self):
        cols = [[], [], []]
        for row in range(3):
            for col in range(3):
                cols[col].append(self.cell(row, col))
        return cols

    @property
    def rows(self):
        rows = [[], [], []]
        for row in range(3):
            for col in range(3):
                rows[row].append(self.cell(row, col))
        return rows

    def check_end(self):
        winner_cell = None

        for row in self.rows:
            if not row[0].is_empty() and are_same(row):
                winner_cell = row[0]

        for col in self.cols:
            if not col[0].is_empty() and are_same(col):
                winner_cell = col[0]

        mid = self.cell(1, 1)
        if (
            not mid.is_empty()
            and (
                self.cell(0, 0) == mid == self.cell(2, 2)
                or self.cell(0, 2) == mid == self.cell(2, 0)
            )
        ):
            winner_cell = mid

        if winner_cell:
            self.ended = True
            self.winner = winner_cell.content
        else:
            self.ended = -1 not in map(lambda x: x.number, self.cells)

    def act(self, action_n, player_n):
        cell_n = self.cls.actions[action_n]
        player = self.players[player_n]
        if self.ended:
            self.ended = True
            self.log.error("Trying to play when game is over.")
            raise InvalidPlay("Game is Over")
        self.cells[cell_n].play(player)
        self.history[player].append(Position(cell_n))
        self.check_end()

        if self.ended:
            self.log.info("Game Over")
            if self.winner:
                self.log.info("%s wins !!!" % self.winner)

                if self.winner.number == player_n:
                    return 10
                else:
                    return -10

            return -3

        return 0

    # ---- Display

    def display(self):
        print(self.string())

    def display_history(self):
        from pprint import pprint
        pprint(dict(self.history))

    def string(self):
        board_frmt = (
            " {} | {} | {} \n"
            "---+---+---\n"
            " {} | {} | {} \n"
            "---+---+---\n"
            " {} | {} | {} "
        )
        return board_frmt.format(*self.board)

    # For learning

    def state(self):
        return self.cls.states.index(
            tuple([cell.number for cell in self.cells])
        )
