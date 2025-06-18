from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.post import Post
from datetime import datetime
from app import db

blog_bp = Blueprint('blog', __name__)

# Create a new blog post
@blog_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        title = request.json.get('title')
        content = request.json.get('content')
        created_at = datetime.now()
        user_id = get_jwt_identity()
        tags = request.json.get('tags', [])
        published = False
    
        if not title or not content:
            return jsonify({"msg": "Title and content are required"}), 400
        post = Post(title=title, content=content, user_id=user_id, published=published, created_at=created_at)
        post.tags = tags
    
        db.session.add(post)
        db.session.commit()
    
        return jsonify({"msg": "Post created successfully", "post_id": post.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error creating post", "error": str(e)}), 500

# Get all blog posts
@blog_bp.route('/posts', methods=['GET'])
def get_posts():
    try:
        posts = Post.query.all()
        posts_data = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
                "published": post.published,
                "tags": [tag.name for tag in post.tags]
            }
            posts_data.append(post_data)
        
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({"msg": "Error retrieving posts", "error": str(e)}), 500
    