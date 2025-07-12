from app import db
from datetime import datetime, timezone
from sqlalchemy import Enum as SQLALCHEMYEnum
from enum import Enum

class BlogStatus(Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    WAITING = "WAITING"
    REFUSED = "REFUSED"

# Tabla intermedia muchos a muchos
post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

# Modelo Post
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(SQLALCHEMYEnum(BlogStatus, name="status_enum"), nullable=False, default=BlogStatus.DRAFT.value)

    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')

    def __repr__(self):
        return f'<Post {self.title}>'
