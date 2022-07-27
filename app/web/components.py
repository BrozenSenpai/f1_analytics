import requests

import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
import plotly.express as px


seasons = [
    x["Season"] for x in requests.get("http://f1analytics-api:5011/api/seasons").json()
]

now = seasons[0]

drivers = [
    x["driver"] for x in requests.get("http://f1analytics-api:5011/api/drivers").json()
]


def nav_button(title, href, component_id):
    # Generate navigation button
    return dbc.Button(
        dbc.NavLink(
            title,
            href=href,
            id=component_id,
            style={"color": "black"},
        ),
        color="primary",
        outline=True,
    )


def dropdown(data, component_id, placeholder, value, multi, reverse):
    # Make a dropdown
    return dcc.Dropdown(
        id=component_id,
        options=[{"label": j, "value": j} for j in sorted(set(data), reverse=reverse)],
        optionHeight=60,
        placeholder=placeholder,
        value=value,
        clearable=False,
        multi=multi,
    )


def header_layout_with_dropdown(component_id, drop, title):
    # Make a layout contains header and dropdown
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.Div([html.H2(title)])),
                    dbc.Col(html.Div([html.Div([drop])]), width=2),
                ]
            ),
            html.Hr(),
            html.Div(id=component_id),
        ]
    )


def dropdown_check(df, selector, ds):
    # "Make dropdowns work
    if (
        selector is None or len(selector) == 0
    ):  # Make sure filter is not empty, if yes return
        # full dataframe
        return df
    df = df.loc[df[ds].isin(selector)]  # Filter dataframe
    return df


def simple_table(df, component_id, col_list, page_size):
    # Generate simple table
    return dash_table.DataTable(
        id=component_id,
        columns=[
            {"name": i, "id": i} for i in df.columns if i not in col_list
        ],  # Reject
        # unwanted columns
        data=df.to_dict("records"),
        page_size=page_size,
        style_cell={"border": "1px solid black", "font-family": "Lato"},
    )


def pie_chart(df, component_id, names, values, title):
    # Plot pie chart
    return dcc.Graph(
        id=component_id,
        figure=px.pie(
            data_frame=df, names=names, values=values, title=title
        ).update_layout(font={"family": "Lato"}),
    )


def stats_card(title, text):
    # Generate bootstrap info cards
    card_content = [dbc.CardHeader(title), dbc.CardBody(html.H5(str(text)))]
    return dbc.Card(card_content, color="primary", outline=True)


def bar_chart(df, component_id, x, y, title):
    # Plot bar chart
    return dcc.Graph(
        id=component_id,
        figure=px.bar(data_frame=df, x=x, y=y, title=title).update_xaxes(
            categoryorder="total descending"
        ),
    )


def box_plot(df, component_id, x, y, hover, color, title):
    # Plot box plot
    return dcc.Graph(
        id=component_id,
        figure=px.box(
            df,
            x=x,
            y=y,
            hover_data=hover,
            points="all",
            color=color,
            title=title,
        ),
    )


def scatter(df, component_id, x, y, color, title, hover):
    # Scatter plot
    return dcc.Graph(
        id=component_id,
        figure=px.line(
            df, x=x, y=y, color=color, title=title, text=hover
        ).update_traces(mode="markers"),
    )
