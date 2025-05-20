import time
from utils.constants import MAPBOX_ZOOM
import numpy as np

def atualizar_layout(fig, center_lat, center_lon, zoom):
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom
        )
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
    start_time = time.time()
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
    return MAPBOX_ZOOM
