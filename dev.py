from config import db, collection
from users_mgt import User
from werkzeug.security import generate_password_hash, check_password_hash

username = "TOTO"
password = "TOTO"
email = "toto@toto.com"

hashed_password = generate_password_hash(password, method='sha256')

new_user = {
    "username": username, 
    "email": email, 
    "password": hashed_password
}

collection.insert_one(new_user)