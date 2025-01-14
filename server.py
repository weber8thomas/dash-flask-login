# Dash app initialization
import dash
# User management initialization
import os
from flask_login import LoginManager, UserMixin
from users_mgt import db, User as base
from config import config


app = dash.Dash(
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


# config
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Create User class with UserMixin
class User(UserMixin, base):
    pass


from sqlalchemy import select
from sqlalchemy.orm import Session
from config import engine

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    # print(User.query.get(int(user_id)))
    # return User.query.get(int(user_id))
    with Session(engine) as session:
        user = session.get(User, user_id)
        return user
    # with Session(engine) as session:
    #     statement = select(User).filter_by(username=user_id)
    #     result = session.execute(statement)
    #     user = result.scalars().first()
    #     return user
