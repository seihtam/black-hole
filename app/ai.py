import os
from app import app, db, login_manager
from app.models import User

class AI1():
    def __init__(self):
        pass

    def play(self, game, player):
        for tile in self.board:
            if self.board[tile] == None:
                game.play(tile)
        pass

