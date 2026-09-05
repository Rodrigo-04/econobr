# infra

Infraestrutura do projeto: Docker Compose, Dockerfiles e scripts.

Status: **M1 (banco) e M6 (CI/CD) — a implementar.**

## Iniciando o container
**Rode no terminal da pasta /infra:**
Criar container e conectar volume:
```docker compose up -d```
Para confirmar se está rodando, no memso terminal utilize: 
```docker ps```
Pausa o container: 
```docker compose stop```
Retoma o container: 
```docker compose start```
Parar o container, sem apagar o volume: 
```docker compose down```
Para o container e pagar volume: 
```docker compose down -v```

Envia as informações do schema.sql para o banco de dados:
```Get-Content schema.sql | docker exec -i econobr-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P ".env:SA_PASSWORD" -C -i /dev/stdin```
Listar todas as tabelas que existem dentro do banco de dados:
```docker exec -it econobr-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P ".env:SA_PASSWORD" -C -Q "USE econobr; SELECT name FROM sys.tables ORDER BY name;"```
Para listar o contúdo utilizamos:
```docker exec -it econobr-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P ".env:SA_PASSWORD" -C -Q "USE econobr; SELECT TOP 5 * FROM selic ORDER BY data DESC;"```
Para listar a contagem das linhas de uma tabela:
```docker exec -it econobr-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P ".env:SA_PASSWORD" -C -Q "USE econobr; SELECT COUNT(*) AS total FROM cambio;"```

## Planejado
- `docker-compose.yml` — SQL Server (M1), depois unificado com a API (M6)
- `schema.sql` — schema inicial: tabelas de SELIC, IPCA, câmbio
- `Dockerfile` (api) — imagem da Web API
- `.github/workflows/` (na raiz do repo) — pipeline de build, testes e deploy
