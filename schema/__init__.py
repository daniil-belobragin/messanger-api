import marshmallow


class UserSchema(marshmallow.Schema):
    name = marshmallow.fields.String(required=True)
    icon_color = marshmallow.fields.String(required=True)
