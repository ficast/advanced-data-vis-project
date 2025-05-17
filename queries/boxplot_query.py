from db import get_session
import pandas as pd

def load_box_plot_data(nome_estado=None, nome_municipio=None, ano=None):
    """
    Carrega os dados para o box plot da materialized view.

    Parameters:
    -----------
    nome_estado : str, optional
        Nome do estado para filtrar os dados
    nome_municipio : str, optional
        Nome do município para filtrar os dados
    ano : int, optional
        Ano para filtrar os dados. Se None, usa o ano mais recente

    Returns:
    --------
    pandas.DataFrame
        DataFrame com os dados para o box plot
    """
    try:
        session = get_session()

        # Query principal
        query = """
            SELECT *
            FROM enem.mv_box_plot_stats
            WHERE (%(ano)s IS NULL OR nu_ano = %(ano)s)
              AND (
                nivel = 'Brasil'
                OR (nivel = 'Estado' AND estado = %(nome_estado)s)
                OR (nivel = 'Municipio' AND municipio = %(nome_municipio)s)
              )
            ORDER BY
                CASE nivel
                    WHEN 'Brasil' THEN 1
                    WHEN 'Estado' THEN 2
                    WHEN 'Municipio' THEN 3
                END,
                disciplina;
        """

        # Parâmetros para a query
        params = {
            'nome_estado': nome_estado if nome_estado != "Brasil" else None,
            'nome_municipio': nome_municipio,
            'ano': ano
        }

        # Log dos parâmetros para debug
        print("Parâmetros da query:")
        print(f"- nome_estado: {params['nome_estado']}")
        print(f"- nome_municipio: {params['nome_municipio']}")
        print(f"- ano: {params['ano']}")

        # Executar a query
        df = pd.read_sql(query, session.connection(), params=params)

        # Log do resultado
        print(f"\nResultados obtidos:")
        print(f"- Total de linhas: {len(df)}")
        if not df.empty:
            print("- Níveis encontrados:", df['nivel'].unique())
            print("- Disciplinas encontradas:", df['disciplina'].unique())

        return df

    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        raise e

    finally:
        session.close()