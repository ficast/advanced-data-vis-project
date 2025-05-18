from dash import dcc, html
from components.timeline import timeline
from components.scale import Scale
from queries.municipios_query import load_municipios_data
from queries.map_query import load_map_data
import plotly.graph_objects as go
import pandas as pd
import os
from utils.constants import MAPBOX_ACCESS_TOKEN, MAPBOX_CENTER, MAPBOX_STYLE, MAPBOX_ZOOM, MIN_NOTA, MAX_NOTA

def get_map_figure(ano=None, estado=None):
    # 1. Carrega dados dos estados
    estado_selecionado = estado if estado != "Brasil" else None
    gdf = load_map_data(ano, estado_selecionado)

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
        df_municipios = load_municipios_data(ano, estado)

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
        mapbox_style=MAPBOX_STYLE,
        mapbox_accesstoken=MAPBOX_ACCESS_TOKEN,
        mapbox_zoom=MAPBOX_ZOOM,
        mapbox_center=MAPBOX_CENTER,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        clickmode="event+select",
        paper_bgcolor="#D6D6D6",
        plot_bgcolor="#D6D6D6",
    )

    return fig

map = html.Div(
    className="map-content",
    children=[
        dcc.Graph(
            id="map-graph",
            figure=get_map_figure(),
            style={"height": "100%", "width": "100%", "position": "relative"},
            config={
                "scrollZoom": True,
                "displayModeBar": False,
                "doubleClick": "reset",
            },
        ),
        Scale(),
        timeline,
    ],
)
