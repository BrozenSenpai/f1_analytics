import requests
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

from app import app
from components import header_layout_with_dropdown, simple_table, dropdown, now, seasons


layout = header_layout_with_dropdown(
    "races-page",
    dropdown(seasons, "season-drop", "Select a season", now, False, True),
    "Grands Prix",
)


@app.callback(Output("races-page", "children"), [Input("season-drop", "value")])
def update_page(year_check):
    races = requests.get(f"http://f1analytics-api:5011/api/races/{year_check}").json()
    df = pd.DataFrame(races)
    df = df[
        [
            "Season",
            "Date",
            "Grand Prix",
            "Circuit",
            "Winner",
            "Constructor",
            "Location",
            "lat",
            "lng",
        ]
    ]
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lng"] = pd.to_numeric(df["lng"], errors="coerce")
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Graph(
                                id="gp_map",
                                figure=px.scatter_mapbox(
                                    data_frame=df,
                                    lat="lat",
                                    lon="lng",
                                    hover_name="Circuit",
                                    hover_data={
                                        "Location": True,
                                        "lat": False,
                                        "lng": False,
                                    },
                                    zoom=1,
                                ).update_layout(mapbox_style="carto-positron"),
                            )
                        ]
                    )
                ]
            ),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        simple_table(
                            df,
                            "races-table",
                            ["year", "lat", "lng", "Location"],
                            len(df),
                        )
                    )
                ]
            ),
        ]
    )
