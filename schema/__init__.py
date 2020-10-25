import marshmallow


class UserSchema(marshmallow.Schema):
    name = marshmallow.fields.String(required=True)
    icon_color = marshmallow.fields.String(required=True)


class CreateRoomSchema(marshmallow.Schema):
    name = marshmallow.fields.String(required=True)
    creator = marshmallow.fields.String(required=True)
