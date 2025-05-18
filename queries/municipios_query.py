import pandas as pd
import os

from db import get_session

def load_municipios_data(ano=None, estado=None, municipio=None):
    """
    Carrega os municípios disponíveis com suas coordenadas e notas.

    Args:
        ano (int, optional): Ano específico para filtrar. Se None, retorna média de todos os anos.
        estado (str, optional): Estado para filtrar.

    Returns:
        pandas.DataFrame: DataFrame com os municípios, suas coordenadas e notas.
    """
    if not estado:
        return None

    if os.path.exists('cache/municipios_cache.csv'):
        df = pd.read_csv('cache/municipios_cache.csv')

        # Filtra pelo estado
        df = df[df['nome_uf'] == estado]
        
        if municipio:
            df = df[df['nome_municipio'] == municipio]
            return df.reset_index(drop=True)

        if ano:
            # Filtra pelo ano, retorna normalmente
            df = df[df['nu_ano'] == ano]
            return df.reset_index(drop=True)
        else:
            # Agrega por município: média das notas, pega o primeiro lat/lng
            df_agg = (
                df.groupby(['codigo_municipio', 'nome_municipio'], as_index=False)
                .agg({
                    'nota_total': 'mean',
                    'lat': 'first',
                    'lng': 'first'
                })
            )
            return df_agg.reset_index(drop=True)
    return None
    
    
    # if not estado and not ano:
    #     return None
    
    # session = get_session()
    
    # if estado and ano:
    #     query = """
    #     SELECT
    #         codigo_municipio,
    #         nome_municipio,
    #         sigla_uf,
    #         nome_uf,
    #         lat,
    #         lng,
    #         nota_total,
    #         avg_nota_cn,
    #         avg_nota_ch,
    #         avg_nota_lc,
    #         avg_nota_mt,
    #         avg_nota_redacao,
    #         nu_ano
    #     FROM enem.mv_media_global_municipio
    #     WHERE nu_ano = %(ano)s AND nome_uf = %(estado)s
    #     ORDER BY nome_uf, nome_municipio
    #     """
        
    #     df = pd.read_sql(query, session.connection(), params={"ano": ano, "estado": estado})
    # elif ano:
    #     query = """
    #     SELECT
    #         codigo_municipio,
    #         nome_municipio,
    #         sigla_uf,
    #         nome_uf,
    #         lat,
    #         lng,
    #         nota_total,
    #         avg_nota_cn,
    #         avg_nota_ch,
    #         avg_nota_lc,
    #         avg_nota_mt,
    #         avg_nota_redacao,
    #         nu_ano
    #     FROM enem.mv_media_global_municipio
    #     WHERE nu_ano = %(ano)s
    #     ORDER BY sigla_uf, nome_municipio
    #     """
    #     df = pd.read_sql(query, session.connection(), params={"ano": ano})
    # elif estado:
    #     query = """
    #     SELECT
    #         codigo_municipio,
    #         nome_municipio,
    #         sigla_uf,
    #         nome_uf,
    #         lat,
    #         lng,
    #         nota_total,
    #         avg_nota_cn,
    #         avg_nota_ch,
    #         avg_nota_lc,
    #         avg_nota_mt,
    #         avg_nota_redacao,
    #         nu_ano
    #     FROM enem.mv_media_global_municipio
    #     WHERE nome_uf = %(estado)s
    #     ORDER BY nome_uf, nome_municipio
    #     """
    #     df = pd.read_sql(query, session.connection(), params={"estado": estado})
    # else:
    #     query = """
    #     SELECT
    #         codigo_municipio,
    #         nome_municipio,
    #         sigla_uf,
    #         nome_uf,
    #         lat,
    #         lng,
    #         nota_total,
    #         avg_nota_cn,
    #         avg_nota_ch,
    #         avg_nota_lc,
    #         avg_nota_mt,
    #         avg_nota_redacao,
    #         nu_ano
    #     FROM enem.mv_media_global_municipio
    #     ORDER BY nome_uf, nome_municipio
    #     """
    #     df = pd.read_sql(query, session.connection())
    #     # save df to csv
    #     df.to_csv('cache/municipios_cache.csv', index=False)
    # session.close()
    # return df
