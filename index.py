from app import app  # importa o app criado em app.py
from components.timeline import timeline
from components.map import map
from components.sidebar import sidebar
import dash_bootstrap_components as dbc

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
                    width=8,
                    style={
                        "height": "100vh",
                        "padding": 0,
                        "margin": 0,
                    },
                ),
                dbc.Col(
                    sidebar,
                    width=4,
                    style={
                        "height": "100vh",
                        'overflowY': 'scroll',
                        "padding": 0,
                        "margin": 0,
                        "box-shadow": "0px 2px 2px rgba(0,0,0,0.12)"
                    },
                ),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
