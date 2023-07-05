from sqlalchemy import Table
from sqlalchemy.sql import select
from sqlalchemy.orm import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from config import engine

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


# User_tbl = Table('user', User.metadata)


def create_user_table():
    User.metadata.create_all(engine)

def delete_user_table():
    User.__table__.drop(engine)


def add_user(username, password, email):
    hashed_password = generate_password_hash(password, method='sha256')

     # Create a new User object
    new_user = User(username=username, email=email, password=hashed_password)

    # Create a new session
    session = Session(engine)

    # Add the new user to the session
    session.add(new_user)

    # Commit the session to write the new user to the database
    session.commit()

    # Close the session to end the transaction
    session.close()

# def add_user(username, password, email):
#     hashed_password = generate_password_hash(password, method='sha256')

#     ins = User_tbl.insert().values(
#         username=username, email=email, password=hashed_password)

#     conn = engine.connect()
#     conn.execute(ins)
#     conn.close()



def del_user(username):
    # Create a new session
    session = Session(engine)

    # Find the user to delete
    user_to_delete = session.query(User).filter(User.username == username).first()

    if user_to_delete is not None:
        # Delete the user and commit the changes
        session.delete(user_to_delete)
        session.commit()

    # Close the session to end the transaction
    session.close()

# def del_user(username):
#     delete = User_tbl.delete().where(User_tbl.c.username == username)

#     conn = engine.connect()
#     conn.execute(delete)
    # conn.close()


def show_users():
    session = Session(engine)  # create a Session using your engine

    users = session.query(User.username, User.email).all()  # perform the query

    for user in users:
        print(user)

    session.close() 

# def show_users():
#     select_st = select([User_tbl.c.username, User_tbl.c.email])

#     conn = engine.connect()
#     rs = conn.execute(select_st)

#     for row in rs:
#         print(row)

#     conn.close()
