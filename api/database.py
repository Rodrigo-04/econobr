"""
database.py

Gerencia a conexão da API com o banco (SQL Server local OU Postgres/Supabase,
dependendo de DB_ENGINE).
"""

import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_ENGINE = os.getenv("DB_ENGINE", "sqlserver")


def obter_conexao():
    """
    Abre uma nova conexão com o banco configurado no .env.
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

    import pyodbc
    
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


def obter_conexao_dependencia():
    """
    Dependência do FastAPI: abre uma conexão nova para cada requisição
    recebida pela API, e garante que ela seja fechada no final.
    """
    conexao = obter_conexao()
    try:
        yield conexao
    finally:
        conexao.close()