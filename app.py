from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def hello_world():
    return 'Hello World!'


@socketio.on('connect_user')
def user_connect(user):
    print(user)
    emit('user_connected', user)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    socketio.run(app, port=1488)
