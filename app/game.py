import os
from binascii import hexlify

board_graph = {
    1: [2, 3],

}

board_neighbor = [[],
                [2,3],
                [1,3,4,5],[1,2,5,6],
                [2,5,7,8],[2,3,4,6,8,9],[3,5,9,10],
                [4,8,11,12],[4,5,7,9,12,13],[5,6,8,10,13,14],[6,9,14,15],
                [7,12,16,17],[7,8,11,13,17,18],[8,9,12,14,18,19],[9,10,13,15,19,20],[10,14,20,21],
                [11,17],[11,12,16,18],[12,13,17,19],[13,14,18,20],[14,15,19,21],[15,20]]

class BlackHoleGame():
    def __init__(self, AI_game = False):
        self.room = hexlify(os.urandom(16)).decode('utf-8')
        self.AI_game = AI_game
        self.board = {n: None for n in range(1, 22)}
        self.turn = 0                         # Current turn (for both sides)
        self.last_move = 0                    # Time of last move
        self.players = []                     # User ids
        self.current = ord(os.urandom(1)) % 2 # Current player
        self.started = self.current

    def play(self, n, player):
        if self.board[n] != None:
            return False
        if self.players[self.current] != player:
            return False
        if n > 21 or n < 1:
            return False

        # Do it
        self.board[n] = {
            'player': player,
            'value': (self.turn // 2) + 1,
        }
        self.turn += 1
        self.current = (self.current + 1) % len(self.players)
        return True

    def ai_play(self, player):
        for tile in self.board:
            if self.board[tile] is None:
                return self.play(tile, player)
        pass

    def get_neightbors(self, n):
        pass


    def to_json(self):
        return {
            'turn': self.turn,
            'room': self.room,
            'board': self.board,
            'players': self.players,
            'started': self.started,
            'current_player': self.players[self.current],
        }

BlackHoleGame()
