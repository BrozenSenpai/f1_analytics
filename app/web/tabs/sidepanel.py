import dash_bootstrap_components as dbc
from dash import html

from components import nav_button

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

layout = html.Div(
    [
        html.H2("F1 Analytics", className="display-4"),
        html.Hr(),
        html.P(
            "A simple site for Formula 1 historical statistics overview",
            className="lead",
        ),
        dbc.Nav(
            [
                nav_button("Seasons", "/seasons", "page-1-link"),
                nav_button("Grands Prix", "/races", "page-2-link"),
                nav_button("Drivers", "/drivers", "page-5-link"),
                nav_button("Incidents", "/incidents", "page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
