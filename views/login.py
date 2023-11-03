from dash import dcc, html
from dash.dependencies import Input, Output, State
from server import app
from users_mgt import User
from flask_login import login_user
from werkzeug.security import check_password_hash
from config import collection
from bson.objectid import ObjectId
import dash_mantine_components as dmc
from dash_iconify import DashIconify

# from app import app

layout = dmc.Center(
    [
        dcc.Location(id="url_login", refresh=True),
        dmc.Card(
            children=[
                dmc.CardSection(
                    [
                        dmc.Text("Welcome to Depictio!", size="lg"),
                        dmc.Stack(
                            [
                                dmc.TextInput(label="Email:", id="uname-box"),
                                dmc.PasswordInput(
                                    label="Password:",
                                    id="pwd-box",
                                    placeholder="Enter your password",
                                    icon=DashIconify(icon="bi:shield-lock"),
                                ),
                            ],
                            spacing="1rem",
                        ),
                        dmc.Group(
                            [
                                dcc.Link(
                                    dmc.Text(
                                        "Don't have an account? Register",
                                        color="gray",
                                        size="sm",
                                    ),
                                    href="/register",
                                ),
                                dmc.Button(
                                    "Login",
                                    radius="md",
                                    id="login-button",
                                    n_clicks=0,
                                    # type="submit",
                                ),
                            ],
                            grow=True,
                            mt="1.5rem",
                            noWrap=True,
                            spacing="apart",
                        ),
                    ],
                    inheritPadding=True,
                ),
                html.Div(children="", id="output-state"),
            ],
            withBorder=True,
            shadow="xl",
            radius="lg",
            p="1.5rem",
            style={"width": "420px"},
        ),
    ],
    style={"paddingLeft": "0%", "paddingRight": "30%", "paddingTop": "20%"},
)


@app.callback(
    Output("url_login", "pathname"),
    [
        Input("login-button", "n_clicks"),
        Input("uname-box", "n_submit"),
        Input("pwd-box", "n_submit"),
    ],
    [State("uname-box", "value"), State("pwd-box", "value")],
)
def success(n_clicks, n_submit_uname, n_submit_pwd, input1, input2):
    # If you have a valid ObjectId as a string:
    # user_d_id = ObjectId({"$oid": "64a842842bf4fa7deaa3dbed"})
    # user_d_username = "dev@example.com"  # Replace with a valid username for dev
    # user_d_password = "devpass"  # Replace with a valid password for dev
    # user_d_email = "dev@example.com"  # Replace with a valid email for dev
    # user = User(user_d_username, user_d_password, user_d_email, str(user_d_id))
    # login_user(user)
    # return "/success"

    print(input1, input2)
    if input1 and input2:
        user_d = collection.find_one({"email": input1})
        user_d_id = user_d["_id"]
        user_d_username = user_d["email"]
        user_d_email = user_d["email"]
        user_d_password = user_d["password"]
        user = User(user_d_username, user_d_password, user_d_email, str(user_d_id))

        if user:
            if check_password_hash(user_d_password, input2):
                login_user(user)
                return "/success"
        else:
            pass


@app.callback(
    Output("output-state", "children"),
    [
        Input("login-button", "n_clicks"),
        Input("uname-box", "n_submit"),
        Input("pwd-box", "n_submit"),
    ],
    [State("uname-box", "value"), State("pwd-box", "value")],
)
def update_output(n_clicks, n_submit_uname, n_submit_pwd, input1, input2):
    print("XXXXXXXXXXXXXXXX")
    print(n_clicks)
    print(n_submit_uname)
    print(n_submit_pwd)

    # if n_clicks > 0 or n_submit_uname > 0 or n_submit_pwd > 0:

    if n_clicks > 0:
        # if app.server.config['DEBUG']:
        # Create a mock user or get a development-specific user.

        # login_user(user)

    # elif n_clicks > 0:
        print(input1, input2)
        print(collection.find_one({"email": input1}))
        user_d = collection.find_one({"email": input1})
        user_d_id = user_d["_id"]
        user_d_username = user_d["email"]
        user_d_email = user_d["email"]
        user_d_password = user_d["password"]
        user = User(user_d_username, user_d_password, user_d_email, user_d_id)
        print(user)
        if user:
            if check_password_hash(user_d_password, input2):
                return ""
            else:
                return "Incorrect username or password"
        else:
            return "Incorrect username or password"
    else:
        return ""
