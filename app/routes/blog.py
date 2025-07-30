from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.post import Post
from app.models.tag import Tag
from app.schemas.blog_schema import BlogSchema, BlogStatus
from marshmallow import ValidationError
from datetime import datetime
from app.utils.helpers import slugify
from app import db
import os
import shutil
from flask import current_app

blog_bp = Blueprint('blog', __name__)

# Create a new blog post
@blog_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        schema = BlogSchema(only=('title', 'tags', 'status','url'))
        data = schema.load(request.get_json())

        title = data['title']
        created_at = datetime.now()
        user_id = get_jwt_identity()
        tags = data['tags']
        status = BlogStatus(data['status']).value
        url = data['url']
        
        if Post.query.filter_by(title=title).first() is not None: return jsonify({"error":"A post with that title already exists"}), 400

        post = Post(title=title, title_slug=slugify(title), user_id=user_id, status=status, created_at=created_at, url=url)
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
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    
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
                "title_slug":slugify(post.title),
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
                "status": post.status,
                "url": post.url,
                "tags": [tag.name for tag in post.tags]
            }
            posts_data.append(post_data)
        
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving posts", "details": str(e)}), 500
    
# Get a single blog post by ID
@blog_bp.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    try:
        post = Post.query.get_or_404(post_id)
        post_data = {
            "id": post.id,
            "title": post.title,
            "title_slug": post.title_slug,
            "created_at": post.created_at.isoformat(),
            "user_id": post.user_id,
            "status": post.status.value,
            "url": post.url,
            "tags": [tag.name for tag in post.tags]
        }
        return jsonify(post_data), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving post", "details": str(e)}), 500


#Get a post by title_slug
@blog_bp.route('/public/<string:title_slug>', methods=['GET'])
def get_post_by_slug(title_slug):
    try:
        post = Post.query.filter_by(title_slug=title_slug).first_or_404()

        if(post.status != BlogStatus.PUBLISHED): return jsonify({"error":"Blog is not published"}), 400

        uploads_base = os.path.join(current_app.root_path, 'static', 'uploads', 'mdxs')
        mdx_path = os.path.join(uploads_base, str(post.user_id), title_slug + ".mdx")

        # Leer contenido MDX
        if not os.path.exists(mdx_path):
            return jsonify({"error": "MDX file not found"}), 404

        with open(mdx_path, 'r', encoding='utf-8') as f:
            mdx_content = f.read()

        return jsonify({
            "title": post.title,
            "creted_at":post.created_at,
            "content": mdx_content
        }), 200

    except Exception as e:
        return jsonify({"error": "Error retrieving public post", "details": str(e)}), 500

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
                "title_slug": post.title_slug,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
                "status": post.status,
                "url": post.url,
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
                "title_slug": post.title_slug,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
                "status": post.status.value,
                "url": post.url,
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
                "title_slug": post.title_slug,
                "created_at": post.created_at.isoformat(),
                "user_id": post.user_id,
                "status": post.status,
                "url": post.url,
                "tags": [t.name for t in post.tags]
            }
            posts_data.append(post_data)
        
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({"error": "Error retrieving posts by tag", "details": str(e)}), 500

# Delete a blog post by ID (and its related static content)
@blog_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:        
        post = Post.query.get_or_404(post_id)
        user_id = get_jwt_identity()

        if int(post.user_id) != int(user_id):
            return jsonify({"error": "Unauthorized to delete this post"}), 403

        # Delete related folders (images, pdfs)
        slug_title = slugify(post.title)
        uploads_base = os.path.join(current_app.root_path, 'static', 'uploads')
        folders_to_delete = ['images', 'pdfs']
        for folder in folders_to_delete:
            blog_path = os.path.join(uploads_base, folder, str(user_id), slug_title)
            if os.path.exists(blog_path):
                shutil.rmtree(blog_path)

        # Delete .mdx and .json files
        blog_path_mdx = os.path.join(uploads_base, 'mdxs', str(user_id), slug_title+".mdx")
        blog_path_json = os.path.join(uploads_base, 'jsons', str(user_id), slug_title+".json")
        os.remove(blog_path_mdx)
        os.remove(blog_path_json)

        # Borrar el post de la base de datos
        db.session.delete(post)
        db.session.commit()

        return jsonify({"msg": "Post and related files deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error deleting post", "details": str(e)}), 500
