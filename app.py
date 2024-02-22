# IMPORTS
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_daq as daq
import subprocess
import plotly.graph_objects as go
import datetime
import os
import glob


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

cansat_logo = html.Div(html.Img(src="assets/navdhara_logo.png", height=70, width=70))
cansat_text = html.Div(html.Img(src="assets/navdhara_text.png", height=70, width=205))


# LAYOUT
# Section: main_time_battery
station_utc = html.Div(
    id="main-control-panel-station-utc",
    children=[
        daq.LEDDisplay(
            id="main-control-panel-station-utc-component",
            value="12:00",
            label="System Time",
            size=40,
            color="#e3b859",
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

cansat_utc = html.Div(
    id="main-control-panel-cansat-utc",
    children=[
        daq.LEDDisplay(
            id="main-control-panel-cansat-utc-component",
            value="12:00:00",
            label="CANSAT Time",
            size=40,
            color="#e3b859",
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

battery_percentage = html.Div(
    id="main-control-panel-battery-percentage",
    children=[
        daq.GraduatedBar(
            id="main-control-panel-battery-component",
            label="battery-precentage",
            min=0,
            max=100,
            value=60,
            step=1,
            showCurrentValue=True,
            color="#e3b859",
        )
    ],
    n_clicks=0,
)

battery_current = html.Div(
    id="main-control-panel-battery-current",
    children=[
        daq.LEDDisplay(
            id="main-control-panel-battery-current-component",
            value="2.0",
            label="Current (in A)",
            size=20,
            color="#e3b859",
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

battery_voltage = html.Div(
    id="main-control-panel-battery-voltage",
    children=[
        daq.LEDDisplay(
            id="main-control-panel-battery-voltage-component",
            value="12.0",
            label="Voltage (in V)",
            size=20,
            color="#e3b859",
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

# Section: main_control_panel
x_vel = html.Div(  # this from gps
    id="main-control-panel-x-vel",
    children=[
        daq.Gauge(
            id="main-control-panel-x-vel-component",
            label="x-Velocity",
            min=0,
            max=50,
            showCurrentValue=True,
            value=10.000,
            size=175,
            units="1 m/s",
            color="#e3b859",
        )
    ],
    n_clicks=0,
)

y_vel = html.Div(
    id="main-control-panel-y-vel",
    children=[
        daq.Gauge(
            id="main-control-panel-y-vel-component",
            label="y-Velocity",
            min=0,
            max=50,
            showCurrentValue=True,
            value=10.000,
            size=175,
            units="1 m/s",
            color="#e3b859",
        )
    ],
    n_clicks=0,
)

z_vel = html.Div(  # this from gps not differentiating from altitude_from_pressure
    id="main-control-panel-z-vel",
    children=[
        daq.Gauge(
            id="main-control-panel-z-vel-component",
            label="z-Velocity",
            min=0,
            max=50,
            showCurrentValue=True,
            value=10000,
            size=175,
            units="1 m/s",
            color="#e3b859",
        )
    ],
    n_clicks=0,
)

pressure = html.Div(
    id="main-control-panel-pressure",
    children=[
        daq.Tank(
            id="main-control-panel-pressure-component",
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

altitude_from_pressure = html.Div(  # this is calculated from pressure data
    id="main-control-panel-altitude-from-pressure",
    children=[
        daq.Tank(
            id="main-control-panel-altitude-from-pressure-component",
            label="Altitude-from-pressure",
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

altitude_gps = html.Div(
    id="main-control-panel-altitude-gps",
    children=[
        daq.Tank(
            id="main-control-panel-altitude-gps-component",
            label="Altitude-GPS",
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
    id="main-control-panel-temperature",
    children=[
        daq.Tank(
            id="main-control-panel-temperature-component",
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
    id="main-control-panel-humidity",
    children=[
        daq.Tank(
            id="main-control-panel-humidity-component",
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

# Section: extra_data
x_gps = html.Div(  # these are absolute distance values from the module, TODO: set a reference point and then plot the scatter plot
    id="main-control-panel-x_gps",
    children=[
        daq.LEDDisplay(
            id="main-control-panel-x-gps-component",
            value="0000.0000",
            label="x-GPS",
            size=24,
            color="#e3b859",
            style={"color": "#black"},
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

y_gps = html.Div(
    id="main-control-panel-y_gps",
    children=[
        daq.LEDDisplay(
            id="main-control-panel-y-gps-component",
            value="0050.9789",
            label="y-GPS",
            size=24,
            color="#e3b859",
            style={"color": "#black"},
            backgroundColor="#2b2b2b",
        )
    ],
    n_clicks=0,
)

# Section: side_systems_check
bno = daq.Indicator(
    className="avionics",
    id="bno",
    label="BNO-055",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

magnetometer = daq.Indicator(
    className="avionics",
    id="magnetometer",
    label="Magnetometer",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

bmp = daq.Indicator(
    className="avionics",
    id="bmp",
    label="BMP-280",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

aht = daq.Indicator(
    className="avionics",
    id="aht",
    label="AHT10",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

buzzer = daq.Indicator(
    className="avionics",
    id="buzzer",
    label="Buzzer",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

motor_driver = daq.Indicator(
    className="avionics",
    id="motor-driver",
    label="Motor driver L293d",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

gps_module = daq.Indicator(
    className="avionics",
    id="gps-module",
    label="GPS MODULE",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

stm32f4 = daq.Indicator(
    className="avionics",
    id="stm32f4",
    label="STM32F",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

esp32 = daq.Indicator(
    className="avionics",
    id="esp32",
    label="ESP-32",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

camera = daq.Indicator(
    className="avionics",
    id="camera",
    label="Camera",
    labelPosition="bottom",
    value=True,
    color="#e3b859",
    style={"color": "#black"},
)

# Stopwatch
stopwatch = html.Div(
    id="stopwatch",
    children=[
        html.H1(id="stopwatch-display", children="00:00:00"),
        html.Button(id="stopwatch-button-start", children="Start", n_clicks=0),
        html.Button(id="stopwatch-button-stop", children="Stop", n_clicks=0),
        html.Button(id="stopwatch-button-reset", children="Reset", n_clicks=0),
        dcc.Interval(
            id="stopwatch-interval",
            interval=1000,  # in milliseconds
            n_intervals=0,
            max_intervals=-1,  # run indefinitely
        ),
    ],
)

# Section: Toggles_and_switches
altitude_toggle = daq.ToggleSwitch(
    id="main-control-panel-toggle-altitude",
    value=True,
    label=["GPS", "From Pressure"],
    color="#ffe102",
    style={"color": "#black"},
)

utc_toggle = daq.ToggleSwitch(
    id="main-time-battery-toggle-UTC",
    value=True,
    label=["System", "CANSAT"],
    color="#ffe102",
    style={"color": "#black"},
)

rf_link_switch = daq.BooleanSwitch(
    id="side-systems-check-rf-link-switch",
    className="switch",
    on="False",
    label="RF Link",
    labelPosition="top",
    color="#e3b859",
)

flight_mode_dropdown = dcc.Dropdown(
    id="side-systems-check-flight-mode-dropdown-component",
    className="flightmode",
    options=[
        {"label": "IDLE", "value": "idle"},
        {"label": "FLIGHT", "value": "FLIGHT"},
        {"label": "RECOVERY", "value": "recovery"},
    ],
    clearable=False,
    value="IDLE",
)

# Section: side_team_info
cansat_full_logo = html.Tr(
    id="side-logo-cansat",
    className="CANSAT-logo",
    children=html.Tr([html.Td(cansat_logo), html.Td(cansat_text)]),
)

team_info = html.Div(
    id="side-team-info",
    className="team-info",
    children=[
        html.H4("Made with ❤️ at NIT Surat ", className="team-header"),
        # html.Div(
        #     className="team-content",
        #     children=[
        #         html.H5("Team Navdhara", className="team-name"),
        #         html.Ul(
        #             className="team-members",
        #             children=[
        #                 html.Li("Kunj Shah", className="team-member"),
        #                 html.Li("Mohit Jani", className="team-member"),
        #                 html.Li("Tirth Jain", className="team-member"),
        #                 html.Li("Kangana Jethwani", className="team-member"),
        #                 html.Li("Pooja Rao", className="team-member"),
        #             ]
        #         ),
        #     ],
        # ),
    ],
)

mission_check_list = html.Div(
    id="side-mission-check-list",
    className="mission-check-list",
    children=[
        html.H4("Mission Timeline & Activities", className="mission-header"),
        html.Div(
            className="mission-content",
            children=[
                html.Ul(
                    className="mission-items",
                    children=[
                        html.Details(
                            className="mission-item",
                            children=[
                                html.Summary(
                                    "Ground System Radio Link Check",
                                    className="mission-summary",
                                ),
                                html.P(
                                    "Details about Ground System Radio Link Check...",
                                    className="mission-details",
                                ),
                            ],
                        ),
                        html.Details(
                            className="mission-item",
                            children=[
                                html.Summary(
                                    "Powering on/off CANSAT",
                                    className="mission-summary",
                                ),
                                html.P(
                                    "Details about Powering on/off CANSAT...",
                                    className="mission-details",
                                ),
                            ],
                        ),
                        html.Details(
                            className="mission-item",
                            children=[
                                html.Summary(
                                    "Launch Configuration Procedures",
                                    className="mission-summary",
                                ),
                                html.P(
                                    "Details about Launch Configuration Procedures...",
                                    className="mission-details",
                                ),
                            ],
                        ),
                        html.Details(
                            className="mission-item",
                            children=[
                                html.Summary(
                                    "Loading CANSAT in launch vehicle",
                                    className="mission-summary",
                                ),
                                html.P(
                                    "Details about Loading CANSAT in launch vehicle...",
                                    className="mission-details",
                                ),
                            ],
                        ),
                        html.Details(
                            className="mission-item",
                            children=[
                                html.Summary(
                                    "Telemetry capture, processing & analysis",
                                    className="mission-summary",
                                ),
                                html.P(
                                    "Details about Telemetry capture, processing & analysis...",
                                    className="mission-details",
                                ),
                            ],
                        ),
                        html.Details(
                            className="mission-item",
                            children=[
                                html.Summary("Recovery", className="mission-summary"),
                                html.P(
                                    "Details about Recovery...",
                                    className="mission-details",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Create a scatter plot
gps_plot = html.Div(
    dcc.Graph(
        id="gps-plot",
        figure={
            "data": [
                go.Scatter(
                    x=[],
                    y=[],
                    mode="markers",
                    marker=dict(
                        size=10,
                        color="rgba(255, 182, 193, .9)",
                        line=dict(width=2, color="rgba(152, 0, 0, .8)"),
                    ),
                )
            ],
            "layout": go.Layout(
                title="GPS Plot",
                xaxis=dict(title="X GPS"),
                yaxis=dict(title="Y GPS"),
                hovermode="closest",
                plot_bgcolor="#a9cad6",
                paper_bgcolor="#a9cad6",
            ),
        },
    ),
    style={"border": "solid #e3b859", "border-radius": "10px"},  # Add a border here
)

# Create a histogram
histogram = html.Div(
    dcc.Graph(
        id="histogram",
        figure={
            "data": [
                go.Histogram(
                    x=[],
                    marker=dict(
                        color="rgba(100, 149, 237, .8)",
                        line=dict(width=1, color="rgba(0, 0, 0, 1)"),
                    ),
                )
            ],
            "layout": go.Layout(
                title="Histogram",
                xaxis=dict(title="Time (in seconds)"),
                yaxis=dict(title="Value"),
                hovermode="closest",
                plot_bgcolor="#a9cad6",
                paper_bgcolor="#a9cad6",
            ),
        },
    ),
    style={"border": "solid #e3b859", "border-radius": "10px"},  # Add a border here
)
# Side layout

side_panel_layout = html.Div(
    id="panel-side",
    children=[
        cansat_full_logo,
        rf_link_switch,
        flight_mode_dropdown,
        mission_check_list,
        html.Div(
            id="side-systems-check",
            children=[
                bno,
                magnetometer,
                bmp,
                aht,
                buzzer,
                motor_driver,
                gps_module,
                stm32f4,
                esp32,
                camera,
            ],
        ),
        team_info,
    ],
)
# Main panel layout
main_panel_layout = html.Div(
    id="panel-main",
    children=[
        dcc.Interval(
            id="interval-component", interval=1 * 1000, n_intervals=0  # in milliseconds
        ),
        gps_plot,
        html.Div(children=[station_utc, cansat_utc, utc_toggle]),
        battery_percentage,
        html.Div(children=[battery_current, battery_voltage]),
        html.Div(children=[x_vel, y_vel, z_vel]),
        html.Div(children=[humidity, temperature]),
        pressure,
        html.Div(children=[altitude_gps, altitude_from_pressure, altitude_toggle]),
        histogram,
        html.Pre(
            id="live-update-text",
            style={
                "backgroundColor": "#000",
                "color": "#fff",
                "fontFamily": "Consolas",
                "textAlign": "center",
                "padding": "10px",
                "borderRadius": "5px",
                "margin": "auto",
                "width": "50%",
                "height": "50%",
                "overflow": "auto",
            },
        ),
        html.Pre(
            id="python-script-run",
            style={
                "backgroundColor": "#000",
                "color": "#fff",
                "fontFamily": "Consolas",
                "textAlign": "center",
                "padding": "10px",
                "borderRadius": "5px",
                "margin": "auto",
                "width": "50%",
                "height": "50%",
                "overflow": "auto",
            },
        ),
    ],
)
# whole layout
root_layout = html.Div(children=[side_panel_layout, main_panel_layout])

app.layout = root_layout


@app.callback(
    Output("live-update-text", "children"), Input("interval-component", "n_intervals")
)
def update_metrics(n):
    # Get the latest CSV file
    list_of_files = glob.glob(
        "data/each_second/xbee_data_*.csv"
    )  # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)

    # Read the second row of the CSV file
    df = pd.read_csv(latest_file, skiprows=1, nrows=1)

    # Convert the row to a string and return it
    return df.to_string(index=False)

@app.callback(
    Output("python-script-run", "children"), Input("side-systems-check-rf-link-switch", "on")
)
def run_script(on):
    if not on:
        # Run the script and get its output
        subprocess.run(["python", r"C:\Users\kunjs\Desktop\Cansat\SEM 7\DEV\GUI\CANSAT_data_viz\with_dash\data\simul_xbee_data_stream.py"])
        return "Script has been run."
    else:
        return "Script has not been run."


@app.callback(
    Output("main-control-panel-station-utc-component", "value"),
    Input("interval-component", "n_intervals"),
)
def update_time(n):
    return datetime.datetime.now().strftime("%H:%M:%S")


# # stopwatch
# @callback(
#     Output("stopwatch-interval", "n_intervals"),
#     Input("stopwatch-button-start", "n_clicks"),
#     Input("stopwatch-button-reset", "n_clicks"),
#     State("stopwatch-interval", "n_intervals"),
# )
# def start_stopwatch(start_clicks, reset_clicks, n_intervals):
#     if start_clicks > 0:
#         return n_intervals + 1
#     elif reset_clicks > 0:
#         return 0
#     else:
#         return n_intervals


# @callback(
#     Output("stopwatch-display", "children"), Input("stopwatch-interval", "n_intervals")
# )
# def update_stopwatch(n_intervals):
#     minutes, seconds = divmod(n_intervals, 60)
#     hours, minutes = divmod(minutes, 60)
#     return f"{hours:02}:{minutes:02}:{seconds:02}"


# Callback Functions
# this fn will return a string for the state of PowerButton


# RUNNING
if __name__ == "__main__":
    app.run_server(debug=True)
