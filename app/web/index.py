import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.io as pio
from dash.dependencies import Input, Output

from app import app
from tabs import sidepanel, seasons, races, incidents, drivers


server = app.server
app.title = "F1 Analytics"
pio.templates.default = "simple_white"
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {"margin-left": "18rem", "margin-right": "2rem", "padding": "2rem 1rem"}

content = html.Div(id="page-content", style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidepanel.layout, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/seasons"]:
        return seasons.layout
    elif pathname == "/races":
        return races.layout
    elif pathname == "/incidents":
        return incidents.layout
    elif pathname == "/drivers":
        return drivers.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=5012)
