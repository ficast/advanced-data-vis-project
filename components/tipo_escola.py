from queries.tipo_escola_query import MAPPING_TP_ESCOLA_LABEL, load_tipo_escola_data
import numpy as np
import plotly.graph_objects as go
from utils.constants import COLOR_BRASIL, COLOR_ESTADO, COLOR_MUNICIPIO


def criar_grafico_tipo_escola(ano, estado, municipio):
    categorias = list(MAPPING_TP_ESCOLA_LABEL.values())

    # Brasil
    df_brasil = load_tipo_escola_data(ano, "Brasil")
    dados_brasil = {}
    for escola in categorias:
        row = df_brasil[df_brasil['tipo_escola_label'] == escola]
        if not row.empty:
            row = row.iloc[0]
            dados_brasil[escola] = row['nota_media']
        else:
            dados_brasil[escola] = np.nan

    # Estado
    dados_estado = {}
    if estado and estado != "Brasil":
        df_estado = load_tipo_escola_data(ano, estado)
        for escola in categorias:
            row = df_estado[df_estado['tipo_escola_label'] == escola]
            if not row.empty:
                row = row.iloc[0]
                dados_estado[escola] = row['nota_media']
            else:
                dados_estado[escola] = np.nan

    # Município
    dados_municipio = {}
    if municipio:
        df_municipio = load_tipo_escola_data(ano, municipio)
        for escola in categorias:
            row = df_municipio[df_municipio['tipo_escola_label'] == escola]
            if not row.empty:
                row = row.iloc[0]
                dados_municipio[escola] = row['nota_media']
            else:
                dados_municipio[escola] = np.nan

    fig = go.Figure()

    # Brasil
    fig.add_trace(go.Bar(
        x=categorias,
        y=[dados_brasil[escola] for escola in categorias],
        name="Brasil",
        marker_color=COLOR_BRASIL
    ))

    # Estado
    if dados_estado:
        fig.add_trace(go.Bar(
            x=categorias,
            y=[dados_estado[escola] for escola in categorias],
            name=estado,
            marker_color=COLOR_ESTADO
        ))

    # Município
    if dados_municipio:
        fig.add_trace(go.Bar(
            x=categorias,
            y=[dados_municipio[escola] for escola in categorias],
            name=municipio,
            marker_color=COLOR_MUNICIPIO
        ))

    fig.update_layout(
        barmode='group',
        xaxis_title="Tipo de Escola",
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