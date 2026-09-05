# etl

Scripts Python que extraem os indicadores econômicos (SELIC, IPCA, câmbio USD/BRL) da API
do Banco Central (SGS) e carregam no SQL Server.

Status: **M2 — a implementar.**

## Planejado
- `extract.py` — consome `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados`
- `transform.py` — valida datas, tipos e valores nulos
- `load.py` — grava no SQL Server (schema definido no M1)
- `requirements.txt` — `requests`, `pandas`, driver de conexão SQL Server (ex. `pyodbc`)

## Códigos das séries (a confirmar antes de codar)
| Indicador | Código SGS |
|---|---|
| SELIC (meta) | 432 |
| IPCA (variação mensal) | 433 |
| Câmbio USD/BRL (venda) | 1 |


## Ambiente
Vamos usar um ambiente virtual (venv)
Criar pasta venv:
```python -m venv venv```
Iniciar venv:
```.\venv\Scripts\Activate.ps1```
Instalar requisitos:
```pip install -r requirements.txt```
    Obs: Sempre que atualizarmos os requisitos precisamos rodar essa instalação no ambiente virtual
Desativar ambiente virtual:
```deactivate```

## Teste
Rode o teste pra a extração
```python extract.py```
Rode o teste pra a transformação
```python transform.py```
Rode o teste pra a ambos
```python teste_manual.py```

## Armazenar no banco de dados SQL Server
Previsamos garantir que windows possui ODBC
```Get-OdbcDriver | Where-Object {$_.Name -like '*SQL Server*'}```
Depedndo do retorno eciamos instala o ODBC para SQL Server, estou utilizando verão 18

Quando finaziamos a criação do load.py e do main.py
    load: abre conexão com o SQL Server
    main: faz o ETL de fato executando os arquivos extract, transform e load
Precisamos ativar o container Docker, como temos anotado no README da pasta infra, assim o banco de dados fica ativo.
E então rodamos:
```python main.py```
Para executar o processo de ETL