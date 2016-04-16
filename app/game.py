
class BlackHoleGame():
    def __init__(self, AI_game = False):
        self.AI_game = AI_game
        self.board = {n: None for n in range(21)}
        self.turn = 0
        self.last_move = 0  # Time of last move
        self.player1 = None # User object
        self.player2 = None # User object
        self.room1 = None   # Room Id of player1
        self.room2 = None   #
        pass

    def to_json(self, player):
        return {
            'board': self.board,
            'brick': self.brick,
        }

