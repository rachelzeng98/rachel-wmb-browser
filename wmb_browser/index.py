"""Main app entry point and routing control."""
import dash_bootstrap_components as dbc
from _app import APP_ROOT_NAME, app, server
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from wmb_browser.apps.dynamic_browser import create_dynamic_browser_layout

LOGO_IMG_URL = (
    "https://raw.githubusercontent.com/lhqing/wmb-browser/master/"
    "wmb_browser/assets/dissection_region_img/navbar_icon.gif"
)


def get_header():
    """Add header to the app."""
    nav = dbc.Row(
        [
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Home", href=f"/{APP_ROOT_NAME}home")),
                ],
                className="mr-5",
                navbar=True,
                style={"font-size": "1.4em"},
            )
        ],
        className="ml-2 flex-nowrap mt-3 mt-md-0",
        align="center",
    )

    navbar = dbc.Navbar(
        [
            html.A(
                dbc.Row([dbc.Col(html.Img(src=LOGO_IMG_URL, height="50px"))], align="left", className="g-0"),
                href=f"/{APP_ROOT_NAME}",
                className="mx-3",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(nav, id="navbar-collapse", navbar=True),
        ],
        color="light",
        className="fixed-top mb-2 p-2",
    )
    return navbar


# make sure IDE do not remove the import line...
# because server need to be imported by wsgi.py from index.py
# all orders matters here
type(server)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        get_header(),  # nav bar
        html.Div(
            id="page-content",
            # Global style of all APPs
            className="page-content",
        ),
    ]
)


@callback(
    Output("page-content", "children"), [Input("url", "pathname")], [State("url", "search"), State("url", "href")]
)
def display_page(pathname, search, total_url):
    """Routing control."""
    app_layout = []
    # search_dict = search_to_dict(search)

    if pathname is None:
        # init callback url is None
        raise PreventUpdate
    elif (pathname == f"/{APP_ROOT_NAME}home") or (pathname == f"/{APP_ROOT_NAME}"):
        layout = []  # home_layout
    elif pathname == f"/{APP_ROOT_NAME}dynamic_browser":
        layout = create_dynamic_browser_layout()
    # add layout functions here based on pathname
    # elif pathname == f"/{APP_ROOT_NAME}app1":
    #     layout = app1_layout(search_dict)
    else:
        layout = None

    # final validate, if any parameter does not found, layout is None
    if layout is None:
        return "404"
    else:
        app_layout.append(layout)
    return app_layout


if __name__ == "__main__":
    app.run(debug=True, port="1234")
