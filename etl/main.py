"""
main.py

Ponto de entrada do ETL: extrai, transforma e carrega os três indicadores
econômicos (SELIC, IPCA, câmbio) no banco de dados.
"""

from datetime import date, timedelta
from extract import buscar_serie, SERIES
from transform import transformar_serie
from load import obter_conexao, carregar_serie


def executar_etl(dias_historico: int = 400) -> None:
    """
    Executa o pipeline completo para todas as séries configuradas.

    Args:
        dias_historico: quantos dias para trás buscar. 400 cobre bem uma
            carga inicial; em execuções diárias futuras, um valor pequeno
            (ex: 10) já seria suficiente para pegar o dado mais recente.
    """
    hoje = date.today()
    data_inicial = hoje - timedelta(days=dias_historico)

    conexao = obter_conexao()

    try:
        for nome_serie in SERIES:
            print(f"\n--- Processando {nome_serie.upper()} ---")

            dados_brutos = buscar_serie(nome_serie, data_inicial, hoje)
            print(f"Extraídos: {len(dados_brutos)} registros")

            df = transformar_serie(dados_brutos)
            print(f"Válidos após transformação: {len(df)} registros")

            linhas_afetadas = carregar_serie(nome_serie, df, conexao)
            print(f"Gravados/atualizados no banco: {linhas_afetadas} registros")
    finally:
        conexao.close()


if __name__ == "__main__":
    executar_etl()