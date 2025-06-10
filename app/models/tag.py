from app import db

# Modelo Tag
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    slug = db.Column(db.String(40), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Tag {self.name}>'