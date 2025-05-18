import os
from app import app
import dash_bootstrap_components as dbc

from components.map import map
from components.sidebar import sidebar

# Importação de callbacks
import callbacks.map_callbacks
import callbacks.timeline_callbacks
import callbacks.sidebar_callbacks
import callbacks.scale_callbacks

# Layout principal
app.layout = dbc.Container(
    className="app-container",
    fluid=True,
    children=[
        dbc.Row(
            [
                dbc.Col(
                    map,
                    className="map-container",
                    width=8,
                ),
                dbc.Col(
                    sidebar,
                    className="sidebar-container",
                    width=4,
                ),
            ],
        ),
    ],
)


if __name__ == "__main__":
    environment = os.getenv("ENVIRONMENT")
    if environment == "development":
        app.run_server(debug=True, host="0.0.0.0", port=8050)
    else:
        app.run_server(debug=False, host="0.0.0.0", port=8050)
