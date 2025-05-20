from dash import html, dcc
import dash_bootstrap_components as dbc

from utils.constants import LOADING_COLOR

styleHr = {"marginBottom": "12px", "marginTop": "12px"}

sidebar = dbc.Container(
    className="sidebar-content",
    children=[
        html.H1(
            "Dados Enem 2014-2023",
            style={"color": "#000000", "textAlign": "center", "marginBottom": "16px"},
        ),
        dcc.Loading(
            id="loading-sidebar",
            type="default",
            color=LOADING_COLOR,
            children=[html.Div(id="loading-content", style={"display": "relative", "margin-top": "24px"})],
        ),
        html.Hr(style={**styleHr, "border": "2px solid #000000"}),
        html.Div(
            [
                html.H3("Filtrando por:", style={"color": "#000000"}),
                html.P(["Estado: ", html.Span(id="nome-estado")]),
                html.P(["Município: ", html.Span(id="nome-municipio")]),
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "10px"},
                    children=[
                        html.P(
                            [
                                "Ano: ",
                                html.Span(id="ano-selecionado"),
                            ],
                            style={"margin": "0px"},
                        ),
                        html.Button("X", id="limpar-ano", n_clicks=0),
                    ],
                ),
            ],
            style={"marginBottom": "10px"},
        ),
        html.Hr(style=styleHr),
        html.H3("Número de Participantes por Ano", style={"color": "#000000"}),
        html.Div(
            [
                dcc.Graph(
                    id="participantes-graph",
                    config={
                        "displayModeBar": False,
                        "scrollZoom": False,
                        "doubleClick": "reset",
                        "editable": False,
                    },
                    style={"height": "400px"},
                )
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
            },
        ),
        html.Hr(style=styleHr),
        html.H3("Notas Médias por Disciplina", style={"color": "#000000"}),
        html.Div(
            [
                dcc.Graph(
                    id="radar-areas",
                    config={
                        "displayModeBar": False,
                        "scrollZoom": False,
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
            },
        ),
        html.Hr(style=styleHr),
        html.H3("Distribuição das notas por Disciplina", style={"color": "#000000"}),
        html.Div(
            [
                dcc.Graph(
                    id="box-plots",
                    config={
                        "displayModeBar": False,
                        "scrollZoom": False,
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
            },
        ),
        html.Hr(style=styleHr),
        html.H3("Notas Médias por Renda Familiar", style={"color": "#000000"}),
        html.Div(
            [
                dcc.Graph(
                    id="grafico-renda-familiar",
                    config={
                        "displayModeBar": False,
                        "scrollZoom": False,
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
            },
        ),
        html.Hr(style=styleHr),
        html.H3("Notas Médias por Tipo de Escola", style={"color": "#000000"}),
        html.Div(
            [
                dcc.Graph(
                    id="grafico-tipo-escola",
                    config={
                        "displayModeBar": False,
                        "scrollZoom": False,
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
            },
        ),
        html.Hr(style=styleHr),
        html.H3("Notas Médias por Cor/Raça", style={"color": "#000000"}),
        html.Div(
            [
                dcc.Graph(
                    id="grafico-cor-raca",
                    config={
                        "displayModeBar": False,
                        "scrollZoom": False,
                    },
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
            },
        ),
    ],
    fluid=True,
)
