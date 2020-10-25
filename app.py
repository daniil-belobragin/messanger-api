from flask import Flask
from flask_cors import CORS
import eventlet
import socketio
import logging

from marshmallow import ValidationError

from model import init_db
from util.validator import body_validator

from schema import UserSchema, CreateRoomSchema
from schema.exception import ConflictException, NotFoundException

from service.room import RoomService
from service.user import UserService
from service.message import MessageService
from service.participant import ParticipantService


eventlet.monkey_patch()

log = logging.getLogger('werkzeug')
log.disabled = True

sio = socketio.Server(cors_allowed_origins="*")

flask_app = Flask(__name__)
app = socketio.WSGIApp(sio, flask_app)

CORS(flask_app)
cors = CORS(flask_app, resources={
    r"/*": {
        "origins": "*"
    }
})


@flask_app.errorhandler(ValidationError)
def handle_validation_exception(error):
    return {
        "error": error.messages
    }, 422


@flask_app.errorhandler(NotFoundException)
def handle_not_found_exception(error):
    return {
        "error": error.response
    }, 404


@flask_app.errorhandler(ConflictException)
def handle_conflict_exception(error):
    return {
        "error": error.response
    }, 409


@flask_app.route("/users/create", methods=["POST"])
def create_user():
    body = body_validator(UserSchema)

    user_name = body["name"]
    icon_color = body["icon_color"]

    user = UserService.add(user_name, icon_color)
    return user.to_dict()


@flask_app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):

    if not UserService.exist_by_id(user_id):
        raise NotFoundException(pointer="user", message="not found")

    user = UserService.remove_by_id(user_id)
    return user.to_dict()


@flask_app.route("/rooms/create", methods=["POST"])
def create_room():
    body = body_validator(CreateRoomSchema)

    room_name = body["name"]
    creator = body["creator"]

    if not UserService.exist_by_id(creator):
        raise NotFoundException(pointer="user", message="not found")

    if RoomService.exist_by_id(room_name):
        raise ConflictException(pointer="room", message="exists")

    room = RoomService.add(room_name, creator)
    ParticipantService.add(room.id, creator, is_creator=True)

    return room.to_dict()


@sio.on("join_room")
def join(sid, data):
    user = data["user"]
    room_id = data["room_id"]
    sio.enter_room(sid, room_id)

    if not RoomService.exist_by_id(room_id):
        sio.emit("not_found_error", "room")
        sio.leave_room(sid, room_id)
        return

    if not UserService.exist_by_id(user["id"]):
        sio.emit("not_found_error", "user")
        sio.leave_room(sid, room_id)

    if ParticipantService.is_creator(room_id, user["id"]):
        participant = ParticipantService.by_room_id(room_id)
        data = {"participants": participant, "messages": []}
        sio.emit("user_connected", data, room=room_id)
        return

    if ParticipantService.exists_by_user_id_room_id(user["id"], room_id):
        sio.emit("conflict_error", "participant")
        sio.leave_room(sid, room_id)
        return

    ParticipantService.add(room_id, user["id"])

    participants = ParticipantService.by_room_id(room_id)
    messages = MessageService.by_room_id(room_id)

    data = {"participants": participants, "messages": messages}
    sio.emit("user_connected", data, room=room_id)
    return


@sio.on("leave_room")
def leave(sid, data):
    user = data["user"]
    room_id = data["room_id"]

    if ParticipantService.is_creator(room_id, user["id"]):
        RoomService.remove_by_id(room_id)
        sio.emit("creator_disconnected", room_id=room_id)

    if ParticipantService.exists_by_user_id(user["id"]):
        ParticipantService.remove_by_user_id(user["id"])

    sio.leave_room(sid, room_id)
    sio.emit("user_disconnected", user["id"], room=room_id)
    return


@sio.event
def connect(sid, environ):
    print("connected: {}".format(sid))


@sio.event
def disconnect(sid):
    print("disconnected: {}".format(sid))


@sio.event
def connect_error(sid):
    print("connect_error: {}".format(sid))


@sio.event
def reconnect(sid):
    print("reconnect: {}".format(sid))


@sio.on("send_message")
def handle_message(sid, data):
    user = data["user"]
    room_id = data["room_id"]
    message_content = data["message_content"]

    message = MessageService.add(room_id, user["id"], message_content)
    print("received message: {}. From user: {}.\nNow it's look like {}".format(message_content, user["name"],
                                                                               message.to_dict()))
    sio.emit("message_received", message.to_dict(), room=room_id)


if __name__ == '__main__':
    init_db()
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 2020)), app)
