# econobr
Ecossistema de indicadores econômicos brasileiros (SELIC, IPCA, câmbio USD/BRL), construído como projeto de portfólio full stack: dados → API → consumo (web e mobile) → automação.

> Projeto desenvolvido com apoio de IA para acelerar o desenvolvimento e auxiliar na documentação

## Acesso ao vivo
 
- **Dashboard**: https://econobr-dashboard.vercel.app
- **API (Swagger/OpenAPI)**: https://econobr.onrender.com/docs

## Arquitetura
 
### Hospedada (produção)
 
```
API Banco Central
        │
        ▼
ETL em Python (extrai → transforma → carrega)
        │
        ▼
Postgres (Supabase)
        │
        ▼
API em Python/FastAPI (Render)
        │
        ▼
  Dashboard Web (Vercel)
```
 
### Local (desenvolvimento)
 
```
API Banco Central
        │
        ▼
ETL em Python (extrai → transforma → carrega)
        │
        ▼
SQL Server (container Docker)
        │
        ▼
API em Python/FastAPI (container Docker)
        │
        ├──────────────┐
        ▼              ▼
  Dashboard Web    App Mobile (React Native/Expo)
```

> O projeto roda contra os dois bancos (SQL Server local ou Postgres/Supabase) através de uma variável de ambiente (`DB_ENGINE`) — ver seção "Decisões técnicas" abaixo.

## Estrutura do repositório

| Pasta | Conteúdo |
|---|---|
| [`etl/`](./etl) | Scripts Python que extraem os indicadores da API do Banco Central, transformam e carregam no banco |
| [`api/`](./api) | API em Python (FastAPI) que expõe os indicadores via REST, com documentação Swagger/OpenAPI automática |
| [`dashboard/`](./dashboard) | Dashboard web (HTML/CSS/JS + Chart.js) que consome a API |
| [`mobile/`](./mobile) | App React Native (Expo) que consome a mesma API |
| [`infra/`](./infra) | Docker Compose, Dockerfiles, schemas SQL |
| [`docs/`](./docs) | Diagramas, prints de tela, documentação complementar |
| [`.github/workflows/`](./.github/workflows) | Automação (GitHub Actions) |

## Status do projeto

- [x] M0 — Setup
- [X] M1 — Banco de dados em Docker
- [X] M2 — ETL (Python)
- [X] M3 — API (Python/FastAPI)
- [X] M4 — Dashboard Web
- [X] M5 — App Mobile (React Native)
- [X] M6 — DevOps / CI-CD
- [X] M7   — Documentação e integração com o portfólio

## Decisões técnicas relevantes
 
- **Backend em Python/FastAPI** — decisão tomada para manter uma única linguagem entre ETL e API, reduzindo troca de contexto, e porque o FastAPI gera documentação Swagger automaticamente.
- **Dois motores de banco suportados** — SQL Server para desenvolvimento local (container
  Docker, sem depender de conta externa) e Postgres (Supabase) para produção. A troca é feita por uma única variável de ambiente (`DB_ENGINE=sqlserver` ou `DB_ENGINE=postgres`), sem duplicar código de aplicação — só a camada de acesso a dados (`database.py`/`load.py`) sabe a diferença.
- **ETL agendado via GitHub Actions está desativado no momento** — a API pública do Banco
  Central (`api.bcb.gov.br`) apresentou instabilidade de DNS, tanto a partir de execuções na
  nuvem (GitHub Actions) quanto localmente, impedindo atualizações automáticas confiáveis. Os dados já coletados continuam servidos normalmente; atualizações seguem sendo feitas rodando `python main.py` manualmente até a situação se normalizar. O workflow permanece no
  repositório, pronto para ser reativado (`.github/workflows/etl-agendado.yml`).

## Como rodar localmente

Pré-requisitos: Docker Desktop, Python 3.12+, Node 18+ com Expo Go instalado no celular (para o app mobile).

### Configurar as variáveis de ambiente
 
Cada pasta (`infra/`, `etl/`, `api/`, `mobile/`) tem um arquivo `.env.example` — copie para
`.env` na mesma pasta e preencha com valores reais (senhas, credenciais de banco, etc.):
 
```bash
cp infra/.env.example infra/.env
cp etl/.env.example etl/.env
cp api/.env.example api/.env
cp mobile/.env.example mobile/.env
```
 
Por padrão (`DB_ENGINE=sqlserver`), tudo roda contra o banco local em Docker, sem precisar de nenhuma conta externa.

### Iniciar o banco + API (Docker)

1. Abra o **Docker Desktop** e espere o ícone da baleia ficar estável.
2. Suba o banco de dados:
```bash
   cd infra
   docker compose up -d
```
3. Confirme que subiu: `docker ps` devem aparecer **dois** containers: `econobr-sqlserver` e
`econobr-api`, ambos com status `Up`.

### Rodar o ETL (popular/atualizar os dados no banco de dados)

```bash
cd etl
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# ou: source venv/Scripts/activate    # Git Bash
pip install -r requirements.txt   # necessário somente na primeira vez
python main.py
```

Busca os dados mais recentes de SELIC, IPCA e câmbio na API do Banco Central e
grava/atualiza no banco (é seguro rodar quantas vezes quiser pois não duplica dados).


### Rodar a API localmente, fora do Docker (opcional)

```bash
cd api
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt   # necessário somente na primeira vez
uvicorn main:app --reload
```

### Iniciar o Dashboard

```bash
cd dashboard
python -m http.server 5500
```
Abra `http://localhost:5500` no navegador. **Observação**: alguns navegadores podem bloquear a biblioteca de gráficos (Chart.js) por causa do recurso de "Tracking Prevention".

### Rodar o App Mobile

```bash
cd mobile
npx expo start
```

Escaneie o QR code com o app **Expo Go** no celular. O celular precisa estar na mesma rede
Wi-Fi que o computador (para apontar para a API local) — ou configure `EXPO_PUBLIC_API_URL`
no `mobile/.env` para apontar direto para a API publicada no Render.

### Encerrar o ambiente

```bash
deactivate          # sai do venv, se estiver ativo
cd infra
docker compose stop  # pausa o container (mantém os dados)
```

Use `docker compose down` em vez de `stop` se quiser remover o container por completo
(os dados continuam salvos no volume). Só use `docker compose down -v` se quiser apagar
os dados de verdade (**não é reversível**).

