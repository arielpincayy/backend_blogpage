from flask import Blueprint, jsonify
from app.models.tag import Tag

tag_bp = Blueprint('tag', __name__)

# Ask for all tags
@tag_bp.route('/tags', methods=['GET'])
def get_tags():
    try:
        tags = Tag.query.all()
        tags_data = [{"id": tag.id, "name": tag.name, "slug": tag.slug} for tag in tags]
        return jsonify({"tags": tags_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

