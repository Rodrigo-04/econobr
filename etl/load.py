"""
load.py

Responsável por conectar no SQL Server e gravar os dados já transformados,
evitando duplicatas (insere se a data não existir, atualiza se já existir).
"""

import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env e disponibiliza as variáveis via os.getenv()


def obter_conexao() -> pyodbc.Connection:
    """
    Abre uma conexão com o SQL Server usando as credenciais do .env.
    """
    servidor = os.getenv("DB_SERVER")
    banco = os.getenv("DB_NAME")
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")

    string_conexao = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={servidor};"
        f"DATABASE={banco};"
        f"UID={usuario};"
        f"PWD={senha};"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(string_conexao)


def carregar_serie(nome_tabela: str, df: pd.DataFrame, conexao: pyodbc.Connection) -> int:
    """
    Grava um DataFrame (colunas: data, valor) na tabela informada.
    Usa MERGE: se a data já existir, atualiza o valor; se não existir, insere.

    Args:
        nome_tabela: "selic", "ipca" ou "cambio"
        df: DataFrame já validado pelo transform.py
        conexao: conexão aberta com o banco

    Returns:
        Número de linhas afetadas (inseridas ou atualizadas)
    """
    if df.empty:
        return 0

    cursor = conexao.cursor()

    sql_merge = f"""
        MERGE {nome_tabela} AS destino
        USING (SELECT ? AS data, ? AS valor) AS origem
        ON destino.data = origem.data
        WHEN MATCHED THEN
            UPDATE SET valor = origem.valor
        WHEN NOT MATCHED THEN
            INSERT (data, valor) VALUES (origem.data, origem.valor);
    """

    linhas_afetadas = 0
    for _, linha in df.iterrows():
        cursor.execute(sql_merge, linha["data"], linha["valor"])
        linhas_afetadas += cursor.rowcount

    conexao.commit()
    cursor.close()

    return linhas_afetadas