import os
from app.ai import AI1
from app.game import BlackHoleGame
from flask.ext.login import login_required, current_user
from flask.ext.socketio import emit, send, leave_room, join_room
from app import app, socketio
from binascii import hexlify

open_games = {}
running_games = {}


@socketio.on('join')
@login_required
def on_join(data):
    # Send userid back to user
    emit('join', {
        'user': current_user.id
    })

    # Check if AI game
    if 'mode' in data and data['mode'] == 'AI':
        game = BlackHoleGame(AI=AI1)

    # LOCK : TODO
    for room in open_games:
        # Join an existing game
        game = open_games[room]
        if game.player1 == current_user.id:
            continue
        game.players.append(current_user.id)
        running_games[room] = game
        del open_games[room]
        join_room(game.room)
        emit('play', game.to_json(), room=game.room)
        break
    else:
        # Create a new game
        game = BlackHoleGame()
        game.players.append(current_user.id)
        open_games[game.room] = game
        join_room(game.room)


@socketio.on('play')
@login_required
def handle_play_event(data):
    print(data)
    try:
        game = running_games[data['room']]
        tile = int(data['tile'])
    except (KeyError, ValueError):
        print("ERROR")
        return 'HUGE ERROR'

    print(tile)
    print(current_user.id)
    if game.play(tile, current_user.id):
        print('Look who wins:', game.winner)
        print("emit play")
        emit('play', game.to_json(), room=game.room)


@socketio.on('disconnect')
@login_required
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    # send(username + ' has left the room.', room=room)
