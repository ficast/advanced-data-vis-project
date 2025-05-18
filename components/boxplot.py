import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.constants import COLOR_BLUE_BRASIL, COLOR_RED_ESTADO, COLOR_GREEN_MUNICIPIO
def create_box_plots(df, nome_estado, nome_municipio):
    disciplinas = ['Linguagens', 'Humanas', 'Natureza', 'Matemática', 'Redação']
    niveis = ['Brasil', 'Estado', 'Municipio']
    cores = {'Brasil': COLOR_BLUE_BRASIL, 'Estado': COLOR_RED_ESTADO, 'Municipio': COLOR_GREEN_MUNICIPIO}
    cor_fake = 'rgba(0,0,0,0)'

    legenda_niveis = {
        'Brasil': 'Brasil',
        'Estado': nome_estado if nome_estado and nome_estado != 'Brasil' else '',
        'Municipio': nome_municipio if nome_municipio else ''
    }

    fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=False,
        vertical_spacing=0.08,
        subplot_titles=disciplinas
    )

    for i, disciplina in enumerate(disciplinas, start=1):
        presentes = []
        for nivel in niveis:
            df_plot = df[(df['disciplina'] == disciplina) & (df['nivel'] == nivel)]
            if not df_plot.empty:
                presentes.append(nivel)
                fig.add_trace(
                    go.Box(
                        q1=[df_plot['q1'].iloc[0]],
                        median=[df_plot['mediana'].iloc[0]],
                        q3=[df_plot['q3'].iloc[0]],
                        lowerfence=[df_plot['min'].iloc[0]],
                        upperfence=[df_plot['max'].iloc[0]],
                        mean=[df_plot['media'].iloc[0]],
                        name=legenda_niveis[nivel] if legenda_niveis[nivel] else nivel,
                        marker_color=cores[nivel],
                        boxpoints=False,
                        legendgroup=nivel,
                        showlegend=(i == 1),
                        line=dict(width=2),
                        fillcolor=cores[nivel],
                        opacity=0.8,
                        width=0.3,
                        offsetgroup=nivel,
                        x=[nivel],
                    ),
                    row=i, col=1
                )
            else:
                # Adiciona boxplot fake transparente para reservar espaço
                fig.add_trace(
                    go.Box(
                        y=[None],  # sem dados
                        name=legenda_niveis[nivel] if legenda_niveis[nivel] else nivel,
                        marker_color=cor_fake,
                        fillcolor=cor_fake,
                        legendgroup=nivel,
                        line=dict(color=cor_fake),
                        boxpoints=False,
                        showlegend=False,
                        width=0.3,
                        offsetgroup=nivel,
                        x=[nivel],
                        hoverinfo='skip'
                    ),
                    row=i, col=1
                )
        fig.update_xaxes(
            categoryorder='array',
            categoryarray=niveis,
            tickvals=niveis,
            ticktext=niveis,
            row=i, col=1
        )
        fig.update_yaxes(range=[0, 1000], row=i, col=1, title_text="Nota")
        
        df_brasil = df[(df['disciplina'] == disciplina) & (df['nivel'] == 'Brasil')]

        if not df_brasil.empty:
            mediana_brasil = df_brasil['mediana'].iloc[0]
            fig.add_trace(
                go.Scatter(
                    x=[niveis[0], niveis[-1]],  # Coordenadas extremas do eixo X
                    y=[mediana_brasil, mediana_brasil],
                    mode='lines',
                    line=dict(color="darkblue", width=1),
                    hoverinfo='text',
                    hovertext=f'Mediana {disciplina} Brasil: {mediana_brasil:.1f}',
                    showlegend=False
                ),
                row=i, col=1
            )

        tickvals = niveis
        ticktext = [legenda_niveis[nivel] if legenda_niveis[nivel] else nivel for nivel in niveis]

        fig.update_xaxes(
            categoryorder='array',
            categoryarray=niveis,
            tickvals=tickvals,
            ticktext=ticktext,
            row=i, col=1
        )
        fig.update_yaxes(range=[0, 1000], row=i, col=1, title_text="Nota")

    fig.update_layout(
        height=1000,
        width=400,
        showlegend=True,
        margin=dict(l=40, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )

    return fig