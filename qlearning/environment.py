class Environment(object):

    def __init__(self, game):
        self.game = game

    def state(self):
        return self.game.state()

    def act(self, action, player):
        return self.game.play(action, player)
