# api

[← voltar ao README principal](../README.md)

API em FastAPI que expõe os indicadores econômicos tratados via REST, com documentação Swagger/OpenAPI gerada automaticamente (Publicada no Render).

## Endpoints
 
| Rota | Descrição |
|---|---|
| `GET /healthz` | Verificação de disponibilidade (não consulta o banco) |
| `GET /selic` | Histórico completo da SELIC |
| `GET /selic/ultimo` | Valor mais recente da SELIC |
| `GET /ipca` | Histórico completo do IPCA |
| `GET /ipca/ultimo` | Valor mais recente do IPCA |
| `GET /cambio` | Histórico completo do câmbio USD/BRL |
| `GET /cambio/ultimo` | Valor mais recente do câmbio USD/BRL |

>Documentação interativa (Swagger) disponível em `https://econobr.onrender.com/docs`
 
## Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Define as rotas e a lógica de cada endpoint |
| `database.py` | Gerencia a conexão com o banco (SQL Server ou Postgres, conforme `DB_ENGINE`) |
| `Dockerfile` | Empacota a API para rodar em container (usado também no deploy no Render) |

## Ambiente
Vamos usar um ambiente virtual (venv) dentro da pasta api
```bash
cd api
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
> Obs: Sempre que atualizarmos os requisitos precisamos rodar essa instalação no ambiente virtual

Copie `.env.example` para `.env` e preencha as credenciais do banco.

Inicia a API
```bash
uvicorn main:app --reload
```

Desativar ambiente virtual:
Ctrl + C
```bash
deactivate
```

## Teste
Com o venv ativo rode:
```bash
uvicorn main:app --reload
```
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

Criação do Dockerfile
E geração da imagem, nomeada como econobr-api
```bash
cd api
docker build -t econobr-api .
```
Para verificar se a imagem foi gerada usamos:
```bash
docker images
```

## Deploy
 
Publicada no [Render](https://render.com) a partir do `Dockerfile` desta pasta, com build e deploy automáticos a cada push na branch `main`.
Variáveis de ambiente configuradas diretamente no painel do Render (nunca commitadas no repositório).