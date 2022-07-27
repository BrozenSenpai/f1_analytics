import requests
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

from app import app
from components import (
    box_plot,
    header_layout_with_dropdown,
    dropdown,
    stats_card,
    scatter,
    drivers,
)


layout = header_layout_with_dropdown(
    "drivers-page",
    dropdown(
        drivers, "driver-info-drop", "Select a driver", "Pierre Gasly", False, False
    ),
    "Driver Overview",
)


@app.callback(Output("drivers-page", "children"), [Input("driver-info-drop", "value")])
def update_page(driver_check):
    drivers_info = requests.get(
        f"http://f1analytics-api:5011/api/drivers_performance/{driver_check}"
    ).json()
    df_drivers_info = pd.DataFrame(drivers_info)
    df_drivers_info["Points"] = pd.to_numeric(
        df_drivers_info["Points"], errors="coerce"
    )
    df_drivers_info["Position"] = pd.to_numeric(
        df_drivers_info["Position"], errors="coerce"
    )
    df_drivers_info["Grid"] = pd.to_numeric(df_drivers_info["Grid"], errors="coerce")
    df_drivers_info["Round"] = pd.to_numeric(df_drivers_info["Round"], errors="coerce")

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            stats_card(
                                "Races", df_drivers_info["Driver"].value_counts().sum()
                            )
                        ]
                    ),
                    dbc.Col(
                        [
                            stats_card(
                                "Wins",
                                df_drivers_info[(df_drivers_info["Position"] == 1)]
                                .value_counts()
                                .sum(),
                            )
                        ]
                    ),
                    dbc.Col(
                        [
                            stats_card(
                                "Podiums",
                                df_drivers_info.query("Position in [1, 2, 3]")
                                .value_counts()
                                .sum(),
                            )
                        ]
                    ),
                    dbc.Col(
                        [
                            stats_card(
                                "Pole Positions",
                                df_drivers_info[(df_drivers_info["Grid"] == 1)]["Grid"]
                                .value_counts()
                                .sum(),
                            )
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            box_plot(
                                df_drivers_info,
                                "drivers-info-const-box",
                                "Constructor",
                                "Position",
                                ["Season", "Round", "Circuit"],
                                None,
                                "Performance by team",
                            )
                        ]
                    ),
                    dbc.Col(
                        [
                            scatter(
                                df_drivers_info,
                                "drivers_info_scatter",
                                "Round",
                                "Points",
                                "Season",
                                "Total points by round per season",
                                df_drivers_info["Circuit"],
                            )
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            box_plot(
                                df_drivers_info,
                                "drivers-info-circuits-box",
                                "Circuit",
                                "Position",
                                ["Season", "Round", "Constructor"],
                                None,
                                "Performance by circuit",
                            )
                        ]
                    )
                ]
            ),
        ]
    )
