
create_product_schema = {
    "type": "object",
    "properties": {
        "user_id": {"type": "string"},# This is the user_id of the user creating the product, as referenced in the user_auth_schema.py
        "product_id": {"type": "string"},
        "name": {"type": "string"},
        "category": {"type": "string"},
        "description": {"type": "string"},
        "brand": {"type": "string"},
        "price": {"type": "number"},
        "quantity": {"type": "number"},
        "image": {"type": "string"},
    },
    "required": ["name", "category", "description", "brand", "price", "quantity", "image"],
    "additionalProperties": False
}

update_product_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "category": {"type": "string"},
        "description": {"type": "string"},
        "brand": {"type": "string"},
        "price": {"type": "number"},
        "quantity": {"type": "number"},
        "image": {"type": "string"},
    },
    "required": ["name", "category", "description", "brand", "price", "quantity", "image"],
    "additionalProperties": False
}

