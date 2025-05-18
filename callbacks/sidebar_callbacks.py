from dash import Output, Input, State, callback_context
from app import app
from components.boxplot import create_box_plots
from components.participantes import create_participantes_figure
from queries.participantes_query import load_participantes_data
from queries.boxplot_query import load_boxplot_data
from queries.radar_query import load_areas_radar
from components.radar_areas import radar_areas


@app.callback(
    Output('limpar-ano', 'style'),
    Input('ano-selecionado', 'children')
)
def mostrar_ou_ocultar_botao_limpar(ano_selecionado):
    if ano_selecionado and ano_selecionado.strip() != "":
        return {"display": "inline-block"}
    else:
        return {"display": "none"}
    


@app.callback(
    Output('radar-areas', 'figure'),
    [Input('nome-estado', 'children'), 
     Input('nome-municipio', 'children'), 
     Input('ano-selecionado', 'children')]
)
def atualizar_radar(nome_estado, nome_municipio, ano_selecionado):
    ano = int(ano_selecionado) if ano_selecionado else None
    df_areas = load_areas_radar(nome_uf=nome_estado, nome_municipio=nome_municipio, ano=ano)
    return radar_areas(df_areas, nome_estado, nome_municipio)


@app.callback(
    Output('box-plots', 'figure'),
    [Input('nome-estado', 'children'),
     Input('nome-municipio', 'children'),
     Input('ano-selecionado', 'children')]
)
def atualizar_box_plots(nome_estado, nome_municipio, ano_selecionado):
    ano = int(ano_selecionado) if ano_selecionado and ano_selecionado.strip() else None
    df = load_boxplot_data(nome_estado=nome_estado,
                           nome_municipio=nome_municipio,
                           ano=ano)
    fig = create_box_plots(df, nome_estado, nome_municipio)
    return fig

@app.callback(
    Output('participantes-graph', 'figure'),
    [Input('nome-estado', 'children'),
     Input('nome-municipio', 'children')]
)
def update_participantes_graph(estado, municipio):
    # Se estado for "Brasil", passa None
    estado_param = None if estado == "Brasil" else estado
    # Se municipio for vazio ou None, passa None
    municipio_param = None if not municipio else municipio

    df = load_participantes_data(estado_param, municipio_param)
    return create_participantes_figure(df, estado_param, municipio_param)


def get_toggle_info(restyle_data, source_fig):
    """Extrai informações sobre qual trace foi alterado"""
    if restyle_data is None:
        return None, None

    toggled_idx = restyle_data[1][0]
    toggled_trace = source_fig['data'][toggled_idx]
    toggled_name = toggled_trace.get('name', None)
    new_visibility = restyle_data[0]['visible'][0]

    return toggled_name, new_visibility


def update_traces_visibility(fig, name, visibility):
    """Atualiza a visibilidade dos traces com o nome especificado"""
    if name is None:
        return fig

    for trace in fig['data']:
        if trace.get('name', '') == name:
            trace['visible'] = visibility
    return fig

@app.callback(
    [Output('radar-areas', 'figure', allow_duplicate=True),
     Output('box-plots', 'figure', allow_duplicate=True),
     Output('participantes-graph', 'figure', allow_duplicate=True)],
    [Input('radar-areas', 'restyleData'),
     Input('box-plots', 'restyleData'),
     Input('participantes-graph', 'restyleData')],
    [State('radar-areas', 'figure'),
     State('box-plots', 'figure'),
     State('participantes-graph', 'figure')],
    prevent_initial_call=True
)
def sync_all_graphs(radar_restyle, boxplot_restyle, participantes_restyle,
                   radar_fig, boxplot_fig, participantes_fig):
    """Sincroniza a visibilidade das legendas entre todos os gráficos"""

    ctx = callback_context
    if not ctx.triggered:
        return radar_fig, boxplot_fig, participantes_fig

    # Identifica qual gráfico disparou o callback
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    # Mapeia os inputs com suas figuras correspondentes
    restyle_map = {
        'radar-areas': (radar_restyle, radar_fig),
        'box-plots': (boxplot_restyle, boxplot_fig),
        'participantes-graph': (participantes_restyle, participantes_fig)
    }

    # Obtém as informações do trace que foi alterado
    restyle_data, source_fig = restyle_map[trigger]
    toggled_name, new_visibility = get_toggle_info(restyle_data, source_fig)

    if toggled_name is None:
        return radar_fig, boxplot_fig, participantes_fig

    # Atualiza todos os gráficos
    radar_fig = update_traces_visibility(radar_fig, toggled_name, new_visibility)
    boxplot_fig = update_traces_visibility(boxplot_fig, toggled_name, new_visibility)
    participantes_fig = update_traces_visibility(participantes_fig, toggled_name, new_visibility)

    return radar_fig, boxplot_fig, participantes_fig