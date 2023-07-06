# index page
# import dash_core_components as dcc
# import dash_html_components as html
from dash import dcc, html
from dash.dependencies import Input, Output, State
from werkzeug.security import generate_password_hash, check_password_hash

from server import app, server
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
from flask import session
# from views import success, login, login_fd, logout
import logging
from config import config, client, db, collection
from users_mgt import User
logging.basicConfig(level=logging.INFO)


def is_user_authenticated():
    return 'username' in session



header = html.Div(
    className='header',
    children=html.Div(
        className='container-width',
        style={'height': '100%'},
        children=[
            html.Img(
                src='assets/dash-logo-stripe.svg',
                className='logo'
            ),
            html.Div(className='links', children=[
                html.Div(id='user-name', className='link'),
                html.Div(id='logout', className='link')
            ])
        ]
    )
)

app.layout = html.Div(
    [
        dcc.Store(id='session', storage_type='session'),

        header,
        html.Div([
            html.Div(
                html.Div(id='page-content', className='content'),
                className='content-container'
            ),
        ], className='container-width'),
        dcc.Location(id='url', refresh=False),
    ]
)



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
# @login_required
def display_page(pathname):
    logging.info(str(pathname))
    if pathname == '/':
        return layout_login
    elif pathname == '/login':
        return layout_login
    elif pathname == '/success':
        if current_user.is_authenticated:
            return layout_success
        else:
            return layout_login_fd
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return layout_logout
        else:
            return layout_logout
    else:
        return html.Div(html.H5('404'))


@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    if current_user.is_authenticated:
        return html.Div('Current user: ' + current_user.username)
        # 'User authenticated' return username in get_id()
    else:
        return ''


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/logout')
    else:
        return ''



# logout.py


# Create app layout
layout_logout = html.Div(children=[
    dcc.Location(id='url_logout', refresh=True),
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
                                html.Div('User disconnected - Please login to view the success screen again'),
                            ]
                        ),
                        html.Div(
                            className="two columns",
                            # children=html.A(html.Button('LogOut'), href='/')
                            children=[
                                html.Br(),
                                html.Button(id='back-button', children='Go back', n_clicks=0)
                            ]
                        )
                    ]
                )
            )
        ]
    )
])


@app.callback(Output('url_logout', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        logout_user()
        return '/'


# success.py


# Create success layout
layout_success = html.Div(children=[
    dcc.Location(id='url_login_success', refresh=True),
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
                                html.Div('Login successfull'),
                            ]
                        ),
                        html.Div(
                            className="two columns",
                            # children=html.A(html.Button('LogOut'), href='/')
                            children=[
                                html.Br(),
                                html.Button(id='back-button', children='Go back', n_clicks=0)
                            ]
                        )
                    ]
                )
            )
        ]
    )
])


# Create callbacks
@app.callback(Output('url_login_success', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'


# login.py


layout_login = html.Div(
    children=[
        html.Div(
            className="container",
            children=[
                dcc.Location(id='url_login', refresh=True),
                html.Div('''Please log in to continue:''', id='h1'),
                html.Div(
                    children=[
                        dcc.Input(
                            placeholder='Enter your username',
                            n_submit=0,
                            type='text',
                            id='uname-box'
                        ),
                        dcc.Input(
                            placeholder='Enter your password',
                            n_submit=0,
                            type='password',
                            id='pwd-box'
                        ),
                        html.Button(
                            children='Login',
                            n_clicks=0,
                            type='submit',
                            id='login-button'
                        ),
                        html.Div(children='', id='output-state')
                    ]
                ),
            ]
        )
    ]
)

@app.callback(
    Output('session', 'data'),
    [Input('login-button', 'n_clicks')],
    [State('uname-box', 'value'),
     State('pwd-box', 'value')]
)
def store_user_data(n_clicks, input1, input2):
    if n_clicks > 0:
        if input1 and input2:
            user = collection.find_one({'username': input1})
            if user and check_password_hash(user['password'], input2):
                # Store user data in the session
                user_obj = User(username=input1, password=user['password'])
                login_user(user_obj)
                app.logger.info('User login successful: %s', input1)
                return {'username': input1}
        app.logger.info('User login failed')
        return {}



@app.callback(
    Output('output-state', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('session', 'data'),
     State('uname-box', 'value'),
     State('pwd-box', 'value')]
)
def update_output(n_clicks, session_data, input1, input2):
    if n_clicks > 0:  # Check if Login button has been clicked
        logging.info(f"{n_clicks} - {session_data} - {input1} - {input2}")
        if session_data is not None and 'username' in session_data:
            return ''
        elif input1 is not None or input2 is not None:
            return 'Incorrect username or password'
    return ''




# login_fd.py
layout_login_fd = html.Div(children=[
    dcc.Location(id='url_login_df', refresh=True),
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
                                html.Div('User non authenticated - Please login to view the success screen'),
                            ]
                        ),
                        html.Div(
                            className="two columns",
                            # children=html.A(html.Button('LogOut'), href='/')
                            children=[
                                html.Br(),
                                html.Button(id='back-button', children='Go back', n_clicks=0)
                            ]
                        )
                    ]
                )
            )
        ]
    )
])


# Create callbacks
@app.callback(Output('url_login_df', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'


if __name__ == '__main__':
    app.run_server(debug=True)
