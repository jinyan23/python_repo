# Import modules
import warnings
from dash import Dash, html, dcc, Input, Output, State
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Import custom module
from bus import bus, route, nearest

warnings.filterwarnings('ignore')

#-------------------------------#
# Python dash app style sheets. #
#-------------------------------#


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)


#------------------------------------------------------#
# Setting the styles of the sidebar and content pages. #
#------------------------------------------------------#


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
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Bus Arrival", href="/bus-arrival", active="exact"),
                dbc.NavLink("Nearest Bus Stops", href="/nearest", active="exact"),
                dbc.NavLink("Service Route", href="/service-route", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=sidebar_style,
)
content = html.Div(id="page-content", style=content_style)


#--------------------------------------------#
# Set the content of the content pages here. #
#--------------------------------------------#


phome_content = html.Div(children=[
    html.H3("Bus Arrival Application"),
    html.P("This is a web application that displays bus arrival timings, bus routes and locations of bus stops in Singapore. Data is retrieved via LTA Datamall API calls. This application displayed on the browser using Python Dash interactive interface.")
])
pone_content = html.Div(children=[
    html.H4("Bus Arrival Timings"),
    html.P("The timings are in minutes. (E.g. 4 = 4 minutes till bus arrival at queried bus stop.) If the bus is arriving within a minute, it'll show 'Arr'. If the cell is empty, it means the LTA Datamall doesn't the data for it. It might also mean the last service or certain gaps between two services that are not yet updated."),
    html.P("Enter Bus Stop Code", className="lead"),
    dcc.Input(id="my-input", value='04111', type='text'),
    html.Button("Submit", id="arr-button", n_clicks=0),
    html.Hr(),
    html.Div(id="my-output"),
])
ptwo_content = html.Div(children=[
    html.H4("List of Bus Stops"),
    html.Div(children=[
        html.P("In mobile application for nearest bus stops display, the geolocation of the individual can be obtained via the GPS service available on the phone. However, for this web application, that service is unavailable. Thus, the geolocation for this demonstration is hard coded in. For mobile app, the geolocation will be updated, and the data will be used to calculate the distance to the nearest bus stops, thus allowing the display of the list of bus stops within the near vicinity of the individual."),
        html.P("The bus stops displayed here are within 500 metres from this coordinates: [1.310429, 103.854368] along Serangoon Road near Farrer Park MRT Station."),
        dcc.Input(id="near-input", value="1.310429, 103.854368", type='text'),
        html.Button("Submit", id="near-button", n_clicks=0),
        html.Hr()
    ]),
    html.Div(id="near-output")
])
pthree_content = html.Div(children=[
    html.H4("Service Route of Bus"),
    html.Div(children=[
        html.P("Enter Bus Service Number", className="lead"),
        dcc.Input(id="service-input", value='124', type='text'),
        html.Button("Submit", id="service-button", n_clicks=0),
        html.Hr(),
        dcc.Graph(id="map-output")
    ])])


#------------------------------------------#
# Determine the layout of the application. #
#------------------------------------------#


# app was instantiated with Dash() above. 
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


#--------------------------------------------#
# Interactive callbacks for the application. #
#--------------------------------------------#


# Display content page based on selection in sidebar.
@app.callback(
    Output("page-content", "children"), 
    Input("url", "pathname")
    )
def render_page_content(pathname):
    if pathname == "/":
        return phome_content
    elif pathname == "/bus-arrival":
        return pone_content
    elif pathname == "/nearest":
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


table_style = dict(border="2px solid",
                       width="80%",
                       textAlign="center")
    
head_style = dict(fontSize="20px", 
                  backgroundColor="#003000",
                  color="white")
    
body_style = dict(border="1px solid",
                  borderLeft="1px solid",
                  borderRight="1px solid",)

# app.callback for bus arrival timing (pane 1)
@app.callback(
    Output(component_id="my-output", component_property="children"),
    Input(component_id="arr-button", component_property="n_clicks"),
    State(component_id="my-input", component_property="value")
)
def update_table(n_clicks, input_value):
    
    df, err_message = bus(input_value)
    
    return html.Table([
        
        html.Thead(
            html.Tr([html.Th(col, style=head_style) for col in df.columns])
        ),
        
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col], style=body_style) for col in df.columns  # type: ignore
            ], style=body_style) for i in range(min(len(df), 30))
        ]),
           
    ],
    
    style=table_style
    
    )

# app.callback for nearest bus list (pane 2)
@app.callback(
    Output(component_id="near-output", component_property="children"),
    Input(component_id="near-button", component_property="n_clicks"),
    State(component_id="near-input", component_property="value")
)
def update_bus_stops(n_clicks, input_value):
    
    bs_output = nearest(input_value)
        
    return html.Table([
        
        html.Thead(
            html.Tr([html.Th(col, style=head_style) for col in bs_output.columns])
        ),
        
        html.Tbody([
            html.Tr([
                html.Td(bs_output.iloc[i][col], style=body_style) for col in bs_output.columns  # type: ignore
            ]) for i in range(min(len(bs_output), 30))
        ])
        
    ],
                      
    style=table_style
    
    )

# app.callback for bus route map (pane 3)
@app.callback(
    Output(component_id="map-output", component_property="figure"),
    Input(component_id="service-button", component_property="n_clicks"),
    State(component_id="service-input", component_property="value")
)
def update_map(n_clicks, input_value):
    
    # Retrieve bus stop codes of bus routes for queried bus service number
    q_bus_stops = route(service_num=input_value)
    
    # Plot latitude and longitude of bus stops onto map
    line_trace = go.Scattermapbox(lat=q_bus_stops["latitude"], 
                                  lon=q_bus_stops["longitude"],
                                  mode="lines",
                                  line=go.scattermapbox.Line(width=2, color="blue"),
                                  hoverinfo="none")

    fig = go.Figure(layout=go.Layout(mapbox_style="open-street-map",
                                    mapbox=dict(center=dict(lat=1.349736,
                                                            lon=103.814513),
                                    zoom=10.3)))


    fig.add_trace(line_trace)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                    showlegend=False)
    
    return fig


#------#
# End. #
#------#

if __name__ == "__main__":
    app.run_server(debug=True)