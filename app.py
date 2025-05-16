import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], external_scripts=[
    {
        "src": "scripts/cursor.js",
        "type": "text/javascript",
    }
])
server = app.server
