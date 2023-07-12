from dash import Dash
from flask_login import LoginManager, UserMixin
from users_mgt import User
from config import collection
from flask_session import Session
import dash_bootstrap_components as dbc
from bson.objectid import ObjectId

app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.2.1/css/all.min.css",
    ],
    use_pages=True,
    suppress_callback_exceptions = True
)
server = app.server


server.config.update(
    SECRET_KEY="secret_key",
    # SECRET_KEY=os.urandom(12),
    SESSION_TYPE="filesystem",
    SESSION_FILE_DIR="flask_session",
)


Session(app)


app.config.suppress_callback_exceptions = True

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"





@login_manager.user_loader
def load_user(user_id):
    user_d = collection.find_one({"_id": ObjectId(user_id)})
    user_d_id = user_d["_id"]
    user_d_username = user_d["email"]
    user_d_email = user_d["email"]
    user_d_password = user_d["password"]
    u = User(user_d_username, user_d_password, user_d_email, user_d_id)
    # print(u)
    if not u:
        return None
    return u
