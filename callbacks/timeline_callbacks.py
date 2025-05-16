from dash import Input, Output, State, callback_context
import plotly.graph_objects as go
from app import app
from queries.timeline_query import load_timeline_data

# Carrega todos os dados uma vez
df_timeline = load_timeline_data()

@app.callback(
    Output('timeline-graph', 'figure'),
    Input('nome-estado', 'children')
)
def atualizar_timeline(nome_estado):
    fig = go.Figure()

    # Linha do Brasil (sempre)
    brasil = df_timeline[df_timeline['estado'] == 'Brasil'].sort_values('nu_ano')
    fig.add_trace(go.Scatter(
        x=brasil['nu_ano'],
        y=brasil['media_global'],
        mode='lines+markers',
        name='Brasil',
        line=dict(color='blue', width=3)
    ))

    # Linha do estado selecionado (se não for Brasil)
    if nome_estado and nome_estado != "Brasil" and nome_estado in df_timeline['estado'].unique():
        estado = df_timeline[df_timeline['estado'] == nome_estado].sort_values('nu_ano')
        fig.add_trace(go.Scatter(
            x=estado['nu_ano'],
            y=estado['media_global'],
            mode='lines+markers',
            name=nome_estado,
            line=dict(color='orange', width=3)
        ))

    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=100,
        xaxis_title="ANO",
        xaxis_tickfont=dict(size=12),
        yaxis_title="MÉDIA",
        yaxis_tickfont=dict(size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        template="plotly_white"
    )

    return fig


@app.callback(
    Output('ano-selecionado', 'children'),
    [Input('timeline-graph', 'clickData'), Input('limpar-ano', 'n_clicks')],
    State('ano-selecionado', 'children')
)
def selecionar_ano_timeline(clickData, n_clicks, ano_anterior):
    ctx = callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    print("clickData:", clickData)
    print("n_clicks:", n_clicks)
    print("ano_anterior:", ano_anterior)
    print("trigger:", trigger)
    if not ctx.triggered:
        return ano_anterior or ""
    if trigger == 'limpar-ano':
        return ""
    if clickData and 'points' in clickData and len(clickData['points']) > 0:
        ano = clickData['points'][0]['x']
        return str(ano)
    return ano_anterior or ""