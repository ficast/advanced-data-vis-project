import os
import pandas as pd
from queries.map_query import load_shapefile_data
import geopandas as gpd
import plotly.graph_objects as go
from queries.municipios_query import load_municipios_disponiveis
from db import get_session
from utils.constants import MIN_NOTA, MAX_NOTA
import numpy as np


def get_map_figure(ano=None, estado=None):
    # 1. Carrega dados dos estados
    estado_selecionado = estado if estado != "Brasil" else None
    gdf = load_shapefile_data(ano, estado_selecionado)

    # 2. Cria o trace base dos estados
    estados_trace = go.Choroplethmapbox(
        geojson=gdf.__geo_interface__,
        locations=gdf["codigo_uf"],
        z=gdf["media_global"],
        featureidkey="properties.codigo_uf",
        text=gdf["estado"],
        hovertemplate="<b>%{text}</b><br>Nota média: %{z:.2f}<extra></extra>",
        customdata=pd.Series(
            ["Estado"] * len(gdf)
        ),  # Mantém o customdata para identificação
        colorscale="Blues",
        zmin=MIN_NOTA,
        zmax=MAX_NOTA,
        marker_opacity=0.7,
        marker_line_width=0.5,
        showscale=False,
        name="Estados",
    )

    # 3. Inicializa a figura com o trace dos estados
    fig = go.Figure(data=[estados_trace])

    # 4. Adiciona o trace dos municípios se um estado estiver selecionado
    if estado and estado != "Brasil":
        df_municipios = load_municipios_disponiveis(ano, estado)

        if df_municipios is not None and not df_municipios.empty:
            municipios_trace = go.Scattermapbox(
                lat=df_municipios["lat"],
                lon=df_municipios["lng"],
                mode="markers",
                marker=go.scattermapbox.Marker(
                    size=7,
                    color=df_municipios["nota_total"],
                    colorscale="Reds",  # Mantém a mesma colorscale dos estados
                    opacity=0.8,
                    cmin=MIN_NOTA,
                    cmax=MAX_NOTA,
                ),
                text=df_municipios["nome_municipio"],
                hovertemplate="<b>%{text}</b><br>Nota média: %{customdata:.2f}<extra></extra>",
                customdata=df_municipios["nota_total"],
                name="Municípios",
            )
            fig.add_trace(municipios_trace)

    # 5. Define o layout do mapa
    fig.update_layout(
        mapbox_style="mapbox://styles/ficast/cmaqktc0d01o301qo7c994rgz",
        mapbox_accesstoken=os.getenv("MAPBOX_ACCESS_TOKEN"),
        mapbox_zoom=3.5,
        mapbox_center={"lat": -14, "lon": -52},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        clickmode="event+select",
        paper_bgcolor="#D6D6D6",
        plot_bgcolor="#D6D6D6",
    )

    return fig


def get_estado_coordinates(gdf, nome_estado):
    estado = gdf[gdf['estado'] == nome_estado]
    if not estado.empty:
        # Obtém os limites geográficos do estado
        bounds = estado.geometry.bounds.iloc[0]
        minx, miny, maxx, maxy = bounds
        # Calcula o centroide do estado
        center_lon = (minx + maxx) / 2
        center_lat = (miny + maxy) / 2
        return center_lat, center_lon
    return None, None

def calculate_zoom(gdf, nome_estado, mapbox_width, mapbox_height):
    estado = gdf[gdf['estado'] == nome_estado]
    if not estado.empty:
        # Obtém os limites geográficos do estado
        bounds = estado.geometry.bounds.iloc[0]
        minx, miny, maxx, maxy = bounds
        # Calcula a largura e a altura do estado em graus
        width = maxx - minx
        height = maxy - miny
        # Calcula o zoom ideal
        zoom_width = np.log2(360 * mapbox_width / (width * 256))
        zoom_height = np.log2(180 * mapbox_height / (height * 256))
        zoom = min(zoom_width, zoom_height)
        return zoom
    return 3