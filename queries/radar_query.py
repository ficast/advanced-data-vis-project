import pandas as pd
from db import get_session


def load_areas_radar(nome_uf=None, nome_municipio=None, ano=None):
    """
    Carrega os dados para o radar da materialized view.

    Args:
        nome_uf (str, optional): Nome do estado para filtrar. Se None, retorna todos os estados.
        nome_municipio (str, optional): Nome do município para filtrar. Se None, retorna todos os municípios.
        ano (int, optional): Ano para filtrar. Se None, retorna todos os anos.

    Returns:
        pandas.DataFrame: DataFrame com os dados para o radar.
    """
    
    session = get_session()
    params = {}
    where_ano = ""
    if ano:
        where_ano = "AND nu_ano = %(ano)s"
        params['ano'] = ano

    query = f"""
    -- Brasil
    SELECT
        'Brasil' AS nivel,
        NULL AS estado,
        NULL AS municipio,
        AVG(avg_nota_lc) AS avg_nota_lc,
        AVG(avg_nota_ch) AS avg_nota_ch,
        AVG(avg_nota_cn) AS avg_nota_cn,
        AVG(avg_nota_mt) AS avg_nota_mt,
        AVG(avg_nota_redacao) AS avg_nota_redacao
    FROM enem.mv_media_global_municipio
    WHERE 1=1 {where_ano}

    UNION ALL

    -- Estado
    SELECT
        'Estado' AS nivel,
        nome_uf AS estado,
        NULL AS municipio,
        AVG(avg_nota_lc) AS avg_nota_lc,
        AVG(avg_nota_ch) AS avg_nota_ch,
        AVG(avg_nota_cn) AS avg_nota_cn,
        AVG(avg_nota_mt) AS avg_nota_mt,
        AVG(avg_nota_redacao) AS avg_nota_redacao
    FROM enem.mv_media_global_municipio
    WHERE nome_uf = %(nome_uf)s {where_ano}
    GROUP BY nome_uf

    UNION ALL

    -- Município
    SELECT
        'Municipio' AS nivel,
        nome_uf AS estado,
        nome_municipio AS municipio,
        AVG(avg_nota_lc) AS avg_nota_lc,
        AVG(avg_nota_ch) AS avg_nota_ch,
        AVG(avg_nota_cn) AS avg_nota_cn,
        AVG(avg_nota_mt) AS avg_nota_mt,
        AVG(avg_nota_redacao) AS avg_nota_redacao
    FROM enem.mv_media_global_municipio
    WHERE nome_uf = %(nome_uf)s AND nome_municipio = %(nome_municipio)s {where_ano}
    GROUP BY nome_uf, nome_municipio
    """

    params['nome_uf'] = nome_uf
    params['nome_municipio'] = nome_municipio

    try:
        df = pd.read_sql(query, session.connection(), params=params)
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        raise e
    finally:
        session.close()