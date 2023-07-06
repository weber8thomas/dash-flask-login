from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from config import db, collection

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        user = collection.find_one({'username': user_id})
        if not user:
            return None
        return User(username=user['username'], password=user['password'])


# class User(UserMixin):

#     def __init__(self, username, email, password, _id=None):
#         self._id = _id
#         self.username = username
#         self.email = email
#         self.password = password

#     @staticmethod
#     def add_user(username, password, email):
#         hashed_password = generate_password_hash(password, method='sha256')

#         new_user = {
#             "username": username, 
#             "email": email, 
#             "password": hashed_password
#         }

#         User.collection.insert_one(new_user)

#     @staticmethod
#     def del_user(username):
#         User.collection.delete_one({"username": username})

#     @staticmethod
#     def show_users():
#         users = User.collection.find({}, {"username": 1, "email": 1})

#         for user in users:
#             print(user)

#     @staticmethod
#     def find_by_id(user_id):
#         user_data = User.collection.find_one({"_id": ObjectId(user_id)})
#         if user_data:
#             return User(user_data["username"], user_data["email"], user_data["password"], user_data["_id"])
#         return None

#     @staticmethod
#     def find_by_username(username):
#         user_data = User.collection.find_one({"username": username})
#         if user_data:
#             return User(user_data["username"], user_data["email"], user_data["password"], user_data["_id"])
#         return None

#     def get_id(self):
#         return str(self._id)
