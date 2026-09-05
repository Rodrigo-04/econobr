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
Desativar ambiente virtual:
```deactivate```

## Teste
Rode o arquivo de teste
```python extract.py```