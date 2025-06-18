from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.services.auth_service import generate_jwt
from app import db

auth_bp = Blueprint('auth', __name__)


# User registration route
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
    
        if not username or not password or not email:
            return jsonify({"error": "Missing required fields"}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 409
        
        #Register the user
        hashed_password = generate_password_hash(password)
        newUser = User(username=username, email=email, password_hash=hashed_password)
    
        db.session.add(newUser)
        db.session.commit()
    
        return jsonify({"message": "User registered successfully", "username": username}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred during registration", "details": str(e)}), 500

# User login route
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    
        if not username or not password:
            return jsonify({"error": "Missing required fields"}), 400
    
        user = User.query.filter_by(username=username).first()
    
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401
    
        # Generate JWT token
        access_token = generate_jwt(user.id, user.username)
    
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    
    except Exception as e:
        return jsonify({"error": "An error occurred during login", "details": str(e)}), 500
