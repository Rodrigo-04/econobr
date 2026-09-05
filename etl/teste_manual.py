#testar o funcionamento dos arquivos em conjunto
#mesma regra que existe para testar o arquivo de transform

if __name__ == "__main__":
    from datetime import date, timedelta
    from extract import buscar_serie, SERIES
    from transform import transformar_serie

    hoje = date.today()
    periodo_teste = hoje - timedelta(days=400)

    for nome in SERIES:
        dados_brutos = buscar_serie(nome, periodo_teste, hoje)
        df = transformar_serie(dados_brutos)
        print(f"\n--- {nome.upper()} ---")
        print(f"Linhas brutas: {len(dados_brutos)} | Linhas válidas após transformação: {len(df)}")
        print(df.head())
        print(df.dtypes)