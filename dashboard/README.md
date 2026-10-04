# dashboard

[← voltar ao README principal](../README.md)
 
Dashboard web que consome a API do econobr e exibe os indicadores em cartões de resumo e gráficos de série temporal. HTML/CSS/JS puro, publicado no Vercel.

>Dashboard ao vivo: `https://econobr-dashboard.vercel.app`

## Identidade visual
 
Tema "terminal financeiro": fundo azul, cada indicador com uma cor fixa (SELIC em amrelo, IPCA em verde, câmbio em vermelho).
 
## Arquivos
 
| Arquivo | Responsabilidade |
|---|---|
| `index.html` | Estrutura da página |
| `style.css` | Estilo visual |
| `script.js` | Busca os dados na API e desenha os cartões e gráficos (Chart.js) |

## Rodar
No terminal:
```bash
cd dashboard
python -m http.server 5500
```

Abra `http://localhost:5500`. A URL da API consumida está fixada no topo de `script.js`
(constante `URL_API`) — ajuste para `http://localhost:8000` se quiser testar contra uma API
rodando localmente, em vez da publicada no Render.
 
**Observação**: o Microsoft Edge pode bloquear o carregamento do Chart.js por causa do recurso "Tracking Prevention".
 
## Deploy
 
Publicado no [Vercel](https://vercel.com) como site estático, direto a partir desta pasta.