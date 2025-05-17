from dash import Output, Input, State
from app import app
from components.boxplot import create_box_plots
from queries.boxplot_query import load_box_plot_data
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
    df = load_box_plot_data(nome_estado=nome_estado,
                           nome_municipio=nome_municipio,
                           ano=ano)
    fig = create_box_plots(df, nome_estado, nome_municipio)
    return fig

@app.callback(
    Output('box-plots', 'figure', allow_duplicate=True),
    Input('radar-areas', 'restyleData'),
    State('box-plots', 'figure'),
    State('radar-areas', 'figure'),
    prevent_initial_call=True
)
def sync_radar_to_boxplot(radar_restyle, boxplot_fig, radar_fig):
    if radar_restyle is None:
        return boxplot_fig

    # Descobre qual grupo foi clicado
    toggled_idx = radar_restyle[1][0]

    # Acessa o nome de forma segura
    toggled_trace = radar_fig['data'][toggled_idx]
    toggled_name = toggled_trace.get('name', None)

    if toggled_name is None:
        return boxplot_fig

    new_visibility = radar_restyle[0]['visible'][0]

    # Atualiza todos os traces do boxplot com o mesmo name
    for trace in boxplot_fig['data']:
        if trace.get('name', '') == toggled_name:
            trace['visible'] = new_visibility

    return boxplot_fig

@app.callback(
    Output('radar-areas', 'figure', allow_duplicate=True),
    Input('box-plots', 'restyleData'),
    State('radar-areas', 'figure'),
    State('box-plots', 'figure'),
    prevent_initial_call=True
)
def sync_boxplot_to_radar(boxplot_restyle, radar_fig, boxplot_fig):
    if boxplot_restyle is None:
        return radar_fig

    # Descobre qual grupo foi clicado
    toggled_idx = boxplot_restyle[1][0]

    # Acessa o nome de forma segura
    toggled_trace = boxplot_fig['data'][toggled_idx]
    toggled_name = toggled_trace.get('name', None)

    if toggled_name is None:
        return radar_fig

    new_visibility = boxplot_restyle[0]['visible'][0]

    # Atualiza todos os traces do radar com o mesmo name
    for trace in radar_fig['data']:
        if trace.get('name', '') == toggled_name:
            trace['visible'] = new_visibility

    return radar_fig