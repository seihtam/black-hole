import os
import threading
from app.ai import AI1
from app.game import BlackHoleGame
from app.models import User
from flask.ext.login import login_required, current_user
from flask.ext.socketio import emit, send, leave_room, join_room
from app import app, socketio
from binascii import hexlify

open_games = {}
running_games = {}
user_games = {}

game_lock = threading.Lock()

# Clear the user from other session
def clear_user(user):
    try:
        game = user_games[user]
    except KeyError:
        return
    emit('left', {}, room=game.room)
    leave_room(game.room)
    del user_games[user]



@socketio.on('join')
@login_required
def on_join(data):
    # Send userid back to user
    emit('join', {
        'player': current_user.id
    })

    # Lock game table
    game_lock.acquire()
    clear_user(current_user.id)
    if 'mode' in data and data['mode'] == 'AI':
        # Create an AI game
        game = BlackHoleGame(AI=AI1())
        game.players = [current_user.id, 0]
        open_games[game.room] = game
        join_room(game.room)
        game.play_AI()

        # Start game
        emit('setup', {
            'names': {
                game.players[0]: User.query.get(game.players[0]).username,
                0: 'Bot',
            }
        }, room=game.room)
        emit('play', game.to_json(), room=game.room)
        app.logger.info('Created AI game for: %d' % game.players[0])
    else:
        # Create human games
        for room in open_games:
            # Join an existing game
            game = open_games[room]
            if current_user.id in game.players:
                continue
            game.players.append(current_user.id)
            running_games[room] = game
            del open_games[room]
            join_room(game.room)

            # Start game
            emit('setup', {
                'names': {
                    game.players[0]: User.query.get(game.players[0]).username,
                    game.players[1]: User.query.get(game.players[1]).username,
                },
            }, room=game.room)
            emit('play', game.to_json(), room=game.room)
            app.logger.info('Paired user: %d with %d' % (game.players[0], game.players[1]))
            break
        else:
            # Create a new game
            game = BlackHoleGame()
            game.players.append(current_user.id)
            open_games[game.room] = game
            join_room(game.room)
            app.logger.info('Cleared a new game lobby for: %d' % game.players[0])
    game_lock.release()

@socketio.on('play')
@login_required
def handle_play_event(data):
    # Validate input
    try:
        game = running_games[data['room']]
        tile = int(data['tile'])
    except (KeyError, ValueError):
        app.logger.error('Client send a play move, the server did not understand')
        return 'HUGE ERROR'

    # Play move
    if game.play(tile, current_user.id):
        app.logger.info('User %d just played' % current_user.id)
        if game.AI:
            app.logger.info('AI is making a move against %d' % current_user.id)
            game.play_AI()
        if game.winner:
            app.logger.info('A game just completed, the winner was: ' + str(game.winner))
        emit('play', game.to_json(), room=game.room)

@socketio.on('disconnect')
@login_required
def handle_disconnect_event(data):
    app.logger.info('Client %d has disconnected' % current_user.id)
    clear_user(current_user.id)
