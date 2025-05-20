import pandas as pd
from db import get_session
import os

TIMELINE_QUERY = """
SELECT nu_ano, estado, AVG(media_global) AS media_global
FROM enem.mv_media_global_estado
GROUP BY nu_ano, estado

UNION ALL

SELECT nu_ano, 'Brasil' AS estado, AVG(media_global) AS media_global
FROM enem.mv_media_global_estado
GROUP BY nu_ano

ORDER BY nu_ano, estado;
"""

def load_timeline_data():
    """
    Carrega os dados da timeline do banco de dados.

    Returns:
        pandas.DataFrame: DataFrame com os dados da timeline.
    """
    
    if os.path.exists('cache/timeline_cache.csv'):
        df = pd.read_csv('cache/timeline_cache.csv')
        return df
    
    session = get_session()
    try:
        df = pd.read_sql(TIMELINE_QUERY, session.connection())
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()
    finally:
        session.close()
    
    # if not os.path.exists('cache/timeline_cache.csv'):
    #     df.to_csv('cache/timeline_cache.csv', index=False)
    
    # return df

def get_timeline_data(df, estado_selecionado):
    """
    Filtra os dados da timeline para o Brasil e estado selecionado.

    Args:
        df: DataFrame com os dados da timeline
        estado_selecionado: Nome do estado selecionado ou None

    Returns:
        tuple: (dados_brasil, dados_estado)
    """
    brasil = df[df['estado'] == 'Brasil'].sort_values('nu_ano')
    if estado_selecionado and estado_selecionado != "Brasil":
        estado = df[df['estado'] == estado_selecionado].sort_values('nu_ano')
    else:
        estado = None
    return brasil, estado
