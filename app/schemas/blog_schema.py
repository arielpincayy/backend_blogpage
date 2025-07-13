from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField
from app.utils import BlogStatus

# BlogSchema defines the schema for blog posts using Marshmallow.
class BlogSchema(Schema):
    id = fields.Int(dump_only=True, error_messages={
        "invalid": "ID must be an integer."
    })
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100), error_messages={
        "required": "Title is required.",
        "invalid": "Title must be a string with a maximum length of 100 characters."
    })
    author_id = fields.Int(dump_only=True, error_messages={
        "invalid": "Author ID must be an integer."
    })
    created_at = fields.DateTime(dump_only=True, error_messages={
        "invalid": "Created at must be a valid datetime."
    })
    status = EnumField(BlogStatus, by_value=True, error_messages={
        "required": "Published status is required.",
        "invalid": "Published status not valid."
    })
    url = fields.Str(required=True, validate=validate.Length(min=1, max=200), error_messages={
        "required":"URL is required",
        "invalid":"URL must be a string with a maximum length of 200 characters"
    })
    tags = fields.List(fields.Str(), required=False, error_messages={
        "invalid": "Tags must be a list of strings."
    })

    class Meta:
        ordered = True  # Ensures the order of fields in the output