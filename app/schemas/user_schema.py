from marshmallow import Schema, fields, validate

# UserSchema defines the schema for user data using Marshmallow.
class UserSchema(Schema):
    id = fields.Int(dump_only=True, error_messages={
        "invalid": "ID must be an integer."
    })
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "Name is required.",
        "invalid": "Name must be a string with a maximum length of 100 characters."
    })
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "Last name is required.",
        "invalid": "Last name must be a string with a maximum length of 100 characters."
    })
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50), error_messages={
        "required": "Username is required.",
        "invalid": "Username must be a string with a maximum length of 50 characters."
    })
    email = fields.Email(required=True, error_messages={
        "required": "Email is required.",
        "invalid": "Email must be a valid email address."
    })
    password_hash = fields.Str(load_only=True, validate=validate.Length(min=6), error_messages={
        "required": "Password is required.",
        "invalid": "Password must be a string with a minimum length of 6 characters."
    })
    created_at = fields.DateTime(dump_only=True, error_messages={
        "invalid": "Created at must be a valid datetime."
    })

    class Meta:
        ordered = True  # Ensures the order of fields in the output