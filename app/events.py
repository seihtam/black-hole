import os
from app.game import BlackHoleGame
from flask.ext.login import login_required
from app import app, socketio

games = {}

@login_required
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    # send(, room=room)

@login_required
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    # send(username + ' has left the room.', room=room)
