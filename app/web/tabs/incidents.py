import requests
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

from app import app
from components import (
    dropdown,
    pie_chart,
    header_layout_with_dropdown,
    dropdown_check,
    simple_table,
    now,
    seasons,
)


layout = html.Div(
    [
        header_layout_with_dropdown(
            "incidents-header",
            dropdown(seasons, "season-drop", None, now, False, True),
            "Incidents",
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(), width=6),
                dbc.Col(html.Div(id="circuit-drop"), width=2),
                dbc.Col(html.Div(id="driver-drop"), width=2),
                dbc.Col(html.Div(id="constructor-drop"), width=2),
            ]
        ),
        html.Br(),
        html.Div(id="incidents-page"),
    ]
)


@app.callback(
    [
        Output("circuit-drop", "children"),
        Output("driver-drop", "children"),
        Output("constructor-drop", "children"),
    ],
    [Input("season-drop", "value")],
)
def update_dropdowns(year_check):
    incidents = requests.get(
        f"http://f1analytics-api:5011/api/incidents/{year_check}"
    ).json()
    df = pd.DataFrame(incidents)

    circuit = dropdown(df.Circuit, "circuit-d", "Select a circuit", None, True, False)
    driver = dropdown(df.Driver, "driver-d", "Select drivers", None, True, False)
    constructor = dropdown(
        df.Constructor, "constructor-d", "Select constructors", None, True, False
    )
    return circuit, driver, constructor


@app.callback(
    Output("incidents-page", "children"),
    [
        Input("season-drop", "value"),
        Input("circuit-d", "value"),
        Input("driver-d", "value"),
        Input("constructor-d", "value"),
    ],
)
def update_page(year_check, circuit, driver, constructor):
    incidents = requests.get(
        f"http://f1analytics-api:5011/api/incidents/{year_check}"
    ).json()
    df = pd.DataFrame(incidents)
    df = dropdown_check(df, circuit, "Circuit")
    df = dropdown_check(df, driver, "Driver")
    df = dropdown_check(df, constructor, "Constructor")

    if len(df) != 0:
        return html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [pie_chart(df, "status-pie", "Incident", None, "Incidents")]
                        )
                    ]
                ),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            [simple_table(df, "status-table", ["Season", "Date"], 20)]
                        )
                    ]
                ),
            ]
        )
    return html.Div([html.P("No incidents for this combination of dropdowns")])
