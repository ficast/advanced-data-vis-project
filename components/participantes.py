import plotly.graph_objects as go
from utils.constants import COLOR_BRASIL, COLOR_ESTADO, COLOR_MUNICIPIO

def create_participantes_figure(df, estado=None, municipio=None):
    """
    Cria gráfico de linha mostrando participantes por ano
    """
    fig = go.Figure()

    # Dados do Brasil (sempre mostrado)
    df_brasil = df[df['nivel'] == 'Brasil']
    fig.add_trace(go.Scatter(
        x=df_brasil['nu_ano'],
        y=df_brasil['participantes'],
        mode='lines+markers',
        name='Brasil',
        line=dict(color=COLOR_BRASIL, width=3),
        hovertemplate='<b>Brasil</b><br>' +
                     'Ano: %{x}<br>' +
                     'Participantes: %{y:,.0f}<br>' +
                     '<extra></extra>'
    ))

    # Estado (case-insensitive)
    if estado and estado != "Brasil":
        df_estado = df[(df['nivel'] == 'Estado') & (df['nome'].str.lower() == estado.lower())]
        if not df_estado.empty:
            fig.add_trace(go.Scatter(
                x=df_estado['nu_ano'],
                y=df_estado['participantes'],
                mode='lines+markers',
                name=estado,
                line=dict(color=COLOR_ESTADO, width=3),
                hovertemplate=f'<b>{estado}</b><br>' +
                             'Ano: %{x}<br>' +
                             'Participantes: %{y:,.0f}<br>' +
                             '<extra></extra>'
            ))

    # Município (case-insensitive)
    if municipio:
        df_mun = df[(df['nivel'] == 'Municipio') & (df['nome'].str.lower() == municipio.lower())]
        if not df_mun.empty:
            fig.add_trace(go.Scatter(
                x=df_mun['nu_ano'],
                y=df_mun['participantes'],
                mode='lines+markers',
                name=municipio,
                line=dict(color=COLOR_MUNICIPIO, width=3),
                hovertemplate=f'<b>{municipio}</b><br>' +
                             'Ano: %{x}<br>' +
                             'Participantes: %{y:,.0f}<br>' +
                             '<extra></extra>'
            ))

    # Layout
    fig.update_layout(
        xaxis=dict(
            title="Ano",
            tickmode='linear',
            dtick=1,  # Mostra todos os anos
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title="Participantes",
            gridcolor='lightgray',
            rangemode='tozero'  # Começa do zero
        ),
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=40, b=40),
        width=500,

    )

    return fig