from dash import html
from utils.constants import COLOR_BRASIL

# snackbar = html.Div(
#     id="mapa-instrucao",
#     style={
#         "background": COLOR_BRASIL,
#         "opacity": 0.75,
#         "border": "1px solid #bbb",
#         "borderRadius": "8px",
#         "padding": "12px 18px",
#         "position": "absolute",
#         "top": "30px",
#         "right": "30px",
#         "zIndex": 10,
#         "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
#         "fontSize": "1.1em",
#         "color": "white",
#         "maxWidth": "400px",
#     },
#     children=[
#         html.P(
#             "Clique em um estado no mapa ou um ano na timeline para filtrar os dados.",
#         ),
#         html.P(
#             "Dê um duplo clique no mapa para resetar os filtros.",
#         ),
#     ],
# )

import dash_bootstrap_components as dbc

snackbar = dbc.Toast(
    [
        html.P("Clique em um estado e/ou município no mapa ou um ano na timeline para filtrar os dados.", style={"fontSize": "14px"}),
        html.P("Dê um duplo clique no mapa para resetar os filtros.", style={"fontSize": "14px"})
    ],
    id="mapa-instrucao",
    is_open=True,
    header="Instruções",
    header_style={"color": COLOR_BRASIL, "fontSize": "18px"},
    dismissable=True,
    duration=30000,
    icon="info",
    style={
        "position": "fixed",
        "top": "50%",
        "left": "50%",
        "transform": "translate(-50%, -50%)",
        "width": 450,
        "zIndex": 1000,
        "opacity": 1,
        "border": "1px solid #bbb",
        "borderRadius": "8px",
        "padding": "12px 18px",
    }
)