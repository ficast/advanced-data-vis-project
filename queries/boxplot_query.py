from db import get_session
import pandas as pd


def load_boxplot_data(nome_estado=None, nome_municipio=None, ano=None):
    """
    Carrega os dados para o box plot da materialized view.

    Args:
        nome_estado : str, optional
            Nome do estado para filtrar os dados
    nome_municipio : str, optional
        Nome do município para filtrar os dados
    ano : int, optional
        Ano para filtrar os dados. Se None, usa o ano mais recente

    Returns:
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
                OR (nivel = 'Estado' AND LOWER(estado) = %(nome_estado)s)
                OR (nivel = 'Municipio' AND LOWER(municipio) = %(nome_municipio)s)
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
            "nome_estado": nome_estado.lower() if nome_estado != "Brasil" else None,
            "nome_municipio": nome_municipio.lower() if nome_municipio else None,
            "ano": ano,
        }
        # Executar a query
        df = pd.read_sql(query, session.connection(), params=params)
        return df

    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

    finally:
        session.close()
