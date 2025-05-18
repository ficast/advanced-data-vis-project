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

    # Calculate white para os 2 primeiros e preto para os 6 últimos
    text_colors = [
        '#EEEEEE' if i > 3 else '#000000' for i in range(num_cores)
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=[1] * num_cores,
                y=valores,
                marker_color=cores,
                orientation='v',
                text=valores_texto,
                textposition="inside",
                textfont=dict(color=text_colors, size=12),
                hoverinfo='skip'
            )
        ]
    )

    fig.update_layout(
        showlegend=False,
        xaxis_visible=False,
        yaxis_visible=False,
        margin=dict(l=0, r=0, t=0, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=80,
        height=300
    )

    return fig

def Scale():
    return html.Div(
        id='scale-card',
        children=[
            html.H4("Escala de Notas",
                   style={'text-align': 'center',
                         'margin-bottom': '0px',
                         'font-size': '12px'}),
            dcc.Graph(
                id='scale-graph',
                figure=criar_escala_cores(MIN_NOTA, MAX_NOTA),
                config={
                    'staticPlot': True,
                    'displayModeBar': False
                },
                style={'pointer-events': 'none'}
            )
        ],
        style={
            'width': 'auto',
            'padding': '10px',
            'background-color': 'rgba(255, 255, 255, 0.7)',
            'border-radius': '8px',
            'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'
        }
    )