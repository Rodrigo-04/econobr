# api

Backend/API | Python (FastAPI), documentação Swagger/OpenAPI automática

Status: **M3 — a implementar.**

## Endpoints planejados
- `GET /selic` — histórico e último valor da SELIC
- `GET /ipca` — histórico e último valor do IPCA
- `GET /cambio` — histórico e último valor do câmbio USD/BRL

## Planejado
- Projeto Python/FastAPI
- Conexão com o SQL Server (do `infra/`)
- Swagger/OpenAPI habilitado

## Ambiente
Vamos usar um ambiente virtual (venv) dentro da pasta api (navegue até ela pelo terminal)
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
Com o venv ativo rode:
```uvicorn main:app --reload```
O --reload faz o servidor reiniciar, importante quando estamos desenvolvendo o código
Para encerrar o Uvicorn (programa que coloca a API no ar) basta usar Ctrl + C

Podemos acessar o documento SWAGGER da API com:
```http://localhost:8000/docs```
Podemos acessar o retorno da SELIC na API com:
```http://localhost:8000/selic```
Podemos acessar o retorno do IPCA na API com:
```http://localhost:8000/ipca```
Podemos acessar o retorno do CÂMBIO na API com:
```http://localhost:8000/cambio```
Para acessar somente o último dado coletado, temos:
Para a SELIC:
```http://localhost:8000/selic/ultimo```
Para o IPCA:
```http://localhost:8000/ipca/ultimo```
Para o CÂMBIO:
```http://localhost:8000/cambio/ultimo```