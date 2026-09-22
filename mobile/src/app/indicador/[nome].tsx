import { useEffect, useState } from 'react';
import { ActivityIndicator, Dimensions, ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Stack, useLocalSearchParams } from 'expo-router';
import { LineChart } from 'react-native-chart-kit';

import { API_URL } from '@/constants/api';
import { Paleta } from '@/constants/paleta';

type NomeIndicador = 'selic' | 'ipca' | 'cambio';

const INFO_INDICADOR: Record<NomeIndicador, { titulo: string; cor: string }> = {
  selic: { titulo: 'SELIC', cor: Paleta.selic },
  ipca: { titulo: 'IPCA', cor: Paleta.ipca },
  cambio: { titulo: 'Câmbio USD/BRL', cor: Paleta.cambio },
};

function formatarValor(nome: NomeIndicador, valor: number): string {
  if (nome === 'cambio') {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  }
  return valor.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
}

function formatarData(dataIso: string): string {
  const [ano, mes, dia] = dataIso.split('-');
  return `${dia}/${mes}`;
}

type PontoTooltip = {
  x: number;
  y: number;
  texto: string;
};

export default function TelaDetalhe() {
  const { nome } = useLocalSearchParams<{ nome: NomeIndicador }>();
  const info = INFO_INDICADOR[nome];

  const [pontos, setPontos] = useState<{ data: string; valor: number }[]>([]);
  const [carregando, setCarregando] = useState(true);
  const [tooltip, setTooltip] = useState<PontoTooltip | null>(null);

  useEffect(() => {
    async function carregar() {
      try {
        const resposta = await fetch(`${API_URL}/${nome}`);
        const dados = await resposta.json();

        const ordenados = [...dados].reverse();
        setPontos(ordenados.slice(-90));
      } catch (erro) {
        console.error(`Erro ao carregar histórico de ${nome}:`, erro);
      } finally {
        setCarregando(false);
      }
    }

    carregar();
  }, [nome]);

  const larguraTela = Dimensions.get('window').width;
  const larguraGrafico = larguraTela - 64;

  const intervaloRotulo = Math.max(1, Math.ceil(pontos.length / 6));
  const rotulos = pontos.map((ponto, indice) =>
    indice % intervaloRotulo === 0 ? formatarData(ponto.data) : ''
  );

  return (
    <SafeAreaView style={styles.tela} edges={['bottom']}>
      <Stack.Screen options={{ title: info.titulo }} />

      <ScrollView contentContainerStyle={styles.conteudo}>
        {carregando && <ActivityIndicator color={Paleta.texto} style={styles.carregando} />}

        {!carregando && pontos.length > 0 && (
          <View style={[styles.cartaoGrafico, { borderTopColor: info.cor }]}>
            <Text style={styles.tituloGrafico}>Últimos {pontos.length} registros</Text>

            {/* position: 'relative' aqui é o que permite o tooltip (position: 'absolute')
                se posicionar relativo a essa área, e não à tela inteira */}
            <View style={styles.areaGrafico}>
              <LineChart
                data={{
                  labels: rotulos,
                  datasets: [{ data: pontos.map((p) => p.valor) }],
                }}
                width={larguraGrafico}
                height={240}
                withInnerLines={false}
                bezier
                chartConfig={{
                  backgroundColor: Paleta.painel,
                  backgroundGradientFrom: Paleta.painel,
                  backgroundGradientTo: Paleta.painel,
                  decimalPlaces: 2,
                  color: () => info.cor,
                  labelColor: () => Paleta.textoSuave,
                  propsForBackgroundLines: { stroke: Paleta.borda },
                  // Pontos pequenos e discretos: precisam existir para o toque
                  // funcionar (onDataPointClick depende deles), mas ficam sutis
                  propsForDots: { r: '1', strokeWidth: '0', fill: info.cor },
                }}
                onDataPointClick={({ index, x, y }) => {
                  const ponto = pontos[index];
                  setTooltip({
                    x,
                    y,
                    texto: `${formatarData(ponto.data)}: ${formatarValor(nome, ponto.valor)}`,
                  });
                }}
                style={styles.grafico}
              />

              {tooltip && (
                <View
                  style={[
                    styles.tooltip,
                    { borderColor: info.cor, left: tooltip.x - 60, top: tooltip.y - 50 },
                  ]}
                >
                  <Text style={styles.textoTooltip}>{tooltip.texto}</Text>
                </View>
              )}
            </View>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  tela: {
    flex: 1,
    backgroundColor: Paleta.fundo,
  },
  conteudo: {
    padding: 16,
  },
  carregando: {
    marginTop: 40,
  },
  cartaoGrafico: {
    backgroundColor: Paleta.painel,
    borderTopWidth: 3,
    borderRadius: 4,
    padding: 16,
  },
  tituloGrafico: {
    color: Paleta.textoSuave,
    fontSize: 13,
    marginBottom: 8,
  },
  areaGrafico: {
    position: 'relative',
  },
  grafico: {
    borderRadius: 4,
    marginLeft: -16,
  },
  tooltip: {
    position: 'absolute',
    backgroundColor: Paleta.fundo,
    borderWidth: 1,
    borderRadius: 6,
    paddingHorizontal: 10,
    paddingVertical: 6,
    width: 120,
  },
  textoTooltip: {
    color: Paleta.texto,
    fontSize: 12,
    textAlign: 'center',
  },
});