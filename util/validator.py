from flask import request


def body_validator(schema):
    body = request.json
    schema_instance = schema()
    schema_instance.load(body)
    return body
