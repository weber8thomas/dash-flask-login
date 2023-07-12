import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


dash.register_page(__name__, path="/profile")


# Define user specifications
user_info = {
    "Name": "User Name",
    "Email": "user@example.com",
    "Phone Number": "1234567890",
    "Location": "Earth",
}

layout = dmc.MantineProvider(
    [
        dbc.Container(
            [
                dmc.Avatar(
                    src="https://e7.pngegg.com/pngimages/799/987/png-clipart-computer-icons-avatar-icon-design-avatar-heroes"
                    "-computer-wallpaper-thumbnail.png",
                    size="lg",
                    radius="xl",
                ),
                html.H2("User Profile", className="mb-5"),

                dbc.ListGroup(
                    [
                        dbc.ListGroupItem([html.Strong(key), ": ", value])
                        for key, value in user_info.items()
                    ],
                    flush=True,
                ),
                html.Br(),
                dbc.NavLink("Logout", href="/logout", className="mt-4"),
            ],
            className="mt-5",
        ),
    ],
    id="themeHolder",
    withNormalizeCSS=True,
    withGlobalStyles=True,
    withCSSVariables=True,
)
