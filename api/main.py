"""
main.py

API que expõe os indicadores econômicos (SELIC, IPCA, câmbio) via REST.
"""

import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import obter_conexao_dependencia

load_dotenv()

DB_ENGINE = os.getenv("DB_ENGINE", "sqlserver")

app = FastAPI(
    title="econobr API",
    description="Indicadores econômicos brasileiros: SELIC, IPCA e câmbio USD/BRL.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/healthz")
def health_check():
    """
    Endpoint simples para o Render (ou qualquer monitor) checar se o
    processo está no ar — não consulta o banco de propósito, para não
    reportar "fora do ar" só porque o banco está lento, por exemplo.
    """
    return {"status": "ok"}

def buscar_indicador(nome_tabela: str, conexao) -> list[dict]:
    """
    Busca todo o histórico de uma tabela, do mais recente para o mais antigo.
    """
    cursor = conexao.cursor()
    cursor.execute(f"SELECT data, valor FROM {nome_tabela} ORDER BY data DESC")
    linhas = cursor.fetchall()
    cursor.close()

    return [{"data": linha[0], "valor": float(linha[1])} for linha in linhas]


def buscar_ultimo_valor(nome_tabela: str, conexao) -> dict | None:
    """
    Busca apenas o registro mais recente de uma tabela.
    """
    cursor = conexao.cursor()
  
    if DB_ENGINE == "postgres":
        cursor.execute(f"SELECT data, valor FROM {nome_tabela} ORDER BY data DESC LIMIT 1")
    else:
        cursor.execute(f"SELECT TOP 1 data, valor FROM {nome_tabela} ORDER BY data DESC")

    linha = cursor.fetchone()
    cursor.close()

    if linha is None:
        return None

    return {"data": linha[0], "valor": float(linha[1])}


@app.get("/selic")
def listar_selic(conexao=Depends(obter_conexao_dependencia)):
    """Retorna o histórico completo da SELIC."""
    return buscar_indicador("selic", conexao)


@app.get("/selic/ultimo")
def ultimo_selic(conexao=Depends(obter_conexao_dependencia)):
    """Retorna apenas o valor mais recente da SELIC."""
    resultado = buscar_ultimo_valor("selic", conexao)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhum dado de SELIC encontrado")
    return resultado


@app.get("/ipca")
def listar_ipca(conexao=Depends(obter_conexao_dependencia)):
    """Retorna o histórico completo do IPCA (variação mensal)."""
    return buscar_indicador("ipca", conexao)


@app.get("/ipca/ultimo")
def ultimo_ipca(conexao=Depends(obter_conexao_dependencia)):
    """Retorna apenas o valor mais recente do IPCA."""
    resultado = buscar_ultimo_valor("ipca", conexao)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhum dado de IPCA encontrado")
    return resultado


@app.get("/cambio")
def listar_cambio(conexao=Depends(obter_conexao_dependencia)):
    """Retorna o histórico completo do câmbio USD/BRL."""
    return buscar_indicador("cambio", conexao)


@app.get("/cambio/ultimo")
def ultimo_cambio(conexao=Depends(obter_conexao_dependencia)):
    """Retorna apenas o valor mais recente do câmbio USD/BRL."""
    resultado = buscar_ultimo_valor("cambio", conexao)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhum dado de câmbio encontrado")
    return resultado