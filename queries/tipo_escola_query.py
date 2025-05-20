
from db import get_session
import pandas as pd

from utils.constants import MAPPING_TP_ESCOLA_LABEL

def load_tipo_escola_data(ano=None, estado=None, municipio=None):
    session = get_session()
    sql = """
        SELECT
            nu_ano,
            local,
            estado,
            municipio,
            tp_escola_mapeada,
            quantidade_alunos,
            nota_media,
            q1,
            mediana,
            q3,
            notas_mil_redacao
        FROM enem.mv_notas_por_tipo_escola
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

    sql += " ORDER BY tp_escola_mapeada"
    
    try:
        df = pd.read_sql(sql, session.bind, params=params)
        df['tipo_escola_label'] = df['tp_escola_mapeada'].map(MAPPING_TP_ESCOLA_LABEL)
        return df
    except Exception as e:
        print(f"Erro ao carregar dados de tipo escola: {e}")
        return pd.DataFrame()
    finally:
        session.close()
