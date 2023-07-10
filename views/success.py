import warnings

# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_login import logout_user, current_user

from server import app


from dash import Dash, html, dcc, Input, Output, State, dash_table
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import dash

# warnings.filterwarnings("ignore")


# app = dash.Dash(
#     external_stylesheets=[dbc.themes.BOOTSTRAP],
#     # these meta_tags ensure content is scaled correctly on different devices
#     # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
#     meta_tags=[
#         {"name": "viewport", "content": "width=device-width, initial-scale=1"}
#     ],
# )

# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("Depictio", className="display-4")),
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "borderColor": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "borderColor": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "A responsive sidebar layout with collapsible navigation " "links.",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/success", active="exact"),
                    # dbc.NavLink("Page 1", href="/page-1", active="exact"),
                    # dbc.NavLink("Page 2", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
        html.Div(
            className="header",
            children=html.Div(
                className="container-width",
                style={"height": "100%"},
                children=[
                    html.Div(
                        className="links",
                        children=[
                            html.Div(id="user-name", className="link"),
                            html.Div(id="logout", className="link"),
                        ],
                    ),
                ],
            ),
            style={"position": "absolute", "bottom": "0"},
        ),
    ],
    id="sidebar",
    # style={"position": "relative"},
)

content = html.Div(id="page-content-success")

# app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content-success", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/success":
        return html.P("This is the content of the home page!")
    # elif pathname == "/page-1":
    #     return html.P("This is the content of page 1. Yay!")
    # elif pathname == "/page-2":
    #     return html.P("Oh cool, this is page 2!")
    # # If the user tries to reach a different page, return a 404 message
    # return html.Div(
    #     [
    #         html.H1("404: Not found", className="text-danger"),
    #         html.Hr(),
    #         html.P(f"The pathname {pathname} was not recognised..."),
    #     ],
    #     className="p-3 bg-light rounded-3",
    # )


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output("user-name", "children"), [Input("page-content", "children")])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.Div("Current user: " + current_user.username)
        # 'User authenticated' return username in get_id()
    else:
        return ""


@app.callback(Output("logout", "children"), [Input("page-content", "children")])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A("Logout", href="/logout")
    else:
        return ""


layout = html.Div(
    children=[
        html.Div([sidebar, content]),
    ]
)

# Create success layout
# layout = html.Div(
#     children=[
#         html.Div([sidebar, content]),


#         dcc.Location(id="url_login_success", refresh=True),
#         html.Div(
#             className="container",
#             children=[
#                 html.Div(
#                     html.Div(
#                         className="row",
#                         children=[
#                             html.Div(
#                                 className="ten columns",
#                                 children=[
#                                     html.Br(),
#                                     html.Div("Welcome"),
#                                 ],
#                             ),
#                             # html.Div(
#                             #     className="two columns",
#                             #     # children=html.A(html.Button('LogOut'), href='/')
#                             #     children=[
#                             #         html.Br(),
#                             #         html.Button(
#                             #             id="back-button", children="Go back", n_clicks=0
#                             #         ),
#                             #     ],
#                             # ),
#                             # html.Div([dcc.Location(id="url", refresh=False), sidebar, content]),
#                             # html.Div([dcc.Location(id="url"), sidebar, content]),
#                         ],
#                     )
#                 )
#             ],
#         ),
#     ]
# )


# Create callbacks
# @app.callback(
#     Output("url_login_success", "pathname"), [Input("back-button", "n_clicks")]
# )
# def logout_dashboard(n_clicks):
#     if n_clicks > 0:
#         return "/"
