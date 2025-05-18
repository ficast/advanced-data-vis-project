import plotly.graph_objects as go
from utils.constants import COLOR_BLUE_BRASIL, COLOR_RED_ESTADO, COLOR_GREEN_MUNICIPIO


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
        line=dict(color=COLOR_BLUE_BRASIL, width=3),
        hovertemplate='<b>Brasil</b><br>' +
                     'Ano: %{x}<br>' +
                     'Participantes: %{y:,.0f}<br>' +
                     '<extra></extra>'
    ))

    if estado and estado != "Brasil":
        df_estado = df[(df['nivel'] == 'Estado') & (df['nome'] == estado)]
        fig.add_trace(go.Scatter(
            x=df_estado['nu_ano'],
            y=df_estado['participantes'],
            mode='lines+markers',
            name=estado,
            line=dict(color=COLOR_RED_ESTADO, width=3),
            hovertemplate=f'<b>{estado}</b><br>' +
                         'Ano: %{x}<br>' +
                         'Participantes: %{y:,.0f}<br>' +
                         '<extra></extra>'
        ))
        
    # Dados do Município (se selecionado)
    if municipio:
        df_mun = df[(df['nivel'] == 'Municipio') & (df['nome'] == municipio)]
        fig.add_trace(go.Scatter(
            x=df_mun['nu_ano'],
            y=df_mun['participantes'],
            mode='lines+markers',
            name=municipio,
            line=dict(color=COLOR_GREEN_MUNICIPIO, width=3),
            hovertemplate=f'<b>{municipio}</b><br>' +
                         'Ano: %{x}<br>' +
                         'Participantes: %{y:,.0f}<br>' +
                         '<extra></extra>'
        ))

    # Layout
    fig.update_layout(
        title=dict(
            text="Número de Participantes por Ano",
            x=0.5,
            y=0.95
        ),
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
        margin=dict(l=60, r=30, t=50, b=50)
    )

    return fig