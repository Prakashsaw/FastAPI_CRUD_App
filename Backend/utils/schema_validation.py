# utils/shcema_validation.py

from jsonschema import validate, ValidationError
from flask import jsonify

# Function to validate JSON data against a schema
def validate_json(schema, data):
    try:
        validate(instance=data, schema=schema)
        return None  # No errors
    except ValidationError as e:
        return jsonify({"error": str(e.message)}), 400
