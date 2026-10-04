# etl

[← voltar ao README principal](../README.md)

Scripts Python que extraem os indicadores econômicos (SELIC, IPCA, câmbio USD/BRL) da API do Banco Central (SGS) e carregam no SQL Server.

## Arquivos
 
| Arquivo | Responsabilidade |
|---|---|
| `extract.py` | Busca os dados brutos na API do BCB, com tentativas automáticas em caso de falha de rede temporária |
| `transform.py` | Converte os dados brutos (texto) para tipos corretos (data, decimal) e remove linhas inválidas/duplicadas |
| `load.py` | Grava os dados no banco (SQL Server ou Postgres, conforme `DB_ENGINE`), em modo upsert para nunca duplicar |
| `main.py` | Orquestra o pipeline completo: extração → transformação → carga, para os três indicadores |
| `teste_manual.py` | Script auxiliar para testar extração + transformação isoladamente, sem gravar no banco |

## Códigos das séries
| Indicador | Código SGS |
|---|---|
| SELIC (meta) | 432 |
| IPCA (variação mensal) | 433 |
| Câmbio USD/BRL (venda) | 1 |


## Ambiente
Vamos usar um ambiente virtual (venv) dentro da pasta ETL
```bash
cd etl
```
Criar o ambiente venv:
```bash
python -m venv venv
```
Iniciar venv:
```bash
.\venv\Scripts\Activate.ps1
```
Instalar requisitos:
```bash
pip install -r requirements.txt
```
>Obs: Sempre que atualizarmos os requisitos precisamos rodar essa instalação no ambiente virtual

Copie `.env.example` para `.env` e preencha as credenciais do banco (ver README principal para o significado de cada variável, incluindo `DB_ENGINE`).

Para rodar o processo completo de ETL:
```bash
python main.py
```

Desativar ambiente virtual:
```bash
deactivate
```

## Teste
Rode o teste pra a extração
```bash
python extract.py
```
Rode o teste pra a transformação
```bash
python transform.py
```
Rode o teste pra a ambos
```bash
python teste_manual.py
```

## Armazenar no banco de dados SQL Server (Local)
> Depende do valor no .env da DB_ENGINE
Precisamos garantir que Windows possui ODBC
```bash
Get-OdbcDriver | Where-Object {$_.Name -like '*SQL Server*'}
```
> Dependendo do retorno precisamos instalar o ODBC para SQL Server, estou utilizando verão 18

## Limitação conhecida
 
A API pública do Banco Central (`api.bcb.gov.br`) apresentou instabilidade de resolução DNS em outubro de 2026, afetando tanto execuções em nuvem (GitHub Actions) quanto localmente. O `extract.py` já tenta novamente automaticamente (3 tentativas, com espera entre elas) antes de desistir, mas se a instabilidade for prolongada, o ETL falha mesmo assim. Nesse caso, é um problema externo, fora do controle do projeto.