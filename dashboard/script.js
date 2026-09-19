const URL_API = "http://localhost:8000";

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
 * Função principal: dispara a busca dos três indicadores e atualiza o cabeçalho.
 */
async function iniciarDashboard() {
  const [dataSelic] = await Promise.all([
    carregarUltimoValor("selic", "valor-selic", formatarPercentual),
    carregarUltimoValor("ipca", "valor-ipca", formatarPercentual),
    carregarUltimoValor("cambio", "valor-cambio", formatarMoeda),
  ]);

  const textoAtualizado = document.getElementById("texto-atualizado");
  if (dataSelic) {
    textoAtualizado.textContent = `Atualizado em ${formatarData(dataSelic)}`;
  } else {
    textoAtualizado.textContent = "Não foi possível carregar os dados";
  }
}

iniciarDashboard();