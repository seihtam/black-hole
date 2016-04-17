import threading
from math import floor, ceil
from app.ai import AI1
from app.game import BlackHoleGame
from app.models import User
from flask.ext.login import login_required, current_user
from flask.ext.socketio import emit, leave_room, join_room
from app import app, socketio, db

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

# Ajust elo according to game result
def update_elo(game):
    app.logger.info('Ajusting elo after game completion')

    winner = game.find_winner()

    # Handle draw
    if winner == 'draw':
        app.logger.error('Draw not handled')
        return

    # Handle winner
    for player in game.players:
        if player == winner:
            winner = User.query.get(player)
            continue
        loser = User.query.get(player)

    # Calculate elo rating
    K = 16
    Q_a = 10**(winner.score / 400)
    Q_b = 10**(loser.score / 400)
    E_a = Q_a / (Q_a + Q_b)
    E_b = Q_b / (Q_a + Q_b)
    app.logger.info('Old score: winner = %d, loser = %d' % (winner.score, loser.score))
    winner_old = winner.score
    loser_old = loser.score

    winner.score = ceil(winner.score + K * (1 - E_a))
    loser.score = floor(loser.score + K * (0 - E_b))

    app.logger.info('New score: winner = %d, loser = %d' % (winner.score, loser.score))
    db.session.commit()

    return {
        winner.id: winner.score - winner_old,
        loser.id: loser.score - loser_old
    }

@socketio.on('join')
@login_required
def on_join(data):
    # Send userid back to user
    emit('join', {
        'player': current_user.id
    })

    # Verify user input
    if 'mode' not in data:
        app.logger.error('User joined without giving a mode!')
        return

    # Lock game table
    game_lock.acquire()
    clear_user(current_user.id)
    if data['mode'] == 'bot':
        # Create an AI game
        game = BlackHoleGame(AI=AI1())
        game.players = [current_user.id, 0]
        open_games[game.room] = game
        join_room(game.room)
        running_games[game.room] = game

        # Start game
        game.play_AI()
        emit('setup', {
            'names': {
                game.players[0]: User.query.get(game.players[0]).username,
                0: 'Bot',
            }
        }, room=game.room)
        emit('play', game.to_json(), room=game.room)
        app.logger.info('Created AI game for: %d' % game.players[0])
    elif data['mode'] == 'pvp':
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
            app.logger.info('Created a new game lobby for: %d' % game.players[0])
    else:
        app.logger.error('User joined with unknown mode %s' % data['mode'])
        return

    # Unlock games table
    app.logger.info('Current open games %d' % len(open_games))
    app.logger.info('Current running games %d' % len(running_games))
    game_lock.release()

@socketio.on('play')
@login_required
def handle_play_event(data):
    # Validate input
    try:
        game = running_games[data['room']]
        tile = int(data['tile'])
    except (KeyError, ValueError):
        app.logger.error('Client send a play move, the server did not understand:' + str(data))
        return

    # Play move
    if game.play(tile, current_user.id):
        app.logger.info('User %d just played' % current_user.id)
        if game.AI:
            app.logger.info('AI is making a move against %d' % current_user.id)
            game.play_AI()
        winner = game.find_winner()
        if winner != None and game.AI == None:
            app.logger.info('A game just completed, the winner was: ' + str(winner))
            emit('endgame', {
                'winner': winner,
                'elo' : update_elo(game)},
                room=game.room
            )
        elif winner != None and game.AI:
            app.logger.info('A bot game just completed, the winner was: ' + str(winner))
            emit('endgame', {
                'winner': winner,
                'elo': None},
                room=game.room
            )
        elif winner != None:
            app.logger.warning('Unhandled win condition')
            return
        emit('play', game.to_json(), room=game.room)

@socketio.on('disconnect')
@login_required
def handle_disconnect_event(data):
    app.logger.info('Client %d has disconnected' % current_user.id)
    clear_user(current_user.id)
