# infra

Infraestrutura do projeto: Docker Compose, Dockerfiles e scripts.

Status: **M1 (banco) e M6 (CI/CD) — a implementar.**

## Planejado
- `docker-compose.yml` — SQL Server (M1), depois unificado com a API (M6)
- `schema.sql` — schema inicial: tabelas de SELIC, IPCA, câmbio
- `Dockerfile` (api) — imagem da Web API
- `.github/workflows/` (na raiz do repo) — pipeline de build, testes e deploy
