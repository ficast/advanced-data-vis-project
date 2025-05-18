from utils.constants import FAIXAS_RENDA
from db import get_session
import pandas as pd

def load_renda_familiar_data(ano=None, estado=None, municipio=None):
    """
    Carrega dados da MV de notas por renda.
    """
    session = get_session()

    sql = """
        SELECT
            nu_ano,
            local,
            estado,
            municipio,
            renda_familiar,
            quantidade_alunos,
            nota_media,
            q1,
            mediana,
            q3,
            notas_mil_redacao
        FROM enem.mv_notas_por_renda
        WHERE 1=1
    """
    params = {}

    if ano:
        sql += " AND nu_ano = %(ano)s"
        params['ano'] = ano

    if municipio:
        sql += " AND local = %(municipio)s"
        params['municipio'] = municipio
    elif estado:
        sql += " AND local = %(estado)s"
        params['estado'] = estado

    sql += """
        ORDER BY
            local,
            CASE renda_familiar
                WHEN 'A' THEN 1
                WHEN 'B' THEN 2
                WHEN 'C' THEN 3
                WHEN 'D' THEN 4
                WHEN 'E' THEN 5
                WHEN 'F' THEN 6
                WHEN 'G' THEN 7
            END
    """

    try:
        df = pd.read_sql(sql, session.bind, params=params)
        df['faixa_renda_label'] = df['renda_familiar'].map(FAIXAS_RENDA)
        if ano is None:
            group_cols = ['faixa_renda_label', 'local']
            df_grouped = df.groupby(group_cols, as_index=False).agg({
                'quantidade_alunos': 'sum',
                'nota_media': 'mean',
                'q1': 'mean',
                'mediana': 'mean',
                'q3': 'mean',
                'notas_mil_redacao': 'sum',
            })
            anos = df.groupby(group_cols)['nu_ano'].unique().reset_index()
            anos['nu_ano'] = anos['nu_ano'].apply(lambda x: ','.join(map(str, sorted(x))))
            df_grouped = df_grouped.merge(anos, on=group_cols, how='left')
            df = df_grouped
        # convert quantidade_alunos to float
        df['quantidade_alunos'] = df['quantidade_alunos'].astype(float)
        return df
    except Exception as e:
        print(f"Erro ao carregar dados da MV: {e}")
        return None
    finally:
        session.close()
        