# econobr

Ecossistema de indicadores econômicos brasileiros (SELIC, IPCA, câmbio USD/BRL), construído como projeto de portfólio full stack: dados → API → consumo (web e mobile) → automação.
Uso de IApara acelerar o desenvolvimento.

## Arquitetura

```
API Banco Central / IBGE
        │
        ▼
ETL em Python (extrai → transforma → carrega)
        │
        ▼
SQL Server (em container Docker)
        │
        ▼
API em ASP.NET (expõe os indicadores tratados via REST + Swagger)
        │
        ├──────────────┐
        ▼              ▼
  Dashboard Web    App Mobile (React Native)
```

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| [`etl/`](./etl) | Scripts Python que extraem os indicadores da API do Banco Central e carregam no banco |
| [`api/`](./api) | Backend/API | Python (FastAPI), documentação Swagger/OpenAPI automática
| [`dashboard/`](./dashboard) | Dashboard web (HTML/CSS/JS + Chart.js) que consome a API |
| [`mobile/`](./mobile) | App React Native (Expo) que consome a mesma API |
| [`infra/`](./infra) | Docker Compose, Dockerfiles, scripts de infraestrutura |
| [`docs/`](./docs) | Diagramas, prints de tela, documentação complementar |

## Status do projeto

- [x] M0 — Setup
- [X] M1 — Banco de dados em Docker
- [X] M2 — ETL (Python)
- [X] M3 — API (Python/FastAPI)
- [ ] M4 — Dashboard Web
- [ ] M5 — App Mobile (React Native)
- [ ] M6 — DevOps / CI-CD
- [ ] M7 — Documentação e integração com o portfólio

## Como rodar

Pré-requisitos: Docker Desktop, Python 3.11+ (com venv em `etl/`), .NET SDK removido do
escopo — API será em Python/FastAPI (ver M3). Node 18+ será necessário a partir do M4.

### Iniciar o ambiente

1. Abra o **Docker Desktop** e espere o ícone da baleia ficar estável.
2. Suba o banco de dados:
```bash
   cd infra
   docker compose up -d
```
3. Confirme que subiu: `docker ps` deve mostrar `econobr-sqlserver` com status `Up`.

### Rodar o ETL (atualizar os dados no banco)

```bash
cd etl
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# ou: source venv/Scripts/activate    # Git Bash
python main.py
```

Isso busca os dados mais recentes de SELIC, IPCA e câmbio na API do Banco Central e
grava/atualiza no banco (é seguro rodar quantas vezes quiser — não duplica dados).


### Iniciar a API
```bash
cd api
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# ou: source venv/Scripts/activate    # Git Bash
python uvicorn main:app --reload 
```

### Iniciar o Dashboard
```bash
cd dashboard
python -m http.server 5500
```
E abre no navegador (o gráfico não será exibido em alguns navegadores)
```
http://localhost:5500/
```

### Encerrar o ambiente

```bash
deactivate          # sai do venv, se estiver ativo
cd infra
docker compose stop  # pausa o container (mantém os dados)
```

Use `docker compose down` em vez de `stop` se quiser remover o container por completo
(os dados continuam salvos no volume). Só use `docker compose down -v` se quiser apagar
os dados de verdade — isso **não é reversível**.
