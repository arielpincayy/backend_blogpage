from flask import Blueprint
from .auth import auth_bp
from .blog import blog_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp, url_prefix='/blog')