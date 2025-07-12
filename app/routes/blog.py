from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.post import Post
from app.models.tag import Tag
from app.schemas.blog_schema import BlogSchema
from marshmallow import ValidationError
from datetime import datetime
from app.utils.helpers import slugify
from app import db

blog_bp = Blueprint('blog', __name__)

# Create a new blog post
@blog_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        schema = BlogSchema(only=('title', 'tags'))
        data = schema.load(request.get_json())

        title = data['title']
        created_at = datetime.now()
        user_id = get_jwt_identity()
        tags = data['tags']
        status = data['status']
        
        if Post.query.filter_by(title=title).first() is not None: return jsonify({"error":"A post with that title already exists"}), 400

        post = Post(title=title, user_id=user_id, status=status, created_at=created_at)
        db.session.add(post)

        # Handle tags
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name, slug=slugify(tag_name))
                db.session.add(tag)
            post.tags.append(tag)

        db.session.commit()
    
        return jsonify({"msg": "Post created successfully", "post_id": post.id}), 201
    
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating post", "details": str(e)}), 500

# Get all blog posts
@blog_bp.route('/posts', methods=['GET'])
def get_posts():
    try:
        posts = Post.query.limit(10).all()
        posts_data = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
                "status": post.status,
                "tags": [tag.name for tag in post.tags]
            }
            posts_data.append(post_data)
        
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving posts", "details": str(e)}), 500
    
# Get a single blog post by ID
@blog_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.isoformat(),
            "user_id": post.user_id,
            "status": post.status,
            "tags": [tag.name for tag in post.tags]
        }
        return jsonify(post_data), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving post", "details": str(e)}), 500

#Get all posts by a specific title
@blog_bp.route('/posts/title/<string:title>', methods=['GET'])
def get_posts_by_title(title):
    try:
        posts = Post.query.filter(Post.title.ilike(f'%{title}%')).all()
        posts_data = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
                "status": post.status,
                "tags": [tag.name for tag in post.tags]
            }
            posts_data.append(post_data)
        
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving posts by title", "details": str(e)}), 500
    
# Get all posts by a specific user
@blog_bp.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    try:
        posts = Post.query.filter_by(user_id=user_id).all()
        posts_data = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
                "status": post.status,
                "tags": [tag.name for tag in post.tags]
            }
            posts_data.append(post_data)
        
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving user's posts", "details": str(e)}), 500
    
# Get all posts with a specific tag
@blog_bp.route('/tags/<string:tag_name>/posts', methods=['GET'])
def get_posts_by_tag(tag_name):
    try:
        tag = Tag.query.filter_by(name=tag_name).first_or_404()
        posts = tag.posts 
        posts_data = []
        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
                "status": post.status,
                "tags": [t.name for t in post.tags]
            }
            posts_data.append(post_data)
        
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving posts by tag", "details": str(e)}), 500
    