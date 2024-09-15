
user_signup_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string", "minLength": 6},
    },
    "required": ["email", "password"],
    "additionalProperties": False
}

user_login_schema = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string", "minLength": 6},
    },
    "required": ["email", "password"],
    "additionalProperties": False
}

user_update_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
    },
    "required": ["name", "email"],
    "additionalProperties": False
}
