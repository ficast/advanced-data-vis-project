import plotly.graph_objects as go
import numpy as np
from queries.renda_familiar_query import load_renda_familiar_data
from utils.constants import COLOR_BRASIL, COLOR_ESTADO, COLOR_MUNICIPIO, FAIXAS_RENDA

def criar_grafico_renda_familiar(ano, estado, municipio):
    categorias = list(FAIXAS_RENDA.values())

    # Brasil
    df_brasil = load_renda_familiar_data(ano, "Brasil")
    dados_brasil = {}
    for faixa in categorias:
        row = df_brasil[df_brasil['faixa_renda_label'] == faixa]
        if not row.empty:
            row = row.iloc[0]
            dados_brasil[faixa] = row['nota_media']
        else:
            dados_brasil[faixa] = np.nan

    # Estado
    dados_estado = {}
    if estado and estado != "Brasil":
        df_estado = load_renda_familiar_data(ano, estado)
        for faixa in categorias:
            row = df_estado[df_estado['faixa_renda_label'] == faixa]
            if not row.empty:
                row = row.iloc[0]
                dados_estado[faixa] = row['nota_media']
            else:
                dados_estado[faixa] = np.nan

    # Município
    dados_municipio = {}
    if municipio:
        df_municipio = load_renda_familiar_data(ano, municipio)
        for faixa in categorias:
            row = df_municipio[df_municipio['faixa_renda_label'] == faixa]
            if not row.empty:
                row = row.iloc[0]
                dados_municipio[faixa] = row['nota_media']
            else:
                dados_municipio[faixa] = np.nan

    fig = go.Figure()

    # Brasil
    fig.add_trace(go.Bar(
        x=categorias,
        y=[dados_brasil[faixa] for faixa in categorias],
        name="Brasil",
        marker_color=COLOR_BRASIL
    ))

    # Estado
    if dados_estado:
        fig.add_trace(go.Bar(
            x=categorias,
            y=[dados_estado[faixa] for faixa in categorias],
            name=estado,
            marker_color=COLOR_ESTADO
        ))

    # Município
    if dados_municipio:
        fig.add_trace(go.Bar(
            x=categorias,
            y=[dados_municipio[faixa] for faixa in categorias],
            name=municipio,
            marker_color=COLOR_MUNICIPIO
        ))

    fig.update_layout(
        barmode='group',
        xaxis_title="Faixa de Renda Familiar",
        yaxis_title="Nota Média",
        yaxis=dict(range=[0, 1000]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=True,
        width=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig