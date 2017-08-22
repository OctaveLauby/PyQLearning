from games.exceptions import InvalidPlay
from games.tictactoe import TTT
from qlearning.agent import Agent


def play(player_n, agent):
    game = TTT()
    while not game.is_over():
        if game.player_n is player_n:
            print()
            game.display()
            action = int(input("Your turn: "))
        else:
            action = agent.predict(game.state())
        try:
            game.act(action, game.player_n)
        except InvalidPlay as e:
            print(e)
            pass

    print()
    game.display()
    if game.winner is None:
        print("Tie Game")
    elif game.winner.number == player_n:
        print("You win.")
    else:
        print("hahaha you such a LOSER")


if __name__ == "__main__":
    from argparse import ArgumentParser
    import os
    parser = ArgumentParser("Train two agents on TicTacToe.")
    parser.add_argument(
        "-p", "--player", type=int, required=False, default=0,
        help="Payer you want to be."
    )
    parser.add_argument(
        "-l", "--load_dir", type=str, required=True,
        help="Directory where AI is."
    )
    args = parser.parse_args()
    player_n = args.player
    assert player_n in [0, 1]
    agent = Agent(TTT)
    agent.load(os.path.join(args.load_dir, str(1-player_n)))

    play(player_n, agent)
