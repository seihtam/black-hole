import os
import time
from binascii import hexlify

board_neighbours = [
    [],
    [2,3],
    [1,3,4,5], [1,2,5,6],
    [2,5,7,8], [2,3,4,6,8,9], [3,5,9,10],
    [4,8,11,12], [4,5,7,9,12,13], [5,6,8,10,13,14], [6,9,14,15],
    [7,12,16,17], [7,8,11,13,17,18], [8,9,12,14,18,19], [9,10,13,15,19,20], [10,14,20,21],
    [11,17], [11,12,16,18], [12,13,17,19], [13,14,18,20], [14,15,19,21], [15,20]]

class BlackHoleGame():
    def __init__(self, AI = None):
        self.room = hexlify(os.urandom(16)).decode('utf-8')
        self.AI = AI
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
        self.last_move = time.time()

        # Find winner (if any)
        self.winner = self.find_winner()
        return True

    def get_neightbours(self, n):
        return board_neighbours[n]

    def find_winner(self):
        if self.turn != 20:
            return None
        for tile in self.board:
            if self.board[tile] == None:
                peers = self.get_neightbours(tile)
                peers = map(lambda n: (self.board[n]['player']. self.board[n]['value']), peers)
                p1_sum = sum([v if p == self.players[0] else 0 for p, v in peers])
                p2_sum = sum([v if p == self.players[1] else 0 for p, v in peers])
                if p1_sum > p2_sum:
                    return self.players[0]
                elif p1_sum < p2_sum:
                    return self.players[1]
                return 'draw'

    def to_json(self):
        return {
            'turn': self.turn,
            'room': self.room,
            'board': self.board,
            'players': self.players,
            'winner': self.winner,
            'started': self.players[self.started],
            'current_player': self.players[self.current],
        }

BlackHoleGame()
