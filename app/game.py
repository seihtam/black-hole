import os
from binascii import hexlify

class BlackHoleGame():
    def __init__(self, AI_game = False):
        self.room = hexlify(os.urandom(16))
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
            'value': self.turn // 2,
        }
        self.turn += 1
        self.current = (self.current + 1) % len(self.players)
        return True

    def to_json(self, player):
        return {
            'room': self.room,
            'board': self.board,
            'players': self.players,
            'current': self.players[self.current],
        }

