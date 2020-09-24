from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from model import init_db

import logging

from service.room import RoomService


log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/users/create', methods=["POST"])
def create_user():
    data = request.json
    print(data)
    return jsonify(data)


@app.route('/room/<room_name>', methods=["POST", "GET"])
def create_room(room_name):
    if request.method == "GET":
        return ''

    if request.method == "POST":
        data = request.json
        room = RoomService.add(room_name, 'asdfsa')
        print(data)
        print(room_name)
        return room.to_dict()


@app.route('/room/<room_name>/join', methods=['POST'])
def join_room(room_name):
    return room_name + 'joined'


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


if __name__ == '__main__':
    init_db()
    socketio.run(app, port=1488, debug=False)
