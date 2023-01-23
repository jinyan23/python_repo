# Import modules
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# Import custom functions
from bus import bus

app = Dash(__name__)

# dbc not working yet
app.layout = html.Div([
    
    dbc.Row([
        
        dbc.Col(html.Label("Insert Bus Stop ID: "), md=4),
        dbc.Col(html.Label("Another Column"), md=8)
    
    ]),
    
    # dcc Callback
    dbc.Row([
        dbc.Col(children=[]),
        dcc.Input(id="my-input", value='04111', type='text')
    ]),
        
    html.H4(children="Bus Arrival Timings"),
    html.Div(id="my-output")
        
])

@app.callback(
    Output(component_id="my-output", component_property="children"),
    Input(component_id="my-input", component_property="value")
)
def update_table(input_value):
    
    df = bus(input_value)
    
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

