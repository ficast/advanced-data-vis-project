import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.LUX], title="Dashboard ENEM 2014-2023"
)


server = app.server
