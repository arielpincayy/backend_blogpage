from marshmallow import Schema, fields, validate

# UserSchema defines the schema for user data using Marshmallow.
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    password_hash = fields.Str(load_only=True, validate=validate.Length(min=6))
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        ordered = True  # Ensures the order of fields in the output