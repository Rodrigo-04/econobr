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
- [ ] M3 — API (Python/FastAPI)
- [ ] M4 — Dashboard Web
- [ ] M5 — App Mobile (React Native)
- [ ] M6 — DevOps / CI-CD
- [ ] M7 — Documentação e integração com o portfólio

## Como rodar (preencher conforme os milestones avançam)

Pré-requisitos: Docker, .NET SDK, Python 3.11+, Node 18+.

```bash
# em breve: instruções de setup completo (M1 em diante)
```