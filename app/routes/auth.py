from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.schemas.user_schema import UserSchema
from app.services.auth_service import generate_jwt
from marshmallow import ValidationError
from app import db

auth_bp = Blueprint('auth', __name__)


# User registration route
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        schema = UserSchema()
        data = schema.load(request.get_json())

        name = data['name']
        last_name = data['last_name']
        admin = False  # Default value for admin
        username = data['username']
        password = data['password_hash']
        email = data['email']
        
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 409
        
        #Register the user
        hashed_password = generate_password_hash(password)
        newUser = User(name=name, last_name=last_name, username=username, email=email, password_hash=hashed_password, admin=admin)
    
        db.session.add(newUser)
        db.session.commit()
    
        return jsonify({"message": "User registered successfully", "username": username}), 201
    
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred during registration", "details": str(e)}), 500

# User login route
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        schema = UserSchema(only=('username', 'password_hash'))
        data = schema.load(request.get_json())
        
        username = data['username']
        password = data['password_hash']
    
        user = User.query.filter_by(username=username).first()
    
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401
    
        # Generate JWT token
        access_token = generate_jwt(user.id, user.username)
    
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    
    except ValidationError as err:
        return jsonify({"error": "Validation error", "details": err.messages}), 400
    
    except Exception as e:
        return jsonify({"error": "An error occurred during login", "details": str(e)}), 500
