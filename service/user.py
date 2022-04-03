import base64
import hashlib
import hmac

from constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_filter(self, filter_dict):
        filter_dict_clear = {}
        for key, value in filter_dict.items():
            if value is not None:
                filter_dict_clear[key] = value
        return self.dao.get_filter(filter_dict_clear)

    def create(self, data):
        user_password = data.get("password")
        if user_password:
            data["password"] = get_hash(user_password)
        return self.dao.create(data)

    def update(self, data):
        user_password = data.get("password")
        if user_password:
            data["password"] = get_hash(user_password)
        return self.dao.update(data)

    def delete(self, uid):
        self.dao.delete(uid)


def get_hash(password):
    return base64.b64encode(hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    ))

# def compare_passwords(self, password_hash, other_password) -> bool:
#     return hmac.compare_digest(
#         base64.b64decode(password_hash),
#         hashlib.pbkdf2_hmac('sha256', other_password.encode(), PWD_HASH_SALT, PWD_HASH_ITERATIONS)
#     )