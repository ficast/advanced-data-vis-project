from queries.municipios_query import load_municipios_data
import geopandas as gpd
import os

def load_map_data(ano=None, estado=None):
    """
    Carrega os dados do shapefile dos estados.

    Args:
        ano (int, optional): Ano específico para filtrar. Se None, retorna todos os anos.
        estado (str, optional): Estado específico para filtrar. Se None, retorna todos os estados.
    
    Returns:
        geopandas.GeoDataFrame: DataFrame com os dados do shapefile dos estados.
    """
    
    if os.path.exists('cache/shapefile_cache.geojson'):
        gdf = gpd.read_file('cache/shapefile_cache.geojson')
        if ano:
            gdf = gdf[gdf['nu_ano'] == ano]
        if estado:
            gdf = gdf[gdf['estado'] == estado]
            
    load_municipios_data()

    # else:
    #     query = "SELECT * FROM enem.mv_media_global_estado"
    #     if ano:
    #         query += f" WHERE nu_ano = {ano}"
    
    #     session = None
    #     try:
    #         session = get_session()
    #         gdf = gpd.read_postgis(query, session.connection(), geom_col="wkb_geometry")
            
    #         # save shapefile to cache se nao existir
    #         if not os.path.exists('cache/shapefile_cache.geojson'):
    #             gdf.to_file('shapefile_cache.geojson', driver='GeoJSON')
    #     finally:
    #         if session:
    #             session.close()
    
    return gdf
