from flask_login import current_user
from server import app
from dash import Dash, html, dcc, Input, Output, State, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from pages import design_visualisation, pivot_table, dashboard, profile


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


# links with text
nav_links_text = [
    dbc.NavLink(
        [html.I(className="fas fa-home"), " Home"],
        href="/success",
        active="exact",
    ),
    dbc.NavLink(
        [html.I(className="fas fa-palette"), " Visualisation design"],
        href="/design-visualisation",
        active="exact",
    ),
    dbc.NavLink(
        [html.I(className="fas fa-th-large"), " Dashboard design"],
        href="/dashboard",
        active="exact",
    ),
    dbc.NavLink(
        [html.I(className="fas fa-search"), " Data exploration"],
        href="/pivot-table",
        active="exact",
    ),
]

# links without text (icons only)
nav_links_icon = [
    dbc.NavLink(
        html.I(className="fas fa-home"),
        href="/success",
        active="exact",
    ),
    dbc.NavLink(
        html.I(className="fas fa-palette"),
        href="/design-visualisation",
        active="exact",
    ),
    dbc.NavLink(
        html.I(className="fas fa-th-large"),
        href="/dashboard",
        active="exact",
    ),
    dbc.NavLink(
        html.I(className="fas fa-search"),
        href="/pivot-table",
        active="exact",
    ),
]

# use the Collapse component to animate hiding / revealing links
collapse = dbc.Collapse(
    dbc.Nav(
        id="nav_links",
        vertical=True,
        pills=True,
    ),
    id="collapse",
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
        # collapse,
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink(
                        [html.I(className="fas fa-home"), " Home"],
                        href="/success",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-palette"), " Visualisation design"],
                        href="/design-visualisation",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-th-large"), " Dashboard design"],
                        href="/dashboard",
                        active="exact",
                    ),
                    dbc.NavLink(
                        [html.I(className="fas fa-search"), " Data exploration"],
                        href="/pivot-table",
                        active="exact",
                    ),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.NavLink(
                        dmc.Avatar(
                            src="https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes"
                            "-computer-wallpaper-thumbnail.png",
                            size="lg",
                            radius="xl",
                        ),
                        href="/profile",
                        target="_blank",
                        style={
                            "display": "block",
                            "width": "100%",
                            "marginBottom": "10px",
                            "position": "absolute",
                            "bottom": "0",
                        },
                    )
                ),
                dbc.Col(
                    dbc.NavLink(
                        html.Div(
                            ["User name"],
                            id="user-name",
                        ),
                        href="/profile",
                        target="_blank",
                        style={
                            "position": "absolute",
                            "bottom": "0",
                            "marginBottom": "22px",
                            "marginLeft": "-90px",
                        },
                    )
                ),
            ]
        ),
    ],
    className="sidebar",
    id="sidebar",
)


content = html.Div(id="page-content-success")


# @app.callback(Output("nav_links", "children"), [Input("sidebar", "className")])
# def update_nav_links(className):
#     print(className)
#     if className == "collapsed":
#         print("TOTO")
#         return nav_links_icon
#     else:
#         return nav_links_text


@app.callback(Output("page-content-success", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/success":
        return html.P("This is the content of the home page!")
    elif pathname == "/design-visualisation":
        return design_visualisation.layout
    elif pathname == "/dashboard":
        return dashboard.layout
    elif pathname == "/pivot-table":
        return pivot_table.layout
    elif pathname == "/profile":
        return profile.layout


@app.callback(
    Output("sidebar", "className"),
    Output("page-content", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
    [State("page-content", "className")],
)
def toggle_classname(n, sidebar_classname, content_classname):
    if n:
        if sidebar_classname == "":
            return "collapsed", "collapsed"
        else:
            return "", ""
    return sidebar_classname, content_classname


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
        return html.Div(current_user.username)
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
    dbc.Row(
        [
            dbc.Col(
                sidebar,
                width={"size": 3, "order": 1, "offset": 2},
                id="sidebar-container",
            ),
            dbc.Col(content, width={"size": 9, "order": 2}, id="content-container"),
        ]
    )
)
