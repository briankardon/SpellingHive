from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    client_ip = request.remote_addr
    return render_template('base.html', ip=client_ip)

@socketio.on('my event')
def test_message(message):
    print('got a message!')
    emit('my response', {'data': message['data']})
    print('sent a message back!')

def send_letters(letters):
    letters = validate_letters(letters)
    emit('letters', {'data': letters})

def validate_letters(letters):
    # Check that these are 7 valid letters
    letters = letters.lower()
    if len(letters) != 7:
        raise ValueError('letters must have 7 letters, instead got '+letters)
    if len(letters) != len(set(letters)):
        raise ValueError('letters argument must be 7 unique letters, instead got '+letters)
    return letters

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')



if __name__ == '__main__':
    socketio.run(app, port=8123)
