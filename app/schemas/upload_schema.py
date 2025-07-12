from marshmallow import Schema, fields

# Schema for file upload validation
class UploadSchema(Schema):
    blog_name = fields.String(required=True, allow_none=False, error_messages={"required": "Blog name is required."})
    number = fields.String(required=True, allow_none=False, error_messages={"required": "Number is required."})

    class Meta:
        ordered = True  # Ensures the order of fields in the output