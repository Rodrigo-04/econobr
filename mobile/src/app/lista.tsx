import { useEffect, useState } from 'react';
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';

import { API_URL } from '@/constants/api';
import { Paleta } from '@/constants/paleta';

type Indicador = {
  nome: 'selic' | 'ipca' | 'cambio';
  titulo: string;
  legenda: string;
  cor: string;
};

const INDICADORES: Indicador[] = [
  { nome: 'selic', titulo: 'SELIC', legenda: 'Meta definida pelo Copom', cor: Paleta.selic },
  { nome: 'ipca', titulo: 'IPCA', legenda: 'Variação mensal', cor: Paleta.ipca },
  { nome: 'cambio', titulo: 'Câmbio USD/BRL', legenda: 'Venda, fechamento diário', cor: Paleta.cambio },
];

function formatarValor(nome: Indicador['nome'], valor: number): string {
  if (nome === 'cambio') {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
  }
  return valor.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + '%';
}

function formatarData(dataIso: string): string {
  const [ano, mes, dia] = dataIso.split('-');
  return `${dia}/${mes}/${ano}`;
}

export default function TelaLista() {
  const [valores, setValores] = useState<Record<string, string>>({});
  const [dataAtualizacao, setDataAtualizacao] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    async function carregarTudo() {
      const resultados = await Promise.all(
        INDICADORES.map(async (indicador) => {
          try {
            const resposta = await fetch(`${API_URL}/${indicador.nome}/ultimo`);
            if (!resposta.ok) throw new Error(`Status ${resposta.status}`);
            const dados = await resposta.json();
            return [indicador.nome, formatarValor(indicador.nome, dados.valor), dados.data] as const;
          } catch (erro) {
            console.error(`Erro ao buscar ${indicador.nome}:`, erro);
            return [indicador.nome, 'Erro', null] as const;
          }
        })
      );

      const novosValores: Record<string, string> = {};
      let dataSelic: string | null = null;

      for (const [nome, valorFormatado, data] of resultados) {
        novosValores[nome] = valorFormatado;
        if (nome === 'selic') dataSelic = data;
      }

      setValores(novosValores);
      setDataAtualizacao(dataSelic);
      setCarregando(false);
    }

    carregarTudo();
  }, []);

  return (
    <SafeAreaView style={styles.tela} edges={['bottom']}>
      <View style={styles.lista}>
        {!carregando && (
          <Text style={styles.textoAtualizado}>
            {dataAtualizacao
              ? `Atualizado em ${formatarData(dataAtualizacao)}`
              : 'Não foi possível carregar os dados'}
          </Text>
        )}

        {carregando && <ActivityIndicator color={Paleta.texto} style={styles.carregando} />}

        {!carregando &&
          INDICADORES.map((indicador) => (
            <Pressable
              key={indicador.nome}
              style={({ pressed }) => [
                styles.cartao,
                { borderTopColor: indicador.cor },
                pressed && styles.cartaoPressionado,
              ]}
              onPress={() => router.push(`/indicador/${indicador.nome}`)}
            >
              <Text style={styles.tituloCartao}>{indicador.titulo}</Text>
              <Text style={[styles.valorCartao, { color: indicador.cor }]}>
                {valores[indicador.nome]}
              </Text>
              <Text style={styles.legendaCartao}>{indicador.legenda}</Text>
            </Pressable>
          ))}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  tela: {
    flex: 1,
    backgroundColor: Paleta.fundo,
  },
  lista: {
    padding: 16,
    gap: 16,
  },
  textoAtualizado: {
    color: Paleta.textoSuave,
    fontSize: 13,
    marginBottom: -4,
  },
  carregando: {
    marginTop: 40,
  },
  cartao: {
    backgroundColor: Paleta.painel,
    borderTopWidth: 3,
    borderRadius: 4,
    padding: 20,
  },
  cartaoPressionado: {
    opacity: 0.7,
  },
  tituloCartao: {
    color: Paleta.textoSuave,
    fontSize: 14,
    marginBottom: 8,
  },
  valorCartao: {
    fontSize: 32,
    fontWeight: '600',
    marginBottom: 6,
  },
  legendaCartao: {
    color: Paleta.textoSuave,
    fontSize: 13,
  },
});