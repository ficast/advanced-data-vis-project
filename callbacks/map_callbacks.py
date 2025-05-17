import pandas as pd
import dash
from dash import Input, Output, State
from queries.map_query import load_shapefile_data
import plotly.graph_objects as go
from app import app
from queries.municipios_query import load_municipios_disponiveis
from utils.map_utils import calculate_zoom, get_estado_coordinates
import os
from utils.constants import MIN_NOTA, MAX_NOTA

@app.callback(
    Output('nome-estado', 'children'),
    Input('map-graph', 'selectedData')
)
def atualizar_nome_estado(selectedData):
    if not selectedData or not selectedData.get('points'):
        return "Brasil"
    is_estado = selectedData['points'][0].get('customdata') == "Estado"
    # Só atualiza se for o trace dos estados (assumindo curveNumber 0)
    if is_estado:
        # Aqui você pode usar 'location' ou 'text' dependendo do seu trace
        return selectedData['points'][0].get('text', 'Desconhecido').strip()
    return dash.no_update  # Não atualiza se não for estado

@app.callback(
    Output('nome-municipio', 'children'),
    Input('map-graph', 'selectedData')
)
def atualizar_nome_municipio(selectedData):
    if not selectedData or not selectedData.get('points'):
        return ""
    is_estado = selectedData['points'][0].get('customdata') == "Estado"
    if not is_estado:
        return selectedData['points'][0].get('text', '').strip()
    return dash.no_update  # Não atualiza se não for município


@app.callback(
    Output('map-graph', 'figure'),
    [Input('map-graph', 'relayoutData'),
     Input('ano-selecionado', 'children'),
     Input('nome-estado', 'children')],
    State('map-graph', 'figure')
)
def atualizar_mapa(relayoutData, ano_selecionado, nome_estado, fig):
    # 1. Obter o zoom e o centro atuais do mapa
    zoom = 3.5
    center_lat = -14
    center_lon = -52

    if relayoutData:
        zoom = relayoutData.get('mapbox.zoom', zoom)
        center_lat = relayoutData.get('mapbox.center.lat', center_lat)
        center_lon = relayoutData.get('mapbox.center.lon', center_lon)

    # 2. Carrega dados necessários
    ano = int(ano_selecionado) if ano_selecionado else None
    gdf = load_shapefile_data(ano)
    estado_selecionado = nome_estado if nome_estado != "Brasil" else None
    
    # 3. Obter as coordenadas do estado selecionado
    if estado_selecionado:
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
        selected=dict(marker=dict(opacity=0.3)),
        unselected=dict(marker=dict(opacity=1)),
        marker_line_width=0.5,
        showscale=False,
        name='Estados'
    ))

    # 5. Adiciona municípios se um estado estiver selecionado
    if nome_estado != "Brasil":
        df_municipios = load_municipios_disponiveis(ano, nome_estado)
        if not df_municipios.empty:
            if nome_estado != "Brasil":
                estado_gdf = gdf[gdf['estado'] == nome_estado].copy()
                fig.add_trace(go.Choroplethmapbox(
                    geojson=estado_gdf.__geo_interface__,
                    locations=estado_gdf["codigo_uf"],
                    z=estado_gdf["media_global"],
                    featureidkey="properties.codigo_uf",
                    text=estado_gdf["estado"],
                    hovertemplate="<b>%{text}</b><br>Nota média: %{z:.2f}<extra></extra>",
                    customdata=pd.Series(["Estado"] * len(estado_gdf)),
                    colorscale=['#FFF4F0'] * len(estado_gdf),
                    zmin=MIN_NOTA,
                    zmax=MAX_NOTA,
                    marker_line_color='red',
                    marker_line_width=4,
                    showscale=False,
                    name='Estado Selecionado'
                ))
            fig.add_trace(go.Scattermapbox(
                lat=df_municipios['lat'],
                lon=df_municipios['lng'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=7,
                    color=df_municipios['nota_total'],
                    colorscale='Reds',
                    opacity=1,
                    cmin=MIN_NOTA,
                    cmax=MAX_NOTA,
                ),
                text=df_municipios['nome_municipio'],
                hovertemplate="<b>%{text}</b><br>Nota média: %{customdata:.2f}<extra></extra>",
                customdata=df_municipios['nota_total'],
                name='Municípios',
            ))

    # 6. Mantém o layout consistente
    fig.update_layout(
        mapbox_style="mapbox://styles/ficast/cmaqktc0d01o301qo7c994rgz",
        mapbox_accesstoken=os.getenv("MAPBOX_ACCESS_TOKEN"),
        mapbox_zoom=zoom,  # Mantém o zoom atual
        mapbox_center={"lat": center_lat, "lon": center_lon},  # Mantém o centro atual
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        clickmode='event+select',
        paper_bgcolor="#D6D6D6",
        plot_bgcolor="#D6D6D6",
    )

    return fig