from utils.constants import MAX_NOTA, MIN_NOTA, NUMBER_OF_STEPS
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from dash import html, dcc


def criar_escala_cores(min_nota, max_nota, cor_escala="Blues"):
    num_cores = NUMBER_OF_STEPS
    cores = px.colors.sample_colorscale(cor_escala, [n/(num_cores - 1) for n in range(num_cores)])

    valores = np.linspace(min_nota, max_nota, num_cores)
    valores_texto = [f"{v:.0f}" for v in valores]

    # Cores do texto: branco se cor for escura
    text_colors = ['#000000' if i < 4 else '#EEEEEE' for i in range(num_cores)]

    fig = go.Figure(
        data=[
            go.Bar(
                y=valores_texto,       # ordem natural: menor embaixo
                x=[1] * num_cores,
                marker_color=cores,    # mesma ordem das cores
                orientation='h',
                text=valores_texto,
                textfont=dict(color=text_colors, size=12),
                hoverinfo='skip',
                textposition="auto",  # Deixa o plotly centralizar
                insidetextanchor="middle",  # Centraliza verticalmente
            )
        ]
    )

    fig.update_layout(
        showlegend=False,
        xaxis_visible=False,
        yaxis=dict(
            tickmode='array',
            showticklabels=False
        ),
        bargap=0,  # remove espaço entre as barras
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=80,
        height=300
    )

    return fig



def Scale():
    return html.Div(
        id="scale-card",
        children=[
            html.H4(
                "Escala de Notas",
                style={
                    "text-align": "center",
                    "margin-bottom": "0px",
                    "font-size": "10px",
                },
            ),
            dcc.Graph(
                id="scale-graph",
                figure=criar_escala_cores(MIN_NOTA, MAX_NOTA),
                config={"staticPlot": True, "displayModeBar": False},
                style={"pointer-events": "none"},
            ),
        ],
        style={
            "width": "auto",
            "padding": "10px",
            "background-color": "rgba(255, 255, 255, 0.7)",
            "border-radius": "8px",
            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
        },
    )
