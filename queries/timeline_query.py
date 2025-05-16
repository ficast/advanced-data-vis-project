import pandas as pd
from db import get_session

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
    """Carrega os dados da timeline do banco de dados."""
    session = get_session()
    df = pd.read_sql(TIMELINE_QUERY, session.connection())
    session.close()
    return df

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

if __name__ == "__main__":
    # Teste
    df = load_timeline_data()
    print("Shape:", df.shape)
    print("\nPrimeiras linhas:")
    print(df.head())

    # Teste com um estado
    brasil, estado = get_timeline_data(df, "São Paulo")
    print("\nDados do Brasil:")
    print(brasil.head())
    if estado is not None:
        print("\nDados de São Paulo:")
        print(estado.head())