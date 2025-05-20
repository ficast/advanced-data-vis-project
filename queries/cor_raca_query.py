import pandas as pd

from db import get_session

from utils.constants import MAPPING_COR_RACA_LABEL

def load_raca_data(ano=None, estado=None, municipio=None):
    session = get_session()
    sql = """
        SELECT
            nu_ano,
            local,
            estado,
            municipio,
            tp_cor_raca_mapeada,
            quantidade_alunos,
            nota_media,
            q1,
            mediana,
            q3,
            notas_mil_redacao
        FROM enem.mv_notas_por_raca
        WHERE 1=1
    """
    params = {}
    if ano:
        sql += " AND nu_ano = %(ano)s"
        params['ano'] = ano
    if estado and estado != "Brasil":
        sql += " AND local = %(estado)s"
        params['estado'] = estado
    elif municipio:
        sql += " AND local = %(municipio)s"
        params['municipio'] = municipio
    elif not estado and not municipio:
        sql += " AND local = 'Brasil'"

    sql += " ORDER BY tp_cor_raca_mapeada"

    try:
        df = pd.read_sql(sql, session.bind, params=params)
        df['raca_label'] = df['tp_cor_raca_mapeada'].map(MAPPING_COR_RACA_LABEL)
        return df
    except Exception as e:
        print(f"Erro ao carregar dados de raca: {e}")
        return pd.DataFrame()
    finally:
        session.close()