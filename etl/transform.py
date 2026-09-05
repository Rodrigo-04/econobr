"""
transform.py

Responsável por converter e validar os dados brutos vindos da API do Banco Central,
deixando-os prontos para carga no banco de dados.
"""

from datetime import datetime
import pandas as pd

    #Converte a lista bruta da API (strings) num DataFrame com tipos corretos,
    #removendo linhas inválidas e duplicadas.

def transformar_serie(dados_brutos: list[dict]) -> pd.DataFrame:
    """
    Args:
        dados_brutos: lista no formato [{"data": "01/08/2025", "valor": "15.00"}, ...]

    Returns:
        DataFrame com colunas: data (datetime.date) e valor (float)
    """
    linhas_validas = []

    for linha in dados_brutos:
        data_texto = linha.get("data")
        valor_texto = linha.get("valor")

        # Pula a linha se faltar data ou valor
        if not data_texto or not valor_texto:
            continue

        # Se a conversão falhar (formato inesperado), pula a linha
        # em vez de derrubar o script inteiro
        try:
            data_convertida = datetime.strptime(data_texto, "%d/%m/%Y").date()
            valor_convertido = float(valor_texto)
        except (ValueError, TypeError):
            continue

        linhas_validas.append({"data": data_convertida, "valor": valor_convertido})

    df = pd.DataFrame(linhas_validas, columns=["data", "valor"])

    if df.empty:
        return df

    # Remove duplicatas de data (mantém a última ocorrência) e ordena cronologicamente
    df = df.drop_duplicates(subset="data", keep="last")
    df = df.sort_values("data").reset_index(drop=True)

    return df


    # Teste manual: encadeia extração + transformação
    #reativar para rodar o arquivo como teste no terminal
"""
if __name__ == "__main__":
    from datetime import date, timedelta
    from extract import buscar_serie, SERIES

    hoje = date.today()
    periodo_teste = hoje - timedelta(days=400)

    for nome in SERIES:
        dados_brutos = buscar_serie(nome, periodo_teste, hoje)
        df = transformar_serie(dados_brutos)
        print(f"\n--- {nome.upper()} ---")
        print(f"Linhas brutas: {len(dados_brutos)} | Linhas válidas após transformação: {len(df)}")
        print(df.head())
        print(df.dtypes)
"""