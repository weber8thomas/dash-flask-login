import os
from flask import Flask
from dash import Dash
from flask_login import LoginManager, UserMixin
from config import client, config
from users_mgt import db, User as base

app = Dash(
    __name__,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ]
)
server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# db.init_app(server)

# server.config.update(
#     SECRET_KEY=os.urandom(12),
#     MONGODB_SETTINGS={
#         'db': config.get('database', 'db'),
#         'host': config.get('database', 'host'),
#         'port': config.get('database', 'port')
#     }
# )

server.config.update(
    SECRET_KEY=os.urandom(12),
)




# Create User class with UserMixin
# class User(UserMixin, base):
#     pass


app.config.suppress_callback_exceptions = True

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    # user = User.get(user_id)
    print(user)
    if user:
        return user
    else:
        return None
    

