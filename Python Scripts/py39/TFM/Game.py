from Player import Player

class Game:
    resources = ('Gold', 'Steel', 'Titanium', 'Plant', 'Energy', 'Heat')
    devider   = '\n' + '-#-#' * 50 + '-\n'
    def __init__(self, players=2):
        self.players = [Player(self, str(i)) for i in range(players)]
        [print(p) for p in self.players]


if __name__ == "__main__":
    import Main