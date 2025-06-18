from flask_jwt_extended import create_access_token
from datetime import timedelta

def generate_jwt(user_id, username):
    expires = timedelta(days=5)
    return create_access_token(
        identity={"user_id": user_id, "username": username},
        expires_delta=expires
    )