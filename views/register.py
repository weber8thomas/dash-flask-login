from dash import dcc, html
from dash.dependencies import Input, Output, State
from server import app
from users_mgt import User
from flask_login import login_user
from werkzeug.security import generate_password_hash
from config import collection
import dash_mantine_components as dmc
from dash_iconify import DashIconify

layout = dmc.Center(
    [
        dcc.Location(id="url_register", refresh=True),
        dmc.Card(
            children=[
                dmc.CardSection(
                    [
                        dmc.Text("Welcome to Depictio!", size="lg"),
                        dmc.Text("Please register:", size="s"),
                        dmc.Stack(
                            [
                                dmc.TextInput(label="Email:", id="email-box"),
                                dmc.PasswordInput(
                                    label="Password:",
                                    id="pwd-box",
                                    placeholder="Enter your password",
                                    icon=DashIconify(icon="bi:shield-lock"),
                                ),
                                dmc.PasswordInput(
                                    label="Confirm Password:",
                                    id="confirm-pwd-box",
                                    placeholder="Re-enter your password",
                                    icon=DashIconify(icon="bi:shield-lock"),
                                ),
                            ],
                            spacing="1rem",
                        ),
                        dmc.Group(
                            [
                                dcc.Link(
                                    dmc.Text(
                                        "Already have an account? Login",
                                        color="gray",
                                        size="sm",
                                    ),
                                    href="/login",
                                ),
                                dmc.Button(
                                    "Register",
                                    radius="md",
                                    id="register-button",
                                    n_clicks=0,
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
                html.Div(children="", id="output-state-register"),
            ],
            withBorder=True,
            shadow="xl",
            radius="lg",
            p="1.5rem",
            style={"width": "420px"},
        ),
    ],
    style={"paddingLeft": "0%", "paddingRight": "30%", "paddingTop": "15%"},
)


@app.callback(
    Output("url_register", "pathname"),
    [Input("register-button", "n_clicks")],
    [
        State("email-box", "value"),
        State("pwd-box", "value"),
        State("confirm-pwd-box", "value"),
    ],
)
def register_user(n_clicks, email, password, confirm_password):
    if n_clicks > 0:
        # Check if passwords match
        if password != confirm_password:
            return "/register"  # Redirect user to registration page
        # Check if user already exists
        user_d = collection.find_one({"email": email})
        if user_d is not None:
            return "/register"  # Redirect user to registration page
        # Create new user
        hashed_password = generate_password_hash(password)
        user_id = collection.insert_one(
            {"username": email, "email": email, "password": hashed_password}
        )
        user = User(email, email, hashed_password, str(user_id.inserted_id))
        login_user(user)
        return "/success"  # Redirect user to success page
    return "/register"  # Keep user on registration page


@app.callback(
    Output("output-state-register", "children"),
    [Input("register-button", "n_clicks")],
    [
        State("email-box", "value"),
        State("pwd-box", "value"),
        State("confirm-pwd-box", "value"),
    ],
)
def register_message(n_clicks, email, password, confirm_password):
    if n_clicks > 0:
        if password != confirm_password:
            return "Passwords do not match!"
        user_d = collection.find_one({"email": email})
        print(user_d)
        if user_d is not None:
            return "User already exists!"
        return "Registration successful!"
    return ""
