import pandas as pd
from db import get_session

def load_participantes_data(estado=None, municipio=None):
    """
    Carrega dados de participantes por ano, filtrando por estado e município se fornecidos
    """
    query = """
    SELECT * FROM mv_participantes_ano
    WHERE 1=1
    """
    if estado and estado != "Brasil":
        query += f" AND (nivel = 'Brasil' OR (nivel = 'Estado' AND LOWER(nome) = '{estado.lower()}') "
        if municipio:
            query += f" OR (nivel = 'Municipio' AND LOWER(nome) = '{municipio.lower()}')"
        query += ")"
        
    session = get_session()

    try:
        df = pd.read_sql(query, session.connection())
        df['nome'] = df['nome'].str.capitalize()
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()
    finally:
        session.close()