const URL_API = "http://localhost:8000";

const CORES = {
  selic: "#C9A227",
  ipca: "#3F8F6F",
  cambio: "#C1554B",
};

/**
 * Formata um número decimal como percentual brasileiro (ex: 14.0 -> "14,00%")
 */
function formatarPercentual(valor) {
  return valor.toLocaleString("pt-BR", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + "%";
}

/**
 * Formata um número decimal como moeda brasileira (ex: 5.42 -> "R$ 5,42")
 */
function formatarMoeda(valor) {
  return valor.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

/**
 * Formata uma data ISO (ex: "2026-09-04") como data brasileira (ex: "04/09/2026")
 */
function formatarData(dataIso) {
  const [ano, mes, dia] = dataIso.split("-");
  return `${dia}/${mes}/${ano}`;
}

/**
 * Busca o último valor de um indicador na API e escreve no elemento HTML correspondente.
 */
async function carregarUltimoValor(nomeIndicador, idElemento, formatador) {
  const elemento = document.getElementById(idElemento);

  try {
    const resposta = await fetch(`${URL_API}/${nomeIndicador}/ultimo`);

    if (!resposta.ok) {
      throw new Error(`API respondeu com status ${resposta.status}`);
    }

    const dados = await resposta.json();
    elemento.textContent = formatador(dados.valor);
    return dados.data; // devolve a data para usarmos no cabeçalho
  } catch (erro) {
    console.error(`Erro ao buscar ${nomeIndicador}:`, erro);
    elemento.textContent = "Erro ao carregar";
    return null;
  }
}

/**
 * Função: Busca o histórico completo de um indicador e desenha um gráfico de linha.
 */
async function carregarGrafico(nomeIndicador, idCanvas, formatador) {
  try {
    const resposta = await fetch(`${URL_API}/${nomeIndicador}`);
 
    if (!resposta.ok) {
      throw new Error(`API respondeu com status ${resposta.status}`);
    }
 
    const dados = await resposta.json();
    const dadosOrdenados = [...dados].reverse();
 
    const rotulos = dadosOrdenados.map((d) => formatarData(d.data));
    const valores = dadosOrdenados.map((d) => d.valor);
    const cor = CORES[nomeIndicador];
 
    const ctx = document.getElementById(idCanvas);
 
    new Chart(ctx, {
      type: "line",
      data: {
        labels: rotulos,
        datasets: [
          {
            data: valores,
            borderColor: cor,
            backgroundColor: cor + "22",
            borderWidth: 2,
            pointRadius: 0,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: cor,
            pointHoverBorderColor: "#0F1B2D",
            pointHoverBorderWidth: 2,
            tension: 0.2,
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: "index",
          intersect: false,
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: "#16273D",
            borderColor: cor,
            borderWidth: 1,
            titleColor: "#EDEAE3",
            bodyColor: "#EDEAE3",
            padding: 10,
            displayColors: false,
            callbacks: {
              label: (contexto) => formatador(contexto.parsed.y),
            },
          },
        },
        scales: {
          x: {
            ticks: { color: "#9FB0C3", maxTicksLimit: 8, maxRotation: 0 },
            grid: { color: "#24395640" },
          },
          y: {
            ticks: { color: "#9FB0C3" },
            grid: { color: "#24395640" },
          },
        },
      },
    });
  } catch (erro) {
    console.error(`Erro ao carregar gráfico de ${nomeIndicador}:`, erro);
  }
}

/**
 * Função principal: dispara a busca dos três indicadores e atualiza o cabeçalho.
 */
async function iniciarDashboard() {
  const [dataSelic] = await Promise.all([
    carregarUltimoValor("selic", "valor-selic", formatarPercentual),
    carregarUltimoValor("ipca", "valor-ipca", formatarPercentual),
    carregarUltimoValor("cambio", "valor-cambio", formatarMoeda),
    carregarGrafico("selic", "grafico-selic", formatarPercentual),
    carregarGrafico("ipca", "grafico-ipca", formatarPercentual),
    carregarGrafico("cambio", "grafico-cambio", formatarMoeda),
  ]);

  const textoAtualizado = document.getElementById("texto-atualizado");
  if (dataSelic) {
    textoAtualizado.textContent = `Atualizado em ${formatarData(dataSelic)}`;
  } else {
    textoAtualizado.textContent = "Não foi possível carregar os dados";
  }
}

iniciarDashboard();