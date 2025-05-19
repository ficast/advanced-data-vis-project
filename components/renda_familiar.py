import pandas as pd
import plotly.graph_objects as go
from utils.constants import FAIXAS_RENDA, COLOR_RED_ESTADO, COLOR_GREEN_MUNICIPIO, CORES_PASTEL
from queries.renda_familiar_query import load_renda_familiar_data
import plotly.express as px

def criar_grafico_renda_familiar(ano=None, estado=None, municipio=None):
    # Carrega dados do Brasil SEMPRE
    df_brasil = load_renda_familiar_data(ano, 'Brasil')
    df_estado = None
    df_municipio = None
    
    if df_brasil is None or df_brasil.empty:
        return px.bar(title="Sem dados do Brasil disponíveis")
    
    if estado != 'Brasil':
        df_estado = load_renda_familiar_data(ano, estado)
    
    if municipio != '':
        df_municipio = load_renda_familiar_data(ano, estado, municipio)
    
    # Ordena as faixas
    df_brasil['faixa_renda_label'] = pd.Categorical(
        df_brasil['faixa_renda_label'],
        categories=list(FAIXAS_RENDA.values()),
        ordered=True
    )

    fig = px.bar(
        df_brasil,
        x='faixa_renda_label',
        y='nota_media',
        color='faixa_renda_label',
        color_discrete_sequence=CORES_PASTEL,
        labels={
            'faixa_renda_label': 'Faixa de Renda Familiar',
            'nota_media': 'Nota Média'
        },
    )

    fig.update_layout(
        xaxis={
            'categoryorder': 'array',
            'categoryarray': list(FAIXAS_RENDA.values()),
            'showgrid': False,
            'zeroline': False,
            'showline': False,
            'ticks': ''
        },
        yaxis={
            'range': [0, 1000],
            'showgrid': False,
            'zeroline': False,
            'showline': False,
            'ticks': ''
        },
        yaxis_title="Nota Média",
        legend_title="Faixa de Renda",
        plot_bgcolor='white',
        paper_bgcolor='white',
        hoverlabel=dict(bgcolor="white"),
        hovermode='x unified',
        margin=dict(l=20, r=20, t=40, b=40),
        showlegend=False
    )
    
    # Hover detalhado
    for i, trace in enumerate(fig.data):
        row = df_brasil.iloc[i]
        trace.customdata = [[row['q1'], row['mediana'], row['q3'], row['quantidade_alunos'], row['local']]]
        trace.hovertemplate = "<br>".join([
            "<b>%{customdata[4]}</b>",
            "Nota Média: %{y:.1f}",
            "Q1: %{customdata[0]:.1f}",
            "Mediana: %{customdata[1]:.1f}",
            "Q3: %{customdata[2]:.1f}",
            "Qtd. de Alunos: %{customdata[3]:.0f}",
        ])
    
    if df_estado is not None and not df_estado.empty:
        # Ordena as faixas
        df_estado['faixa_renda_label'] = pd.Categorical(
            df_estado['faixa_renda_label'],
            categories=list(FAIXAS_RENDA.values()),
            ordered=True
        )
        
        if estado:
            fig.add_trace(go.Scatter(
                x=df_estado['faixa_renda_label'],
                y=df_estado['nota_media'],
                mode='markers',
                name=estado,
                marker=dict(size=10, color=COLOR_RED_ESTADO, symbol='square'),
                hovertemplate="<b>%{x}: %{customdata[4]}</b><br>Nota Média: %{y:.1f}<br>Q1: %{customdata[0]:.1f}<br>Mediana: %{customdata[1]:.1f}<br>Q3: %{customdata[2]:.1f}<br>Qtd. de Alunos: %{customdata[3]:.0f}<extra></extra>",
                customdata=df_estado[['q1', 'mediana', 'q3', 'quantidade_alunos', 'local']]
            ))

    if df_municipio is not None and not df_municipio.empty:
        # Ordena as faixas
        df_municipio['faixa_renda_label'] = pd.Categorical(
            df_municipio['faixa_renda_label'],
            categories=list(FAIXAS_RENDA.values()),
            ordered=True
        )

        if municipio:
            fig.add_trace(go.Scatter(
                x=df_municipio['faixa_renda_label'],
                y=df_municipio['nota_media'],
                mode='markers',
                name=municipio,
                marker=dict(size=10, color=COLOR_GREEN_MUNICIPIO, symbol='star'),
                hovertemplate="<b>%{x}: %{customdata[4]}</b><br>Nota Média: %{y:.1f}<br>Q1: %{customdata[0]:.1f}<br>Mediana: %{customdata[1]:.1f}<br>Q3: %{customdata[2]:.1f}<br>Qtd. de Alunos: %{customdata[3]:.0f}<extra></extra>",
                customdata=df_municipio[['q1', 'mediana', 'q3', 'quantidade_alunos', 'local']]
            ))
    
    return fig