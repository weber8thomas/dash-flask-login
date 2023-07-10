# index page
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from server import app, server
from flask_login import logout_user, current_user
from views import success, login, login_fd, logout

# header = html.Div(
#     className='header',
#     children=html.Div(
#         className='container-width',
#         style={'height': '100%'},
#         children=[
#             html.Img(
#                 src='assets/dash-logo-stripe.svg',
#                 className='logo'
#             ),
#             html.Div(className='links', children=[
#                 html.Div(id='user-name', className='link'),
#                 html.Div(id='logout', className='link')
#             ])
#         ]
#     )
# )

app.layout = html.Div(
    [
        
        # header,
        html.Div([
            html.Div(
                html.Div(id='page-content', 
                        #  className='content'
                         ),
                # className='content-container'
            ),
        ], 
        # className='container-width'
        ),
        dcc.Location(id='url', refresh=False),
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':

        return login.layout
    elif pathname == '/login':
        return login.layout
    elif pathname == '/success':
        # print(current_user)
        # print(current_user.is_authenticated)
        # if current_user.is_authenticated:
        return success.layout
        # else:
        #     return login_fd.layout
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            return logout.layout
    else:
        return '404'




if __name__ == '__main__':
    app.run_server(debug=True)