from dash import dcc, html
from dash.dependencies import Input, Output
from server import app
from flask_login import logout_user, current_user
from views import success, login, login_fd, logout, register


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    html.Div(id="page-content"),
                ),
            ],
        ),
        dcc.Location(id="url", refresh=False),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return login.layout
    elif pathname == "/register":
        return register.layout
    elif pathname == "/login":
        return login.layout
    elif pathname == "/success":
        print(current_user)
        print(current_user.is_authenticated)
        if current_user.is_authenticated:
            return success.layout
        else:
            return login_fd.layout
    elif pathname == "/design-visualisation":
        return success.layout
    elif pathname == "/dashboard":
        return success.layout
    elif pathname == "/profile":
        return success.layout
    elif pathname == "/pivot-table":
        return success.layout
    elif pathname == "/logout":
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            return logout.layout
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(debug=True)
