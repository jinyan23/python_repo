# Import modules
from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


# Import custom module
from bus import bus


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)


sidebar_style = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

content_style = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H3("Bus Arrival App", className="display-4"),
        html.Hr(),              # Draws a horizontal line
        html.P("Enter Bus Stop ID Below", className="lead"),
        dcc.Input(id="my-input", value='04111', type='text'),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Map", href="/map", active="exact"),
                dbc.NavLink("Service Route", href="/service-route", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=sidebar_style,
)


content = html.Div(id="page-content", style=content_style)


# Set the content of the pages here
pone_content = html.Div(children=[
    html.H4("Bus Arrival Timings"),
    html.Div(id="my-output")
])

ptwo_content = html.Div(children=[
    html.H4("Map of Bus Stop Location"),
    html.Div(children="Work In Progress")])
pthree_content = html.Div(children=[
    html.H4("Service Route of Bus"),
    html.Div(children="Work In Progress")])


# app.layout
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# app.callback for navigation panel
@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname")
    )
def render_page_content(pathname):
    if pathname == "/":
        return pone_content
    elif pathname == "/map":
        return ptwo_content
    elif pathname == "/service-route":
        return pthree_content
    
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


# app.callback for bus arrival timing
@app.callback(
    Output(component_id="my-output", component_property="children"),
    Input(component_id="my-input", component_property="value")
)
def update_table(input_value):
    
    df, err_message = bus(input_value)
    
    return html.Table([
        
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns  # type: ignore
            ]) for i in range(min(len(df), 30))
        ])
        
    ])

if __name__ == "__main__":
    app.run_server(debug=True)