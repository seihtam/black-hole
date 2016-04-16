import os
from binascii import hexlify

class BlackHoleGame():
    def __init__(self, AI_game = False):
        self.room = hexlify(os.urandom(16)).decode('utf-8')
        self.AI_game = AI_game
        self.board = {n: None for n in range(1, 22)}
        self.turn = 0
        self.last_move = 0  # Time of last move
        self.players = []   # User ids
        self.current = 0    # Current player

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

    def to_json(self):
        return {
            'room': self.room,
            'board': self.board,
            'players': self.players,
            'current_player': self.players[self.current],
        }

