import base64
import calendar
import datetime
import hashlib
import hmac
import jwt

from flask import request
from flask_restx import abort

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, JWT_SECRET, JWT_ALGORITHM
from implemented import user_service


def auth_check():
    if 'Authorization' not in request.headers:
        return False
    token = request.headers['Authorization'].split("Bearer ")[-1]
    return jwt_decode(token)


def jwt_decode(token):
    try:
        decoded_jwt = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        return False
    else:
        return decoded_jwt


def auth_required(func):
    def wrapper(*args, **kwargs):
        if auth_check():
            return func(*args, **kwargs)
        abort(401, "Authorization error")
    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        decoded_jwt = auth_check()
        if decoded_jwt:
            role = decoded_jwt.get("role")
            if role == "admin":
                return func(*args, **kwargs)
        abort(401, "Admin role required")
    return wrapper



def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {'access token': access_token, 'refresh token':refresh_token}

def compare_passwords(password_hash, other_password):
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        hashlib.pbkdf2_hmac('sha256', other_password.encode(), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
    )

def login_user(req_json):
    user_name = req_json.get("username")
    user_password = req_json.get("password")
    if user_name and user_password:
        user = user_service.get_filter({"username": user_name})
        if user:
            pass_hashed = user[0].password
            req_json["role"] = user[0].role
            if compare_passwords(pass_hashed, user_password):
                return generate_token(req_json)
    return False

def refresh_user_token(req_json):
    refresh_token = req_json.get("refresh_token")
    data = jwt_decode(refresh_token)
    if data:
        token = generate_token(data)
        return  token
    return False