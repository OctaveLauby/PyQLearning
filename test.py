from games.tictactoe import TTT

ttt = TTT()
print(len(TTT.states))
ttt.act(1, 0)
ttt.act(2, 1)
ttt.act(3, 0)
ttt.act(4, 1)
ttt.act(5, 0)
ttt.act(6, 1)
ttt.display()
