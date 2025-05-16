import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from dash import html, dcc

def criar_escala_cores(min_nota, max_nota):
    num_cores = 8
    cores = px.colors.sample_colorscale("Blues", [n/(num_cores - 1) for n in range(num_cores)])

    valores = np.linspace(min_nota, max_nota, num_cores)
    valores_texto = [f"{v:.0f}" for v in valores]

    # Definir cor do texto: branco para todas, exceto a mais clara (primeira), que é preta
    text_colors = ['#000000'] * (num_cores)

    fig = go.Figure(
        data=[
            go.Bar(
                x=[1] * num_cores,
                y=valores,
                marker_color=cores,
                orientation='v',
                text=valores_texto,
                textposition="inside",
                textfont=dict(color=text_colors, size=10),
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
        height=260
    )

    return fig

def Scale(min_nota, max_nota):
    return html.Div(
        id='scale-card',
        children=[
            html.H4("Escala de Notas",
                   style={'text-align': 'center',
                         'margin-bottom': '8px',
                         'font-size': '12px'}),
            dcc.Graph(
                id='scale-graph',
                figure=criar_escala_cores(min_nota, max_nota),
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