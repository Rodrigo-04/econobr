"""
main.py
API que expõe os indicadores econômicos (SELIC, IPCA, câmbio) via REST.
"""

from fastapi import FastAPI, Depends
import pyodbc

from database import obter_conexao_dependencia

app = FastAPI(
    title="econobr API",
    description="Indicadores econômicos brasileiros: SELIC, IPCA e câmbio USD/BRL.",
    version="1.0.0",
)

def buscar_indicador(nome_tabela: str, conexao: pyodbc.Connection) -> list[dict]:
    """
    Função auxiliar reaproveitada pelos três endpoints: busca todo o histórico de uma tabela, do mais recente para o mais antigo.
    """
    cursor = conexao.cursor()
    cursor.execute(f"SELECT data, valor FROM {nome_tabela} ORDER BY data DESC")
    linhas = cursor.fetchall()
    cursor.close()

    return [{"data": linha.data, "valor": float(linha.valor)} for linha in linhas]
    '''
    comprcompreensão de lista de:
    resultado = []
    for linha in linhas:
        resultado.append({"data": linha.data, "valor": float(linha.valor)})
    return resultado
    '''
def buscar_ultimo_valor(nome_tabela: str, conexao: pyodbc.Connection) -> dict | None:
    """
    Busca apenas o registro mais recente de uma tabela.
    """
    cursor = conexao.cursor()
    cursor.execute(f"SELECT TOP 1 data, valor FROM {nome_tabela} ORDER BY data DESC")
    linha = cursor.fetchone()
    cursor.close()
 
    if linha is None:
        return None
 
    return {"data": linha.data, "valor": float(linha.valor)}

@app.get("/selic")
def listar_selic(conexao: pyodbc.Connection = Depends(obter_conexao_dependencia)):
    """Retorna o histórico completo da SELIC."""
    return buscar_indicador("selic", conexao)

@app.get("/selic/ultimo")
def ultimo_selic(conexao: pyodbc.Connection = Depends(obter_conexao_dependencia)):
    """Retorna apenas o valor mais recente da SELIC."""
    resultado = buscar_ultimo_valor("selic", conexao)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhum dado de SELIC encontrado")
    return resultado

@app.get("/ipca")
def listar_ipca(conexao: pyodbc.Connection = Depends(obter_conexao_dependencia)):
    """Retorna o histórico completo do IPCA (variação mensal)."""
    return buscar_indicador("ipca", conexao)

@app.get("/ipca/ultimo")
def ultimo_ipca(conexao: pyodbc.Connection = Depends(obter_conexao_dependencia)):
    """Retorna apenas o valor mais recente do IPCA."""
    resultado = buscar_ultimo_valor("ipca", conexao)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhum dado de IPCA encontrado")
    return resultado

@app.get("/cambio")
def listar_cambio(conexao: pyodbc.Connection = Depends(obter_conexao_dependencia)):
    """Retorna o histórico completo do câmbio USD/BRL."""
    return buscar_indicador("cambio", conexao)

@app.get("/cambio/ultimo")
def ultimo_cambio(conexao: pyodbc.Connection = Depends(obter_conexao_dependencia)):
    """Retorna apenas o valor mais recente do câmbio USD/BRL."""
    resultado = buscar_ultimo_valor("cambio", conexao)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Nenhum dado de câmbio encontrado")
    return resultado