import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_daq as daq
import subprocess

# Create a Dash app
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

# This is for gunicorn
server = app.server

# Read the CSV file and import assets
df = pd.read_csv('csv_data/cansat_data.csv')
cansat_logo = html.Div(html.Img(src = "assets/navdhara_logo.png", height = 70, width = 70))
cansat_text = html.Div(html.Img(src = "assets/navdhara_text.png", height = 70, width = 205))


# Define the layout of your app
#Main dashboard
station_utc = html.Div(
    id="control-panel-station_utc",
    children=[
        daq.LEDDisplay(
            id="control-panel-station_utc-component",
            value="12:00",
            label="Time",
            size=40,
            color="#fec036",
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

cansat_utc = html.Div(
    id="control-panel-cansat_utc",
    children=[
        daq.LEDDisplay(
            id="control-panel-cansat_utc-component",
            value="12:00",
            label="Time",
            size=40,
            color="#fec036",
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

x_speed = html.Div(
    id="control-panel-x_speed",
    children=[
        daq.Gauge(
            id="control-panel-x_speed-component",
            label="X_Speed",
            min=0,
            max=50,
            showCurrentValue=True,
            value=10.000,
            size=175,
            units="1 m/s",
            color="#fec036",
        )
    ],
    n_clicks=0,
)

y_speed = html.Div(
    id="control-panel-y_speed",
    children=[
        daq.Gauge(
            id="control-panel-y_speed-component",
            label="Y_Speed",
            min=0,
            max=50,
            showCurrentValue=True,
            value=10.000,
            size=175,
            units="1 m/s",
            color="#fec036",
        )
    ],
    n_clicks=0,
)

z_speed = html.Div(
    id="control-panel-z_speed",
    children=[
        daq.Gauge(
            id="control-panel-z_speed-component",
            label="Z_Speed",
            min=0,
            max=50,
            showCurrentValue=True,
            value=10.000,
            size=175,
            units="1 m/s",
            color="#fec036",
        )
    ],
    n_clicks=0,
)

pressure = html.Div(
    id="control-panel-pressure",
    children=[
        daq.Tank(
            id="control-panel-pressure-component",
            label="Pressure",
            min=0,
            max=10,
            value=2,
            units="atm",
            showCurrentValue=True,
            color="#303030",
        )
    ],
    n_clicks=0,
)

#this is calculated from pressure data
altitude = html.Div(
    id="control-panel-altitude",
    children=[
        daq.Tank(
            id="control-panel-altitude-component",
            label="Altitude",
            min=0,
            max=1500,
            value=500,
            units="meters",
            showCurrentValue=True,
            color="#303030",
        )
    ],
    n_clicks=0,
)

temperature = html.Div(
    id="control-panel-temperature",
    children=[
        daq.Tank(
            id="control-panel-temperature-component",
            label="Temperature",
            min=0,
            max=500,
            value=300,
            units="Kelvin",
            showCurrentValue=True,
            color="#303030",
        )
    ],
    n_clicks=0,
)

humidity = html.Div(
    id="control-panel-humidity",
    children=[
        daq.Tank(
            id="control-panel-humidity-component",
            label="Humidity",
            min=0,
            max=100,
            value=55,
            units="Percentage",
            showCurrentValue=True,
            color="#303030",
        )
    ],
    n_clicks=0,
)

battery_indicator = html.Div(
    id="control-panel-battery",
    children=[
        daq.GraduatedBar(
            id="control-panel-battery-component",
            label="Battery-Level",
            min=0,
            max=100,
            value=60,
            step=1,
            showCurrentValue=True,
            color="#fec036",
        )
    ],
    n_clicks=0,
)

x_gps = html.Div(
    id="control-panel-x_gps",
    children=[
        daq.LEDDisplay(
            id="control-panel-x_gps-component",
            value="0000.0000",
            label="X_gps",
            size=24,
            color="#fec036",
            style={"color": "#black"},
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

y_gps = html.Div(
    id="control-panel-y_gps",
    children=[
        daq.LEDDisplay(
            id="control-panel-y_gps-component",
            value="0050.9789",
            label="Y_gps",
            size=24,
            color="#fec036",
            style={"color": "#black"},
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

#Side bar
cansat_full_logo = html.Tr(children= html.Tr([html.Td(cansat_logo), html.Td(cansat_text)]))

team_info = html.P(children= [
    html.H2("Our Team"),
    html.Tr("Kunj Shah"),
    html.Tr("Mohit Jani"),
    html.Tr("Tirth Jain"),
    html.Tr("Kangana Jethwani"),
    html.Tr("Pooja Rao"),
    html.Tr("Write here about NIT Surat", style = {"color": "grey"})
])

mission_info = html.P(children= [
    html.H2("Our CANSAT"),
    html.Tr("We have built one-of-a-kind cansat that can self stabilize itself")
])

root_layout = html.Div([
    html.Tr(cansat_full_logo), 
    html.Tr(team_info), 
    html.Tr(mission_info),
    daq.PowerButton(id = "power-button", on = "False"),
    html.Div(id='power-button-result')
])

app.layout = root_layout

#Defining every callbacks
#this is for clicking PowerButton
@callback(
    Output('power-button-result', 'children'),
    Input('power-button', 'on')
)


#Callback Functions
#this fn will return a string for the state of PowerButton
def update_output(on):
    return f'The button is {on}.'

#this fn will execute the cansat_data.csv file if PoweerButton is clicked
def execute_script(on):
    if on == "True":
        result = subprocess.run(['python', 'csv_data/random_data_generator.py'], capture_output=True, text=True)
        return f'Script Output: {result.stdout}'
    else:
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
