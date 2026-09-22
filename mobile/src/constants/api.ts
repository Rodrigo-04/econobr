/**
 * URL base da API, lida da variável de ambiente EXPO_PUBLIC_API_URL (arquivo .env).
 * Se não estiver definida, cai num valor de aviso — sinal de que o .env está faltando.
 */
export const API_URL = process.env.EXPO_PUBLIC_API_URL ?? 'http://CONFIGURE_O_ENV';

if (!process.env.EXPO_PUBLIC_API_URL) {
  console.warn(
    'EXPO_PUBLIC_API_URL não definida. Crie o arquivo mobile/.env (veja .env.example).'
  );
}