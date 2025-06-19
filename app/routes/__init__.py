from .auth import auth_bp
from .blog import blog_bp
from .tag import tag_bp
from .upload import upload_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(tag_bp, url_prefix='/tags')
    app.register_blueprint(upload_bp, url_prefix='/upload')