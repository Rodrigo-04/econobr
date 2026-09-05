"""
extract.py

Responsável por buscar dados de séries temporais na API do Banco Central (SGS).
"""

import requests
from datetime import date, timedelta

# Códigos das séries no SGS (Sistema Gerenciador de Séries Temporais)
SERIES = {
    "selic": 432,   # SELIC (meta), definida pelo Copom
    "ipca": 433,    # IPCA, variação mensal (%)
    "cambio": 1,    # Câmbio USD/BRL, venda, fechamento diário
}

BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"


def buscar_serie(nome_serie: str, data_inicial: date, data_final: date) -> list[dict]:
    """
    Busca uma série temporal do Banco Central entre duas datas.

    Args:
        nome_serie: chave em SERIES (ex: "selic", "ipca", "cambio")
        data_inicial: primeira data do intervalo
        data_final: última data do intervalo

    Returns:
        Lista de dicionários no formato [{"data": "01/08/2026", "valor": "13.75"}, ...]
    """
    if nome_serie not in SERIES:
        raise ValueError(f"Série desconhecida: {nome_serie}. Use uma de {list(SERIES.keys())}")

    codigo = SERIES[nome_serie]
    url = BASE_URL.format(codigo=codigo)

    params = {
        "formato": "json",
        "dataInicial": data_inicial.strftime("%d/%m/%Y"),
        "dataFinal": data_final.strftime("%d/%m/%Y"),
    }

    resposta = requests.get(url, params=params, timeout=30)

    # A API do BCB responde 404 quando não há nenhum dado no período pedido
    # (comum em séries mensais/anuais consultadas numa janela curta). Isso
    # não é um erro real, é o jeito da API dizer "sem resultados aqui".
    if resposta.status_code == 404:
        return []

    resposta.raise_for_status()  # lança erro se o status não for 200 OK (outros casos)

    return resposta.json()


if __name__ == "__main__":
    # Teste manual: busca um período mais largo (400 dias) pra garantir que
    # séries mensais como o IPCA tenham pelo menos uma publicação na janela
    hoje = date.today()
    periodo_teste = hoje - timedelta(days=400)

    for nome in SERIES:
        dados = buscar_serie(nome, periodo_teste, hoje)
        print(f"\n--- {nome.upper()} ({len(dados)} registros) ---")
        for linha in dados[:5]:  # mostra só os 5 primeiros, pra não poluir o terminal
            print(linha)