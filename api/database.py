"""
database.py
Gerencia a conexão da API com o SQL Server.
"""

import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


def obter_conexao() -> pyodbc.Connection:
    """
    Abre uma nova conexão com o SQL Server usando as credenciais do .env.
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


def obter_conexao_dependencia():
    """
    Dependência do FastAPI: abre uma conexão nova para cada requisição recebida pela API, e garante que ela seja fechada no final, mesmo que algo dê errado no meio do caminho.
    """
    conexao = obter_conexao()
    try:
        yield conexao
    finally:
        conexao.close()