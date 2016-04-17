import os
from random import choice, randrange
from app import app, db, login_manager
from app.models import User

class AI1():
    def __init__(self):
        pass

    def play(self, game):
        # Find a tile
        app.logger.info('BOT: Game = ' + str(game))
        tiles = [(game.board[t]['value'] if game.board[t] else 0, t) for t in game.board]
        tiles = sorted(tiles, reverse=True)
        app.logger.info('BOT: Tiles = ' + str(tiles))

        # Choose a tile
        for _, tile in tiles:
            free = filter(lambda n: game.board[n] == None, game.get_neightbours(tile))
            free = list(free)
            if len(free) == 0:
                continue
            game.play(choice(free))
            return
