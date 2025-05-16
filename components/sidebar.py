from dash import html, dcc
import dash_bootstrap_components as dbc

sidebar = dbc.Container(
        className="sidebar-container",
        children=[
            html.H1(
            "Dados Enem 2014-2023", style={"color": "#000000", "textAlign": "center", "marginBottom": "16px"}
        ),
        html.Div([
            html.H3("Filtrando por:", style={"color": "#000000"}),
            html.P(id="nome-estado"),
        ], style={"marginBottom": "10px"}),
        html.Hr(),
        html.H3("Ano selecionado:", style={"color": "#000000"}),
        html.Div(
            style={"display": "flex", "alignItems": "center", "gap": "10px"},
            children=[
                html.P(id="ano-selecionado", style={"margin": "0px"}),
                html.Button("X", id="limpar-ano", n_clicks=0),
            ],
        ),
        html.Hr(),
    ],
    fluid=True,
)
