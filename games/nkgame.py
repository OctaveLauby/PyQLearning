from .exceptions import GameOver, InvalidPlay, InvalidPlayer
from .game import Game


def build_diags(n, k):
    """Build all possible diags of min size k withing a n*n square.

    Returns:
        (2d-list): each sublist is a list of indexes describing a diag
            index for position i, j = n * i + j
    """
    brange = list(range(n))
    diags_indexes = []
    # Diags from left to right
    for row in brange:
        crange = [0] if row else brange  # Avoid going on previous diags
        for col in crange:
            # row, col is a starting point in matrix
            diag_indexes = [row * n + col]
            next_row, next_col = row + 1, col + 1
            while not (next_row >= n or next_col >= n):
                diag_indexes.append(next_row * n + next_col)
                next_row += 1
                next_col += 1
            if len(diag_indexes) < k:
                continue
            else:
                diags_indexes.append(diag_indexes)

    # Diags from right to left
    for row in brange:
        crange = [n-1] if row else brange  # Avoid going on previous diags
        for col in crange:
            diag_indexes = [row * n + col]
            next_row, next_col = row + 1, col - 1
            while not (next_row >= n or next_col < 0):
                diag_indexes.append(next_row * n + next_col)
                next_row += 1
                next_col -= 1
            if len(diag_indexes) < k:
                continue
            else:
                diags_indexes.append(diag_indexes)

    return diags_indexes


def winners(sub_cells, k):
    """Return list of winners an a succession of cells."""
    previous_cell = None
    counter = {}
    winners = set()
    for cell in sub_cells:
        if cell is None:
            previous_cell = cell
        if previous_cell is None:
            counter[cell] = 1
            previous_cell = cell
        elif cell == previous_cell:
            counter[cell] += 1
            if counter[cell] >= k:
                winners.add(previous_cell)
        elif cell != previous_cell:
            counter[cell] = 1
            previous_cell = cell
    return winners


class NKGame(Game):

    def __init__(self, n, k, **game_kwargs):
        kwargs = {
            'n': n,
            'k': k,
        }
        kwargs.update(game_kwargs)
        super().__init__(**kwargs)

        assert n >= k

        # Game board
        self.n = n
        self.k = k
        self.cells = [None for cell in range(n**2)]

        # State
        self.player_n = 0
        self.winner = None
        self.ended = False
        self.history = []

        # Utils
        self.indexes = None
        self.init()

    def init(self):
        """Init possible successions of cells (indexes)."""

        brange = list(range(self.n))  # Row/Col range

        # TODO: make in work for n > k cases
        self.indexes = {
            'row': [
                [i * self.n + j for j in brange]
                for i in brange
            ],
            'col': [
                [i * self.n + j for i in brange]
                for j in brange
            ],
            'diag': build_diags(self.n, self.k)
        }

    def is_over(self):
        return self.ended

    def act(self, cell_i, player):
        """Play on cell i for player."""
        if self.is_over():
            raise GameOver("Game over already.")

        if self.player_n != player:
            raise InvalidPlayer(
                "Expecting player %s, got player %s"
                % (self.player_n, player)
            )

        if self.cells[cell_i] is not None:
            raise InvalidPlay(
                "Can't play on cell %s, already played by %s"
                % (cell_i, self.cells[cell_i])

            )

        self.cells[cell_i] = player
        self.history.append((player, cell_i))
        self.player_n = 1 - player
        self.check_end()

    def check_end(self):
        # sub_indexes = self.indexes['row'][0]
        # sub_cells = [self.cells[ind] for ind in sub_indexes]
        # print(sub_cells, self.k, winners(sub_cells, self.k))
        subs_indexes = (
            self.indexes['row'] + self.indexes['col'] + self.indexes['diag']
        )
        for sub_indexes in subs_indexes:
            sub_cells = [self.cells[ind] for ind in sub_indexes]
            win_set = winners(sub_cells, self.k)
            if win_set:
                self.winner = win_set.pop()
                self.ended = True
                return

        self.ended = None not in self.state()

    def reset(self):
        """Reset game to beginning."""
        self.cells = [None for cell in range(self.n**2)]

        # State
        self.player_n = 0
        self.winner = None
        self.ended = False
        self.history = []

    # ----------------------------------------------------------------------- #
    # For qlearning

    def actions(self):
        """Return list of available actions."""
        return [
            cell_i
            for cell_i, cell in enumerate(self.cells)
            if cell is not None
        ]

    def actions_all(self):
        return [cell_i for cell_i in range(self.n ** 2)]

    def state(self):
        """Return tuple describing state."""
        return tuple(self.cells)

    # ----------------------------------------------------------------------- #
    # Display

    def display(self):
        print(self.string())

    def display_history(self):
        from pprint import pprint
        pprint(dict(self.history))

    def string(self):
        symbols = self.symbols()
        ligne_separtor = " \n" + ("---+" * self.n)[:-1] + "\n"
        return ligne_separtor.join(
            [
                " |".join(
                    [
                        " " + str(symbol)
                        for symbol in row_symbols
                    ]
                )
                for row_symbols in symbols
            ]
        ) + " "

    def symbols(self):
        brange = list(range(self.n))  # Row/Col range
        return [
            [
                " "
                if self.cells[self.n * row + col] is None
                else self.cells[self.n * row + col]
                for col in brange
            ]
            for row in brange
        ]
