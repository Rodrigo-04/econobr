import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: '#0F1B2D' },
        headerTintColor: '#EDEAE3',
        headerTitleStyle: { fontWeight: '600' },
        contentStyle: { backgroundColor: '#0F1B2D' },
      }}
    >
      <Stack.Screen name="index" options={{ headerShown: false }} />
      <Stack.Screen name="lista" options={{ title: 'econobr' }} />
    </Stack>
  );
}