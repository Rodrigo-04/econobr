# infra

[← voltar ao README principal](../README.md)
 
Infraestrutura do projeto: orquestração dos containers locais (banco + API) e os schemas SQL usados para criar as tabelas, nos dois motores de banco suportados.

## Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `docker-compose.yml` | Sobe o SQL Server e a API juntos, localmente, com um único comando |
| `schema.sql` | Cria as tabelas `selic`, `ipca`, `cambio` — sintaxe SQL Server (uso local) |
| `schema_postgres.sql` | Mesmo schema, em sintaxe PostgreSQL — rodado manualmente no SQL Editor do Supabase (produção) |

## Como as tabelas são estruturadas
 
Três tabelas, mesma forma: `id` (chave primária autoincremento), `data` (única por tabela, um registro por dia), `valor` (decimal), `criado_em` (timestamp de quando a linha foi gravada, para auditoria). A restrição de unicidade em `data` é o que torna o processo de carga do ETL seguro para rodar repetidamente, sem duplicar registros (upsert).

## Ambiente
**Rode no terminal da pasta /infra:**
Criar container e conectar volume:
```bash
docker compose up -d
```
Para confirmar se está rodando, no memso terminal utilize: 
```bash
docker ps
```
Pausa o container: 
```bash
docker compose stop
```
Retoma o container: 
```bash
docker compose start
```
Parar o container, sem apagar o volume: 
```bash
docker compose down
```
Para o container e pagar volume: 
```bash
docker compose down -v
```

Envia as informações do schema.sql para o banco de dados:
```bash
Get-Content schema.sql | docker exec -i econobr-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P ".env:SA_PASSWORD" -C -i /dev/stdin
```
Listar todas as tabelas que existem dentro do banco de dados:
```bash
docker exec -it econobr-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P ".env:SA_PASSWORD" -C -Q "USE econobr; SELECT name FROM sys.tables ORDER BY name;"
```
Para listar o contúdo utilizamos:
```bash
docker exec -it econobr-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P ".env:SA_PASSWORD" -C -Q "USE econobr; SELECT TOP 5 * FROM selic ORDER BY data DESC;"
```
Para listar a contagem das linhas de uma tabela:
```bash
docker exec -it econobr-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P ".env:SA_PASSWORD" -C -Q "USE econobr; SELECT COUNT(*) AS total FROM cambio;"
```

## Dockerfile
Agora reconstruimos a imagem a partir do Dockerfile
```bash
docker compose up -d --build
```
E quando utilizamos a imagem, já vamos ter o econobr-api e o econobr-sqlserver rodando.
Para parar continuamos usando:
```bash
docker compose down
```

## Como rodar localmente
 
```bash
cd infra
docker compose up -d
```
 
Isso builda a imagem da API a partir do `Dockerfile` em `../api/` e sobe os dois containers (`econobr-sqlserver` e `econobr-api`) na mesma rede interna do Docker Compose, onde a API encontra o banco pelo nome do serviço (`sqlserver`), sem precisar de IP ou `localhost`.
 
Um `healthcheck` no serviço do banco garante que a API só inicia depois que o SQL Server estiver de fato pronto para aceitar conexões, não só "existindo" como container.

## Variáveis de ambiente
 
Ver `.env.example` nesta pasta. O `docker-compose.yml` lê o `.env` automaticamente (sem necessidade de nenhuma biblioteca extra, diferente do Python), só precisa estar na mesma pasta do `docker-compose.yml` ao rodar o comando.