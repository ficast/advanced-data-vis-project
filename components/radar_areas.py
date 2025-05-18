from utils.constants import MAX_NOTA, MIN_NOTA, COLOR_BLUE_BRASIL, COLOR_RED_ESTADO, COLOR_GREEN_MUNICIPIO
import plotly.graph_objects as go

def radar_areas(df_areas, estado=None, municipio=None):
    # Áreas na ordem desejada
    areas = ['Linguagens', 'Humanas', 'Natureza', 'Matemática', 'Redação']
    colunas = ['avg_nota_lc', 'avg_nota_ch', 'avg_nota_cn', 'avg_nota_mt', 'avg_nota_redacao']

    fig = go.Figure()

    # Brasil
    brasil = df_areas[df_areas['nivel'] == 'Brasil']
    fig.add_trace(go.Scatterpolar(
        r=[brasil[c].values[0] for c in colunas],
        theta=areas,
        fill='toself',
        name='Brasil',
        line=dict(color=COLOR_BLUE_BRASIL, width=2)
    ))

    # Estado
    if estado and estado in df_areas['estado'].values:
        est = df_areas[(df_areas['nivel'] == 'Estado') & (df_areas['estado'] == estado)]
        if not est.empty:
            fig.add_trace(go.Scatterpolar(
                r=[est[c].values[0] for c in colunas],
                theta=areas,
                fill='toself',
                name=estado,
                line=dict(color=COLOR_RED_ESTADO, width=2)
            ))

    # Município
    if municipio and municipio in df_areas['municipio'].values:
        mun = df_areas[(df_areas['nivel'] == 'Municipio') & (df_areas['municipio'] == municipio)]
        if not mun.empty:
            fig.add_trace(go.Scatterpolar(
                r=[mun[c].values[0] for c in colunas],
                theta=areas,
                fill='toself',
                name=municipio,
                line=dict(color=COLOR_GREEN_MUNICIPIO, width=2)
            ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[MIN_NOTA, MAX_NOTA])
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=20, b=20),
        height=300,
        width=500
    )
    return fig