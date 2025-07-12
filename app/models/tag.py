from app import db

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(40), nullable=False, unique=True)

    posts = db.relationship('Post', secondary='post_tags', back_populates='tags')