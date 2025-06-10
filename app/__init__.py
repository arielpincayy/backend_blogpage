from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:terrioco22verde701*@db:5432/blogdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Importa los modelos para que Flask-Migrate los registre
    from .models.user import User
    from .models.post import Post
    from .models.tag import Tag  # si lo tienes
    from .models import post_tags  # si defines la tabla many-to-many fuera de clase

    return app