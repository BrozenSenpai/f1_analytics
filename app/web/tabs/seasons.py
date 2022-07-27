import requests
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

from app import app
from components import (
    simple_table,
    stats_card,
    header_layout_with_dropdown,
    dropdown,
    bar_chart,
    now,
    seasons,
)


layout = header_layout_with_dropdown(
    "seasons-page",
    dropdown(seasons, "season-drop", "Select a season", now, False, True),
    "Seasons",
)


@app.callback(Output("seasons-page", "children"), [Input("season-drop", "value")])
def update_page(year_check):
    drivers = requests.get(
        f"http://f1analytics-api:5011/api/drivers_seasons/{year_check}"
    ).json()
    constructors = requests.get(
        f"http://f1analytics-api:5011/api/constructors_seasons/{year_check}"
    ).json()
    df_driv = pd.DataFrame(drivers)
    df_const = pd.DataFrame(constructors)

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            simple_table(
                                df_driv,
                                "drivers-rank",
                                ["Season", "Nationality", "Podiums"],
                                12,
                            )
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            bar_chart(
                                df_driv[(df_driv["Podiums"] > 0)],
                                "podiums-driv-bar",
                                "Driver",
                                "Podiums",
                                "Podiums",
                            )
                        ],
                        width=7,
                    ),
                    dbc.Col(
                        children=[
                            stats_card("Points", df_driv["Points"].sum()),
                            html.Br(),
                            stats_card("Drivers", df_driv["Driver"].nunique()),
                            html.Br(),
                            stats_card(
                                "Nationalities", df_driv["Nationality"].nunique()
                            ),
                        ],
                        width=2,
                    ),
                ]
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        simple_table(
                            df_const,
                            "constructors-rank",
                            ["Season", "Nationality", "Podiums"],
                            12,
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        bar_chart(
                            df_const[(df_const["Podiums"] > 0)],
                            "podiums-const-bar",
                            "Constructor",
                            "Podiums",
                            "Podiums",
                        ),
                        width=7,
                    ),
                    dbc.Col(
                        children=[
                            stats_card("Points", df_const["Points"].sum()),
                            html.Br(),
                            stats_card(
                                "Constructors", df_const["Constructor"].nunique()
                            ),
                            html.Br(),
                            stats_card(
                                "Nationalities",
                                df_const["Nationality"].nunique(),
                            ),
                        ],
                        width=2,
                    ),
                ]
            ),
        ]
    )
