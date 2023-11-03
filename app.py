import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
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


# Global storage for development purposes. Replace with a database in production.


# @app.callback(
#     Output("new-dashboard-output", "children"),
#     [Input("submit-new-dashboard", "n_clicks")],
#     [State("new-dashboard-name", "value")],
#     prevent_initial_call=True,
# )
# def create_new_dashboard(n_clicks, dashboard_name):
#     if dashboard_name:
#         # This is where you would save the dashboard info to your database.
#         # user_dashboards[dashboard_name] = {}  # Placeholder for dashboard configuration

#         return f"Dashboard '{dashboard_name}' created!"
#     return "Please enter a name for the new dashboard."




def generate_dashboard_layout(dashboard_name):
    # Placeholder for generating the dashboard layout based on its configuration.
    # You would customize this function to build the dashboard from the saved config.
    return html.Div(
        [
            html.H2(f"Dashboard: {dashboard_name}"),
            # Add components and layout for this dashboard
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
    # elif pathname == "/design-visualisation":
    #     return success.layout
    # Dynamic dashboards
    elif pathname.startswith("/dashboard/"):
        dashboard_name = pathname.split("/dashboard/")[1]
        print(pathname)
        print(dashboard_name)
        return generate_dashboard_layout(dashboard_name)

    # Settings page
    elif pathname == "/settings":
        return success.layout
    elif pathname == "/profile":
        return success.layout
    # elif pathname == "/pivot-table":
    #     return success.layout
    elif pathname == "/logout":
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            return logout.layout
    else:
        return "404"


if __name__ == "__main__":
    app.run_server(port=9050, debug=True)
