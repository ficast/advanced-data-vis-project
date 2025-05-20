import plotly.graph_objects as go

from queries.cor_raca_query import load_raca_data
import numpy as np
from utils.constants import COLOR_BRASIL, COLOR_ESTADO, COLOR_MUNICIPIO
from queries.cor_raca_query import MAPPING_COR_RACA_LABEL, load_raca_data

def criar_grafico_cor_raca(ano, estado, municipio):
    categorias = list(MAPPING_COR_RACA_LABEL.values())

    # Brasil
    df_brasil = load_raca_data(ano, "Brasil")
    dados_brasil = {}
    for raca in categorias:
        row = df_brasil[df_brasil['raca_label'] == raca]
        if not row.empty:
            row = row.iloc[0]
            dados_brasil[raca] = row['nota_media']
        else:
            dados_brasil[raca] = np.nan

    # Estado
    dados_estado = {}
    if estado and estado != "Brasil":
        df_estado = load_raca_data(ano, estado)
        for raca in categorias:
            row = df_estado[df_estado['raca_label'] == raca]
            if not row.empty:
                row = row.iloc[0]
                dados_estado[raca] = row['nota_media']
            else:
                dados_estado[raca] = np.nan

    # Município
    dados_municipio = {}
    if municipio:
        df_municipio = load_raca_data(ano, municipio)
        for raca in categorias:
            row = df_municipio[df_municipio['raca_label'] == raca]
            if not row.empty:
                row = row.iloc[0]
                dados_municipio[raca] = row['nota_media']
            else:
                dados_municipio[raca] = np.nan

    fig = go.Figure()

    # Brasil
    fig.add_trace(go.Bar(
        x=categorias,
        y=[dados_brasil[raca] for raca in categorias],
        name="Brasil",
        marker_color=COLOR_BRASIL
    ))

    # Estado
    if dados_estado:
        fig.add_trace(go.Bar(
            x=categorias,
            y=[dados_estado[raca] for raca in categorias],
            name=estado,
            marker_color=COLOR_ESTADO
        ))

    # Município
    if dados_municipio:
        fig.add_trace(go.Bar(
            x=categorias,
            y=[dados_municipio[raca] for raca in categorias],
            name=municipio,
            marker_color=COLOR_MUNICIPIO
        ))

    fig.update_layout(
        barmode='group',
        xaxis_title="Cor/Raça",
        yaxis_title="Nota Média",
        yaxis=dict(range=[0, 1000]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig