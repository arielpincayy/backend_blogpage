from marshmallow import Schema, fields, validate

# BlogSchema defines the schema for blog posts using Marshmallow.
class BlogSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    author_id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    published = fields.Bool(required=True)
    tags = fields.List(fields.Str(), required=False)

    class Meta:
        ordered = True  # Ensures the order of fields in the output