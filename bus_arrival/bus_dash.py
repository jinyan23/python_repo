# Import modules
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Import custom functions
from bus import bus

app = Dash(__name__)

colors = {"background": "#111111",
          "text": "#7FDBFF"}

# Data frame for bus arrival timings here
bus_arrivals = bus()

def generate_table(df, max_rows=20):
    return html.Table([
        
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
        
    ])


app.layout = html.Div([
    
    html.Label("Insert Bus Stop ID: "),
    
    # dcc Callback
    dcc.Input(value='04111', type='text'),
    
    html.Br(),
    
    html.H4(children="Bus Arrival Timings"),
    generate_table(bus_arrivals)
    
])


if __name__ == "__main__":
    app.run_server(debug=True)

# dcc.Dropdown([Input List])
# dcc.RadioItems([Input List])
# dcc.Checklist([Input List])
# dcc.Input(value="default", type="text")
# dcc.Slider(min=0, max=10, **kwargs)
