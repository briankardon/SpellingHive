from flask import Flask
from flask import redirect, url_for
from flask import render_template
from flask import request
from flask import session
from flask_session import Session
from flask_socketio import SocketIO, emit
from game import Game
import json
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(
    app,
    connectionStateRecovery={
        'maxDisconnectionDuration': 3 * 1000, # 30 seconds to recover
        'skipMiddlewares': True
    },
    ping_timeout=3,
    ping_interval=5,
)
Session(app)

game = Game()

@app.route('/')
def home_page(**kwargs):
    return redirect(url_for('lobby_page', **kwargs))

@app.route('/lobby')
def lobby_page(**kwargs):
    return render_template('lobby.html')

@app.route('/game')
def game_page(**kwargs):
    # if not game.started:
    #     return redirect(url_for('lobby_page', **kwargs))
    # else:
    return render_template('game.html')

@socketio.on('new_game_request')
def new_game(message):
    print('got new game request')
    global game
    if not game.started:
        print('New game requested')
        game.reset()
        game.start()
        update_client_game_state()
        emit('start_game', {'data': None}, broadcast=True)
    else:
        print('New game requested but game was already started')

# def send_letters():
#     emit('letters', {'data': game.letters})

def get_player_list():
    players = {id:game.players[id]['name'] for id in game.players}
    emit('player_list', {'data':players})

def get_client_game_state():
    return dict(
        players=game.players,
        played_words=game.played_words,
        started = game.started,
        finished=game.finished,
        letters=game.letters,
        required_letter=game.required_letter,
        words=game.words,
    )

def increment_name(name):
    match = re.search('(.*)(_([0-9]+))', name)
    if match:
        base_name = match.groups(1)
        if len(match.groups()) > 2:
            number = int(match.groups(3))
        else:
            number = 0
    else:
        base_name = name
        number = 0

    number = number + 1

    new_name = "{bn}_{k}".format(bn=base_name, k=number)
    return new_name



def update_client_game_state(message='', broadcast=True):
    emit('update_game_state', {'data': get_client_game_state(), 'comment':message}, broadcast=broadcast)

def broadcast_message(text_message):
    # Send message to all players
    emit('message', {'data': text_message}, broadcast=True)

@socketio.on('chat')
def chat(message):
    id = request.sid
    name = game.players[id]['name']
    text_message = name + ' says: ' + message['data']
    print('sending chat:', text_message)
    broadcast_message(text_message)

@socketio.on('connect')
def connect(message):
    id = request.sid
    try:
        print('Got connect signal:')
        print('id=', id)
        game.add_player(id, 'Mystery player')
        print('RX/TX: Player connected')
        emit('your_id', {'data': id});
        # emit('player_added', {'data': 'Player {id} connected'.format(id=id)})
    except IndexError:
        print('RX/TX: Player reconnected')
        emit('your_id', {'data': id});
        # emit('player_added', {'data': 'Player {id} reconnected'.format(id=id)})
    update_client_game_state()

@socketio.on('rename')
def rename(message):
    id = request.sid
    old_name = game.get_player_name(id)
    new_name = message['data']
    message = old_name + " changed name to " + new_name
    game.rename_player(id, new_name)
    # emit('rename', {'data': 'renamed {id} from {o} to {n}'.format(id=id, o=old_name, n=new_name)})
    update_client_game_state(message=message)

@socketio.on('play_word')
def play_word(message):
    id = request.sid
    word = message['data']
    score, msg = game.play_word(id, word)
    if game.finished:
        game_over()
    message = "{p} point{s}: {msg}".format(p=score, s='s'*(score!=1), msg=msg)
    update_client_game_state(message=message)

def game_over():
    winner_ids = game.get_winner()
    winner_names = [game.get_player_name(id) for id in winner_ids]
    message = json.dumps(dict(ids=winner_ids, names=winner_names))
    update_client_game_state(message=message)

@socketio.on('disconnect')
def disconnect(reason):
    id = request.sid
    name = game.get_player_name(id)
    message = name + ' left'
    game.remove_player(id)
    update_client_game_state(message=message)
    print('RX/TX: Client disconnected because:', reason)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8123)
