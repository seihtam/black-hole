import os
from app.game import BlackHoleGame
from flask.ext.login import login_required, current_user
from flask.ext.socketio import emit, send, leave_room
from app import app, socketio
from binascii import hexlify

open_games = {}
running_games = {}

@login_required
@socketio.on('join')
def on_join(data):
    # Send userid back to user
    send({
        'user': current_user.id
    })

    # LOCK : TODO
    for room in open_games:
        # Join an existing game
        game = open_games[room]
        game.players.append(current_user.id)
        running_games[room] = game
        del open_games[room]
        emit(game.to_json, room=game.room)
        break
    else:
        # Create a new game
        game = BlackHoleGame()
        game.players.append(current_user.id)
        open_games[game.room] = game

@login_required
@socketio.on('play')
def handle_play_event(data):
    try:
        game = open_games[data['room']]
        tile = int(data['tile'])
    except (KeyError, ValueError):
        return 'HUGE ERROR'
    if game.play(tile, current_user.id):
        emit(game.to_json, room = game.room)


@login_required
@socketio.on('disconnect')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    # send(username + ' has left the room.', room=room)
