from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask_session import Session
from flask_socketio import SocketIO, emit
from game import Game
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(
    app,
    connectionStateRecovery={
        'maxDisconnectionDuration': 30 * 1000, # 30 seconds to recover
        'skipMiddlewares': True
    }
)
Session(app)

game = Game()

@app.route('/')
def index():
    return render_template('base.html')

@socketio.on('new_game_request')
def new_game():
    global game
    print('New game requested')
    game.reset()
    update_client_game_state()

# def send_letters():
#     emit('letters', {'data': game.letters})

def get_client_game_state():
    return dict(
        players=game.players,
        played_words=game.played_words,
        finished=game.finished,
        letters=game.letters,
        words=game.words,
    )

def update_client_game_state(message='', broadcast=True):
    emit('update_game_state', {'data': get_client_game_state(), 'comment':message}, broadcast=broadcast)

@socketio.on('connect')
def connect():
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
    game.rename_player(id, new_name)
    # emit('rename', {'data': 'renamed {id} from {o} to {n}'.format(id=id, o=old_name, n=new_name)})
    update_client_game_state()

@socketio.on('play_word')
def play_word(message):
    id = request.sid
    word = message['data']
    score, msg = game.play_word(id, word)
    if game.finished:
        game_over()
    message = "{p} point{s}: {msg}".format(p=score, s='s'*(score!=1), msg=msg)
    update_client_game_state(message)

def game_over():
    winner_ids = game.get_winner()
    winner_names = [game.get_player_name(id) for id in winner_ids]
    message = json.dumps(dict(ids=winner_ids, names=winner_names))
    update_client_game_state()

@socketio.on('disconnect')
def disconnect(reason):
    id = request.sid
    game.remove_player(id)
    update_client_game_state()
    print('RX/TX: Client disconnected because:', reason)

if __name__ == '__main__':
    socketio.run(app, port=8123)
