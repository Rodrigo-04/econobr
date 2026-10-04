# docs

[← voltar ao README principal](../README.md)
 
Diagramas e capturas de tela do projeto, para referência e documentação visual.
 
## Arquitetura
 
![Diagrama de arquitetura](./architecture.svg)
 
Fluxo de produção: API do Banco Central → ETL (Python) → Postgres (Supabase) → API REST (FastAPI, no Render) → Dashboard Web (Vercel) e App Mobile (Expo), em paralelo.
O ambiente local de desenvolvimento segue a mesma lógica, trocando Supabase por SQL Server em container Docker, ver o README principal para os dois fluxos completos.
 
## Capturas de tela
 
Todas em [`screenshots/`](./screenshots).
 
### Dashboard web
 
| Resumo + gráficos | SELIC | IPCA | Câmbio |
|---|---|---|---|
| ![Dashboard completo](./screenshots/Dashboard.png) | ![Gráfico da SELIC](./screenshots/Dashboard_SELIC.png) | ![Gráfico do IPCA](./screenshots/Dashboard_IPCA.png) | ![Gráfico do câmbio](./screenshots/Dashboard_CAMBIO.png) |
 
### App mobile
 
| Splash | Lista (Home) | SELIC | IPCA | Câmbio |
|---|---|---|---|---|
| ![Tela de splash](./screenshots/Mobile_SplashScreen.jpeg) | ![Lista de indicadores](./screenshots/Mobile_Home.jpeg) | ![Detalhe da SELIC](./screenshots/Mobile_SELIC.jpeg) | ![Detalhe do IPCA](./screenshots/Mobile_IPCA.jpeg) | ![Detalhe do câmbio](./screenshots/Mobile_CAMBIO.jpeg) |
 
### API
 
![Documentação Swagger da API](./screenshots/API_SWAGGER.png)
