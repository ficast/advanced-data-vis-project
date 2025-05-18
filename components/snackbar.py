from dash import html
from utils.constants import COLOR_BLUE_BRASIL
snackbar = html.Div(
    "Clique em um estado no mapa ou um ano na timeline para filtrar os dados.",
    id="mapa-instrucao",
    style={
        "background": COLOR_BLUE_BRASIL,
        "opacity": 0.75,
        "border": "1px solid #bbb",
        "borderRadius": "8px",
        "padding": "12px 18px",
        "position": "absolute",
        "top": "30px",
        "right": "30px",
        "zIndex": 10,
        "boxShadow": "0 2px 8px rgba(0,0,0,0.08)",
        "fontSize": "1.1em",
        "color": "white",
        "maxWidth": "400px",
    },
)
