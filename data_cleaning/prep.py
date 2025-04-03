import pandas as pd
import psycopg2
import io
import gc


def carregar_ano(arquivo_csv, ano):
    """
    Lê o CSV do ENEM referente a 'ano' e retorna um DataFrame pronto
    para inserir no banco. Aqui você adiciona todos os IFs e manipulações
    para as colunas que variam entre anos.
    """
    print(f"[INFO] Lendo arquivo {arquivo_csv} para o ano {ano}")

    df = pd.read_csv(arquivo_csv, sep=";", encoding="ISO-8859-1")

    # Variaveis finais TP_ESTADO_CIVIL
    SOLTEIRO_1 = 1
    CASADO_2 = 2
    DIVORCIADO_3 = 3
    VIUVO_4 = 4
    NAO_INFORMADO_0 = 0

    # Tratamento coluna TP_ESTADO_CIVIL
    if ano in [2014, 2015, 2016, 2018]:
        mapeamento_final_tp_estado_civil = {
            0: SOLTEIRO_1,  # Solteiro fica Solteiro
            1: CASADO_2,  # Casado fica Casado/Mora com companheiro
            2: DIVORCIADO_3,  # Divorciado fica Divorciado/Desquitado/Separado
            3: VIUVO_4,  # Viúvo fica Viúvo
            None: NAO_INFORMADO_0,  # Nones ficam Não informado
        }
        # 2014, 2015, 2016 e 2018 tem uma codificação diferente para o estado civil, portanto,
        # é necessário mapear para o padrão do banco. Ex: O que era 0 ficará 1, o que era 1 ficará 2, etc.
        df["TP_ESTADO_CIVIL"] = (
            df["TP_ESTADO_CIVIL"].map(mapeamento_final_tp_estado_civil).fillna(0)
        )

    # Variaveis finais TP_COR_RACA
    NAO_DISPOE_OU_NAO_DECLARADO_0 = 0
    BRANCA_1 = 1
    PRETA_2 = 2
    PARDA_3 = 3
    AMARELA_4 = 4
    INDIGENA_5 = 5

    # Tratamento coluna TP_COR_RACA
    if ano in [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]:
        mapeamento_final_tp_cor_raca = {
            0: NAO_DISPOE_OU_NAO_DECLARADO_0,  # Não declarado fica Não declarado
            1: BRANCA_1,  # Branca fica Branca
            2: PRETA_2,  # Preta fica Preta
            3: PARDA_3,  # Parda fica Parda
            4: AMARELA_4,  # Amarela fica Amarela
            5: INDIGENA_5,  # Indígena fica Indígena
            6: NAO_DISPOE_OU_NAO_DECLARADO_0,  # Não dispõe da informação fica Não informado
        }
        df["TP_COR_RACA"] = (
            df["TP_COR_RACA"].map(mapeamento_final_tp_cor_raca).fillna(0)
        )

    # Variaveis finais TP_NACIONALIDADE
    # NASCIONALIDADE_NAO_INFORMADA_0 = 0
    # BRASILEIRO_1 = 1
    # BRASILEIRO_NATURALIZADO_2 = 2
    # ESTRANGEIRO_3 = 3
    # BRASILEIRO_NASCIDO_NO_EXTERIOR_4 = 4

    # Variaveis finais TP_ST_CONCLUSAO
    # JA_CONCLUIU_1 = 1
    # CURSANDO_PARA_CONCLUIR_NO_ANO_DA_PROVA_2 = 2
    # CURSANDO_PARA_CONCLUIR_DEPOIS_DO_ANO_DA_PROVA_3 = 3
    # NAO_CONCLUI_E_NAO_CURSANDO_4 = 4

    # Tratamento coluna TP_ANO_CONCLUIU
    if ano in [2015, 2016]:
        mapeamento_2015_2016 = {
            0: NAO_INFORMADO_0,
            1: 2015,
            2: 2014,
            3: 2013,
            4: 2012,
            5: 2011,
            6: 2010,
            7: 2009,
            8: 2008,
            9: 2007,
            10: 2006,
        }
        df["TP_ANO_CONCLUIU"] = (
            df["TP_ANO_CONCLUIU"].map(mapeamento_2015_2016).fillna(0)
        )

    if ano == 2017:
        mapeamento_2017 = {
            0: NAO_INFORMADO_0,
            1: 2016,
            2: 2015,
            3: 2014,
            4: 2013,
            5: 2012,
            6: 2011,
            7: 2010,
            8: 2009,
            9: 2008,
            10: 2007,
            11: 2006,
        }
        df["TP_ANO_CONCLUIU"] = df["TP_ANO_CONCLUIU"].map(mapeamento_2017).fillna(0)

    if ano == 2018:
        mapeamento_2018 = {
            0: NAO_INFORMADO_0,
            1: 2017,
            2: 2016,
            3: 2015,
            4: 2014,
            5: 2013,
            6: 2012,
            7: 2011,
            8: 2010,
            9: 2009,
            10: 2008,
            11: 2007,
            12: 2006,
        }
        df["TP_ANO_CONCLUIU"] = df["TP_ANO_CONCLUIU"].map(mapeamento_2018).fillna(0)

    if ano == 2019:
        mapeamento_2019 = {
            0: NAO_INFORMADO_0,
            1: 2018,
            2: 2017,
            3: 2016,
            4: 2015,
            5: 2014,
            6: 2013,
            7: 2012,
            8: 2011,
            9: 2010,
            10: 2009,
            11: 2008,
            12: 2007,
            13: 2006,
        }
        df["TP_ANO_CONCLUIU"] = df["TP_ANO_CONCLUIU"].map(mapeamento_2019).fillna(0)

    if ano == 2020:
        mapeamento_2020 = {
            0: NAO_INFORMADO_0,
            1: 2019,
            2: 2018,
            3: 2017,
            4: 2016,
            5: 2015,
            6: 2014,
            7: 2013,
            8: 2012,
            9: 2011,
            10: 2010,
            11: 2009,
            12: 2008,
            13: 2007,
            14: 2006,
        }
        df["TP_ANO_CONCLUIU"] = df["TP_ANO_CONCLUIU"].map(mapeamento_2020).fillna(0)

    if ano == 2021:
        mapeamento_2021 = {
            0: NAO_INFORMADO_0,
            1: 2020,
            2: 2019,
            3: 2018,
            4: 2017,
            5: 2016,
            6: 2015,
            7: 2014,
            8: 2013,
            9: 2012,
            10: 2011,
            11: 2010,
            12: 2009,
            13: 2008,
            14: 2007,
            15: 2006,
        }

        df["TP_ANO_CONCLUIU"] = df["TP_ANO_CONCLUIU"].map(mapeamento_2021).fillna(0)

    if ano == 2022:
        mapeamento_2022 = {
            0: NAO_INFORMADO_0,
            1: 2021,
            2: 2020,
            3: 2019,
            4: 2018,
            5: 2017,
            6: 2016,
            7: 2015,
            8: 2014,
            9: 2013,
            10: 2012,
            11: 2011,
            12: 2010,
            13: 2009,
            14: 2008,
            15: 2007,
            16: 2006,
        }
        df["TP_ANO_CONCLUIU"] = df["TP_ANO_CONCLUIU"].map(mapeamento_2022).fillna(0)

    if ano == 2023:
        mapeamento_2023 = {
            0: NAO_INFORMADO_0,
            1: 2022,
            2: 2021,
            3: 2020,
            4: 2019,
            5: 2018,
            6: 2017,
            7: 2016,
            8: 2015,
            9: 2014,
            10: 2013,
            11: 2012,
            12: 2011,
            13: 2010,
            14: 2009,
            15: 2008,
            16: 2007,
            17: 2006,
        }
        df["TP_ANO_CONCLUIU"] = df["TP_ANO_CONCLUIU"].map(mapeamento_2023).fillna(0)

    df["TP_ANO_CONCLUIU"] = (
        pd.to_numeric(df["TP_ANO_CONCLUIU"], errors="coerce").fillna(0).astype(int)
    )

    # Tratamento coluna TP_ESCOLA

    # Variaveis finais TP_ESCOLA
    NAO_RESPONDEU_0 = 0
    PUBLICA_1 = 1
    PRIVADA_2 = 2
    EXTERIOR_3 = 3

    if ano in (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023):
        mapeamento_2015_2023 = {
            1: NAO_RESPONDEU_0,
            2: PUBLICA_1,
            3: PRIVADA_2,
            4: EXTERIOR_3,
        }
        df["TP_ESCOLA"] = df["TP_ESCOLA"].map(mapeamento_2015_2023).fillna(0)

    # Variaveis TP_ENSINO
    ENSINO_REGULAR_1 = 1
    EDUCACAO_ESPECIAL_2 = 2
    EJA_3 = 3

    if ano == 2014:
        mapeamento_2014 = {
            1: ENSINO_REGULAR_1,
            2: EDUCACAO_ESPECIAL_2,
            3: EJA_3,
            4: EJA_3,
        }
        df["TP_ENSINO"] = df["TP_ENSINO"].map(mapeamento_2014).fillna(0)

    # Variaveis TP_SIT_FUNC_ESC
    EM_ATIVIDADE_1 = 1
    PARALISADA_2 = 2
    EXTINTA_3 = 3

    if ano in (2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023):
        mapeamento_2015_2023 = {
            1: EM_ATIVIDADE_1,
            2: PARALISADA_2,
            3: EXTINTA_3,
            4: EXTINTA_3,
        }
        df["TP_SIT_FUNC_ESC"] = (
            df["TP_SIT_FUNC_ESC"].map(mapeamento_2015_2023).fillna(0)
        )

    # Variaveis ESCOLARIDADE_PAI e ESCOLARIDADE_MAE

    NAO_ESTUDOU_A = "A"
    ATE_5_SERIE_B = "B"
    ATE_9_SERIE_C = "C"
    MEDIO_INCOMPLETO_D = "D"
    MEDIO_COMPLETO_E = "E"
    SUPERIOR_COMPLETO_F = "F"
    POS_GRADUACAO_G = "G"
    NAO_SABE_H = "H"

    mapeamento_escolaridade_2014 = {
        "A": NAO_ESTUDOU_A,
        "B": ATE_5_SERIE_B,
        "C": ATE_9_SERIE_C,
        "D": MEDIO_INCOMPLETO_D,
        "E": MEDIO_COMPLETO_E,
        "F": MEDIO_COMPLETO_E,
        "G": SUPERIOR_COMPLETO_F,
        "H": POS_GRADUACAO_G,
        "I": NAO_SABE_H,
    }
    if not "ESCOLARIDADE_PAI" in df.columns:

        if ano == 2014:
            # criar a partir da variavel Q001
            df["ESCOLARIDADE_PAI"] = (
                df["Q001"].map(mapeamento_escolaridade_2014).fillna(NAO_SABE_H)
            )
        else:
            df["ESCOLARIDADE_PAI"] = df["Q001"].fillna(NAO_SABE_H)

    if not "ESCOLARIDADE_MAE" in df.columns:
        if ano == 2014:
            df["ESCOLARIDADE_MAE"] = (
                df["Q002"].map(mapeamento_escolaridade_2014).fillna(NAO_SABE_H)
            )
        else:
            df["ESCOLARIDADE_MAE"] = df["Q002"].fillna(NAO_SABE_H)

    # Variaveis RENDA_FAMILIAR:
    ATE_1_SALARIO_A = "A"
    DE_1_A_3_SALARIOS_B = "B"
    DE_3_A_6_SALARIOS_C = "C"
    DE_6_A_10_SALARIOS_D = "D"
    DE_10_A_20_SALARIOS_E = "E"
    MAIS_DE_20_SALARIOS_F = "F"
    NAO_INFORMADO_G = "G"

    mapeamento_renda = {
        "A": ATE_1_SALARIO_A,
        "B": ATE_1_SALARIO_A,
        "C": DE_1_A_3_SALARIOS_B,
        "D": DE_1_A_3_SALARIOS_B,
        "E": DE_1_A_3_SALARIOS_B,
        "F": DE_1_A_3_SALARIOS_B,
        "G": DE_3_A_6_SALARIOS_C,
        "H": DE_3_A_6_SALARIOS_C,
        "I": DE_3_A_6_SALARIOS_C,
        "J": DE_6_A_10_SALARIOS_D,
        "K": DE_6_A_10_SALARIOS_D,
        "L": DE_6_A_10_SALARIOS_D,
        "M": DE_6_A_10_SALARIOS_D,
        "N": DE_10_A_20_SALARIOS_E,
        "O": DE_10_A_20_SALARIOS_E,
        "P": DE_10_A_20_SALARIOS_E,
        "Q": MAIS_DE_20_SALARIOS_F,
    }

    if ano == 2014:
        df["RENDA_FAMILIAR"] = (
            df["Q003"].map(mapeamento_renda).fillna(NAO_INFORMADO_G)
        )
    else:
        df["RENDA_FAMILIAR"] = df["Q006"].map(mapeamento_renda).fillna(NAO_INFORMADO_G)

    # Variaveis ACESSO_INTERNET
    NAO_A = "A"
    SIM_B = "B"
    NAO_RESPONDEU_C = "C"

    if ano == 2014:
        mapeamento_acesso_internet_2014 = {
            "A": SIM_B,
            "B": SIM_B,
            "C": SIM_B,
            "D": NAO_A,
        }
        df["ACESSO_INTERNET"] = (
            df["Q017"].map(mapeamento_acesso_internet_2014).fillna(NAO_RESPONDEU_C)
        )
    else:
        df["ACESSO_INTERNET"] = df["Q025"].fillna(NAO_RESPONDEU_C)

    # ------------------------------------------------------------
    # 2) Tratamento das colunas que não precisam de mudança
    #    Exemplo: 'NU_ANO', 'TP_FAIXA_ETARIA' e 'TP_SEXO'
    #    Se esses nomes estiverem iguais em todos os anos,
    #    você simplesmente deixa como está ou só renomeia para minúsculo.
    # ------------------------------------------------------------
    # Ex.: df.rename(columns={'NU_ANO': 'nu_ano'}, inplace=True)
    # mas se "NU_ANO" já está do jeito que você quer, nem precisa renomear.

    # ------------------------------------------------------------
    # 3) Exemplo de coluna que varia conforme o ano:
    #    'TP_ESTADO_CIVIL' tem categorias diferentes dependendo do ano
    # ------------------------------------------------------------
    # if "TP_ESTADO_CIVIL" not in df.columns:
    #     # Se em algum ano essa coluna não existe, criar como None ou um valor default
    #     df["TP_ESTADO_CIVIL"] = None
    # else:
    #     # Se a coluna existe, mas muda a codificação para 2015, por exemplo:
    #     if ano == 2015:
    #         # Exemplo fictício:
    #         # Se 2015 traz "1=Solteiro,2=Casado,3=Outro" e
    #         # você quer padronizar para "1=Solteiro,2=Casado,4=Viúvo,5=Separado",
    #         # terá que mapear, algo como:
    #         mapeamento_2015 = {
    #             1: 1,  # Solteiro fica Solteiro
    #             2: 2,  # Casado fica Casado
    #             3: 5,  # "Outro" vira "Separado" (exemplo)
    #         }
    #         df["TP_ESTADO_CIVIL"] = df["TP_ESTADO_CIVIL"].map(mapeamento_2015).fillna(0)
    #     elif ano == 2016:
    #         # Exemplo: 2016 já veio no formato correto, então talvez não precise de nada
    #         pass
    #     # E assim por diante para cada ano...

    # ------------------------------------------------------------
    # 4) Exemplo de colunas que são idênticas para todos os anos,
    #    mas precisamos renomear para o padrão do banco:
    # ------------------------------------------------------------

    int_cols = [
        "NU_ANO",
        "TP_FAIXA_ETARIA",
        "TP_SEXO",
        "TP_ESTADO_CIVIL",
        "TP_COR_RACA",
        "TP_NACIONALIDADE",
        "TP_ST_CONCLUSAO",
        "TP_ANO_CONCLUIU",
        "TP_ESCOLA",
        "TP_ENSINO",
        "CO_MUNICIPIO_ESC",
        "CO_UF_ESC",
        "TP_DEPENDENCIA_ADM_ESC",
        "TP_LOCALIZACAO_ESC",
        "TP_SIT_FUNC_ESC",
        "CO_MUNICIPIO_PROVA",
        "CO_UF_PROVA",
    ]
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    col_map = {
        "NU_ANO": "nu_ano",
        "TP_FAIXA_ETARIA": "tp_faixa_etaria",
        "TP_SEXO": "tp_sexo",
        "TP_ESTADO_CIVIL": "tp_estado_civil",
        "TP_COR_RACA": "tp_cor_raca",
        "TP_NACIONALIDADE": "tp_nacionalidade",
        "TP_ST_CONCLUSAO": "tp_st_conclusao",
        "TP_ANO_CONCLUIU": "tp_ano_concluiu",
        "TP_ESCOLA": "tp_escola",
        "TP_ENSINO": "tp_ensino",
        "CO_MUNICIPIO_ESC": "co_municipio_esc",
        "NO_MUNICIPIO_ESC": "no_municipio_esc",
        "CO_UF_ESC": "co_uf_esc",
        "SG_UF_ESC": "sg_uf_esc",
        "TP_DEPENDENCIA_ADM_ESC": "tp_dependencia_adm_esc",
        "TP_LOCALIZACAO_ESC": "tp_localizacao_esc",
        "TP_SIT_FUNC_ESC": "tp_sit_func_esc",
        "CO_MUNICIPIO_PROVA": "co_municipio_prova",
        "NO_MUNICIPIO_PROVA": "no_municipio_prova",
        "CO_UF_PROVA": "co_uf_prova",
        "SG_UF_PROVA": "sg_uf_prova",
        "NU_NOTA_CN": "nu_nota_cn",
        "NU_NOTA_CH": "nu_nota_ch",
        "NU_NOTA_LC": "nu_nota_lc",
        "NU_NOTA_MT": "nu_nota_mt",
        "NU_NOTA_REDACAO": "nu_nota_redacao",
        "ESCOLARIDADE_PAI": "escolaridade_pai",
        "ESCOLARIDADE_MAE": "escolaridade_mae",
        "RENDA_FAMILIAR": "renda_familiar",
        "ACESSO_INTERNET": "acesso_internet",
        # e assim por diante para todas as colunas que você tiver
    }
    df.rename(columns=col_map, inplace=True)

    # ------------------------------------------------------------
    # 5) Ajustar ordem e garantir que todas colunas existem
    #    (criando colunas ausentes se necessário)
    # ------------------------------------------------------------
    colunas_finais = [
        "nu_ano",
        "tp_faixa_etaria",
        "tp_sexo",
        "tp_estado_civil",
        "tp_cor_raca",
        "tp_nacionalidade",
        "tp_st_conclusao",
        "tp_ano_concluiu",
        "tp_escola",
        "tp_ensino",
        "co_municipio_esc",
        "no_municipio_esc",
        "co_uf_esc",
        "sg_uf_esc",
        "tp_dependencia_adm_esc",
        "tp_localizacao_esc",
        "tp_sit_func_esc",
        "co_municipio_prova",
        "no_municipio_prova",
        "co_uf_prova",
        "sg_uf_prova",
        "nu_nota_cn",
        "nu_nota_ch",
        "nu_nota_lc",
        "nu_nota_mt",
        "nu_nota_redacao",
        "escolaridade_pai",
        "escolaridade_mae",
        "renda_familiar",
        "acesso_internet",
    ]

    for col in colunas_finais:
        if col not in df.columns:
            df[col] = None

    df = df.reindex(columns=colunas_finais)

    # ------------------------------------------------------------
    # 6) Fazer outras conversões de tipo, se for o caso
    # ------------------------------------------------------------
    # Exemplo: converter nu_ano para int
    df["nu_ano"] = pd.to_numeric(df["nu_ano"], errors="coerce").fillna(-1).astype(int)

    return df


def inserir_no_banco(df, conn_info):
    """
    Insere o DataFrame df na tabela enem.microdados usando COPY.
    Ajuste o nome da tabela/colunas conforme seu CREATE TABLE.
    """
    conn = psycopg2.connect(**conn_info)
    cur = conn.cursor()

    buffer = io.StringIO()
    # Gera CSV em memória (sem header, delimitador ';')
    df.to_csv(buffer, index=False, header=False, sep=";")
    buffer.seek(0)

    copy_sql = """
        COPY enem.microdados (
            nu_ano,
            tp_faixa_etaria,
            tp_sexo,
            tp_estado_civil,
            tp_cor_raca,
            tp_nacionalidade,
            tp_st_conclusao,
            tp_ano_concluiu,
            tp_escola,
            tp_ensino,
            co_municipio_esc,
            no_municipio_esc,
            co_uf_esc,
            sg_uf_esc,
            tp_dependencia_adm_esc,
            tp_localizacao_esc,
            tp_sit_func_esc,
            co_municipio_prova,
            no_municipio_prova,
            co_uf_prova,
            sg_uf_prova,
            nu_nota_cn,
            nu_nota_ch,
            nu_nota_lc,
            nu_nota_mt,
            nu_nota_redacao,
            escolaridade_pai,
            escolaridade_mae,
            renda_familiar,
            acesso_internet
        )
        FROM STDIN
        DELIMITER ';'
        CSV
    """
    cur.copy_expert(sql=copy_sql, file=buffer)
    conn.commit()
    cur.close()
    conn.close()


def main():
    conn_info = {
        "host": "localhost",
        "port": 5434,
        "dbname": "enem",
        "user": "admin",
        "password": "%8f3pE%ykKvj",
    }

    anos_e_arquivos = [
        (2014, "enem_database/data/MICRODADOS_ENEM_2014.csv"),
        (2015, "enem_database/data/MICRODADOS_ENEM_2015.csv"),
        (2016, "enem_database/data/MICRODADOS_ENEM_2016.csv"),
        (2017, "enem_database/data/MICRODADOS_ENEM_2017.csv"),
        (2018, "enem_database/data/MICRODADOS_ENEM_2018.csv"),
        (2019, "enem_database/data/MICRODADOS_ENEM_2019.csv"),
        (2020, "enem_database/data/MICRODADOS_ENEM_2020.csv"),
        (2021, "enem_database/data/MICRODADOS_ENEM_2021.csv"),
        (2022, "enem_database/data/MICRODADOS_ENEM_2022.csv"),
        (2023, "enem_database/data/MICRODADOS_ENEM_2023.csv"),
    ]

    for ano, arquivo_csv in anos_e_arquivos:
        df = carregar_ano(arquivo_csv, ano)
        print(f"[INFO] Inserindo ano {ano} no banco de dados...")
        inserir_no_banco(df, conn_info)
        print(f"[OK] Ano {ano} concluído!\n")
        df = None
        gc.collect()

    print("[FIM] Script finalizado.")


if __name__ == "__main__":
    main()
