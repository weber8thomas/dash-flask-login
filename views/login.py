import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State

from server import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash

layout = html.Div(
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
            with Session(client) as session:
                statement = select(User).filter_by(username=input1)
                result = session.execute(statement)
                user = result.scalars().first()
                if user and check_password_hash(user.password, input2):
                    # Store user data in the session
                    return {'username': input1}
    return {}

@app.callback(
    Output('url_login', 'pathname'),
    [Input('session', 'data')]
)
def redirect_after_login(session_data):
    if session_data is not None and 'username' in session_data:
        return '/success'
    return ''

@app.callback(
    Output('output-state', 'children'),
    [Input('session', 'data'),
     Input('uname-box', 'value'),
     Input('pwd-box', 'value')]
)
def update_output(session_data, input1, input2):
    if session_data is not None and 'username' in session_data:
        return ''
    elif input1 is not None or input2 is not None:
        return 'Incorrect username or password'
    return ''
