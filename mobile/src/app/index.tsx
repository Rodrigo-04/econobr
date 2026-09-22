import { useEffect } from 'react';
import { StyleSheet, Text } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';

import { Paleta } from '@/constants/paleta';

export default function TelaSplash() {
  useEffect(() => {
    const temporizador = setTimeout(() => {
      router.replace('/lista');
    }, 700);

    return () => clearTimeout(temporizador);
  }, []);

  return (
    <SafeAreaView style={styles.tela}>
      <Text style={styles.titulo}>ECONOBR</Text>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  tela: {
    flex: 1,
    backgroundColor: Paleta.fundo,
    alignItems: 'center',
    justifyContent: 'center',
  },
  titulo: {
    color: Paleta.texto,
    fontSize: 36,
    fontWeight: '600',
  },
});