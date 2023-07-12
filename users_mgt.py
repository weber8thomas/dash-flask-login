import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

# from depo.common.database import Database
from config import db, collection as Database
from flask_login import UserMixin
from bson.objectid import ObjectId


class User(UserMixin):
    def __init__(self, username, password, email, _id=None):
        self.username = username
        self.email = email
        self.password = password
        self._id = _id

    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        # print("is_active was called")
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self._id

    @classmethod
    def get_by_username(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        verify_user = User.get_by_email(email)
        if verify_user is not None:
            return check_password_hash(verify_user.password, password)
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(username, password, email)
            new_user.save_to_mongo()
            session["email"] = email
            return True
        else:
            return False

    def json(self):
        return {
            "username": self.username,
            "email": self.email,
            "_id": self._id,
            "password": self.password,
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())
