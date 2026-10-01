"""
load.py

Responsável por conectar no SQL Server e gravar os dados já transformados,
evitando duplicatas (insere se a data não existir, atualiza se já existir).
SQL Server local OU Postgres/Supabase, dependendo de DB_ENGINE
"""

import os
import pyodbc
import psycopg
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env e disponibiliza as variáveis via os.getenv()

DB_ENGINE = os.getenv("DB_ENGINE", "sqlserver")  # "sqlserver" (padrão local) ou "postgres"

def obter_conexao():
    """
    Abre uma conexão com o banco configurado no .env.
    """
    if DB_ENGINE == "postgres":
        return psycopg.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT", "5432"),
            dbname=os.getenv("PG_DB", "postgres"),
            user=os.getenv("PG_USER", "postgres"),
            password=os.getenv("PG_PASSWORD"),
            sslmode="require",
        )
 
    # Padrão: SQL Server local
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


def carregar_serie(nome_tabela: str, df: pd.DataFrame, conexao) -> int:
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
    linhas_afetadas = 0
 
    if DB_ENGINE == "postgres":
        sql_upsert = f"""
            INSERT INTO {nome_tabela} (data, valor) VALUES (%s, %s)
            ON CONFLICT (data) DO UPDATE SET valor = EXCLUDED.valor;
        """
        for _, linha in df.iterrows():
            cursor.execute(sql_upsert, (linha["data"], linha["valor"]))
            linhas_afetadas += cursor.rowcount
    else:
        sql_merge = f"""
            MERGE {nome_tabela} AS destino
            USING (SELECT ? AS data, ? AS valor) AS origem
            ON destino.data = origem.data
            WHEN MATCHED THEN
                UPDATE SET valor = origem.valor
            WHEN NOT MATCHED THEN
                INSERT (data, valor) VALUES (origem.data, origem.valor);
        """
        for _, linha in df.iterrows():
            cursor.execute(sql_merge, linha["data"], linha["valor"])
            linhas_afetadas += cursor.rowcount
 
    conexao.commit()
    cursor.close()
 
    return linhas_afetadas