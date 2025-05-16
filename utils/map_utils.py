import os
import geopandas as gpd
import numpy as np
from db import get_session
import plotly.express as px
import plotly.graph_objects as go

def load_data(ano=None):
    session = get_session()
    query = "SELECT * FROM enem.mv_media_global_estado"
    if ano:
        query += f" WHERE nu_ano = {ano}"
    gdf = gpd.read_postgis(query, session.connection(), geom_col="wkb_geometry")
    session.close()
    return gdf

def get_map_figure(ano=None):
    gdf = load_data(ano)

    # Calculando min e max
    min_nota = gdf["media_global"].min()
    max_nota = gdf["media_global"].max()

    # Arredondando para números mais "amigáveis"
    min_nota_rounded = np.floor(min_nota / 100) * 100
    max_nota_rounded = np.ceil(max_nota / 100) * 100

    fig = go.Figure(go.Choroplethmapbox(
        geojson=gdf.__geo_interface__,
        locations=gdf["codigo_uf"],
        z=gdf["media_global"],
        featureidkey="properties.codigo_uf",
        text=gdf["estado"],
        hovertemplate="<b>%{text}</b><br>Nota média: %{z:.2f}<extra></extra>",
        colorscale='Blues',
        zmin=min_nota_rounded,
        zmax=max_nota_rounded,
        marker_opacity=0.7,
        marker_line_width=0.5,
        showscale=False,
    ))

    fig.update_layout(
        mapbox_style="mapbox://styles/ficast/cmaqktc0d01o301qo7c994rgz",
        mapbox_accesstoken=os.getenv("MAPBOX_ACCESS_TOKEN"),
        mapbox_zoom=3.5,
        mapbox_center={"lat": -14, "lon": -52},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        clickmode='event+select',
        paper_bgcolor="#D6D6D6",
        plot_bgcolor="#D6D6D6",
    )

    return fig, min_nota_rounded, max_nota_rounded