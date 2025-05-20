import pandas as pd
import dash
from dash import Input, Output, State
from queries.map_query import load_map_data
import plotly.graph_objects as go
from app import app
from queries.municipios_query import load_municipios_data
from utils.map_utils import calculate_zoom, get_estado_coordinates
from utils.constants import (
    COLOR_ESTADO,
    MAPBOX_ACCESS_TOKEN,
    MAPBOX_CENTER,
    MAPBOX_STYLE,
    MAPBOX_ZOOM,
    MIN_NOTA,
    MAX_NOTA,
)


@app.callback(Output("nome-estado", "children"), Input("map-graph", "selectedData"))
def atualizar_nome_estado(selectedData):
    if not selectedData or not selectedData.get("points"):
        return "Brasil"
    is_estado = selectedData["points"][0].get("customdata") == "Estado"
    # Só atualiza se for o trace dos estados (assumindo curveNumber 0)
    if is_estado:
        # Aqui você pode usar 'location' ou 'text' dependendo do seu trace
        return selectedData["points"][0].get("text", "Desconhecido").strip()
    return dash.no_update  # Não atualiza se não for estado


@app.callback(Output("nome-municipio", "children"), Input("map-graph", "selectedData"))
def atualizar_nome_municipio(selectedData):
    if not selectedData or not selectedData.get("points"):
        return ""
    is_estado = selectedData["points"][0].get("customdata") == "Estado"
    if not is_estado:
        return selectedData["points"][0].get("text", "").strip()
    return dash.no_update  # Não atualiza se não for município


# # alternative version of alterar mapa
@app.callback(
    Output('map-graph', 'figure'),
    [Input('map-graph', 'relayoutData'),
     Input('ano-selecionado', 'children'),
     Input('nome-estado', 'children'),
     Input('nome-municipio', 'children')
     ],
    State('map-graph', 'figure')
)
def atualizar_mapa(relayoutData, ano_selecionado, nome_estado, nome_municipio, fig_state):
    # Defaults
    zoom = MAPBOX_ZOOM
    center_lat = MAPBOX_CENTER['lat']
    center_lon = MAPBOX_CENTER['lon']
    
    if fig_state and 'layout' in fig_state and 'mapbox' in fig_state['layout']:
        zoom = fig_state['layout']['mapbox'].get('zoom', zoom)
        center_lat = fig_state['layout']['mapbox']['center'].get('lat', center_lat)
        center_lon = fig_state['layout']['mapbox']['center'].get('lon', center_lon)

    ctx = dash.callback_context
    if not ctx.triggered:
        return fig_state  # Retorna o mapa anterior se nenhum input foi alterado

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # 1. Carrega dados
    ano = int(ano_selecionado) if ano_selecionado else None
    gdf = load_map_data(ano)
    estado_selecionado = nome_estado if nome_estado != "Brasil" else None

    # 2. Se um estado está selecionado, calcula centro e zoom
    if (trigger_id == 'nome-estado' and estado_selecionado):
        center_lat, center_lon = get_estado_coordinates(gdf, estado_selecionado)
        zoom = calculate_zoom(gdf, estado_selecionado, 800, 600)
        
    # 4. Cria figura base com os estados
    fig = go.Figure(go.Choroplethmapbox(
        geojson=gdf.__geo_interface__,
        locations=gdf["codigo_uf"],
        z=gdf["media_global"],
        featureidkey="properties.codigo_uf",
        text=gdf["estado"],
        hovertemplate="<b>%{text}</b><br>Nota média: %{z:.2f}<extra></extra>",
        customdata=pd.Series(["Estado"] * len(gdf)),
        colorscale='Blues',
        zmin=MIN_NOTA,
        zmax=MAX_NOTA,
        marker_opacity=1,
        marker_line_width=0.5,
        showscale=False,
        name='Estados'
    ))

    # 5. Adiciona destaque e municípios se um estado está selecionado
    if estado_selecionado:
        estado_gdf = gdf[gdf['estado'] == estado_selecionado].copy()
        fig.add_trace(go.Choroplethmapbox(
            geojson=estado_gdf.__geo_interface__,
            locations=estado_gdf["codigo_uf"],
            z=estado_gdf["media_global"],
            featureidkey="properties.codigo_uf",
            text=estado_gdf["estado"],
            hovertemplate="<b>%{text}</b><br>Nota média: %{z:.2f}<extra></extra>",
            customdata=pd.Series(["Estado"] * len(estado_gdf)),
            colorscale='Reds',
            zmin=MIN_NOTA,
            zmax=MAX_NOTA,
            marker_opacity=0.2,
            marker_line_color=COLOR_ESTADO,
            marker_line_width=4,
            showscale=False,
            name='Estado Selecionado'
        ))

        # Carrega municípios
        df_municipios = load_municipios_data(ano, estado_selecionado)
        if not df_municipios.empty:
            fig.add_trace(go.Scattermapbox(
                lat=df_municipios['lat'],
                lon=df_municipios['lng'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color=df_municipios['nota_total'],
                    colorscale='Reds',
                    opacity=0.8,
                    cmin=MIN_NOTA,
                    cmax=MAX_NOTA,
                ),
                text=df_municipios['nome_municipio'],
                hovertemplate="<b>%{text}</b><br>Nota média: %{customdata:.2f}<extra></extra>",
                customdata=df_municipios['nota_total'],
                name='Municípios',
            ))

    # 6. Layout
    fig.update_layout(
        mapbox_style=MAPBOX_STYLE,
        mapbox_accesstoken=MAPBOX_ACCESS_TOKEN,
        mapbox_zoom=zoom,
        mapbox_center={"lat": center_lat, "lon": center_lon},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        clickmode='event+select',
        paper_bgcolor="#D6D6D6",
        plot_bgcolor="#D6D6D6",
    )
    return fig