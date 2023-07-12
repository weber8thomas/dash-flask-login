from dash import dcc, html

from dash.dependencies import Input, Output
import dash_mantine_components as dmc
from server import app

# Create app layout
layout = html.Div(
    children=[
        dcc.Location(id="url_logout", refresh=True),
        html.Div(
            className="container",
            children=[
                html.Div(
                    html.Div(
                        className="row",
                        children=[
                            html.Div(
                                className="ten columns",
                                children=[
                                    html.Br(),
                                    html.Div(
                                        "User disconnected - Please login to view the success screen again"
                                    ),
                                ],
                            ),
                            html.Div(
                                className="two columns",
                                # children=html.A(html.Button('LogOut'), href='/')
                                children=[
                                    html.Br(),
                                    # html.Button(id='back-button', children='Go back', n_clicks=0)
                                    dmc.Button(
                                        "Go back",
                                        radius="md",
                                        id="back-button",
                                        n_clicks=0,
                                    ),
                                ],
                            ),
                        ],
                    )
                )
            ],
        ),
    ]
)


# Create callbacks
@app.callback(Output("url_logout", "pathname"), [Input("back-button", "n_clicks")])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return "/"
