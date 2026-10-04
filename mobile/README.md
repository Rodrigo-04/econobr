# mobile

[← voltar ao README principal](../README.md)
 
App React Native (Expo, com Expo Router) que consome a mesma API do econobr. Testado via Expo Go em dispositivo físico.

## Telas
 
- **Splash** (`src/app/index.tsx`) — tela de abertura rápida com o nome do app
- **Lista** (`src/app/lista.tsx`) — cartões com o último valor de cada indicador e a data da   última atualização
- **Detalhe** (`src/app/indicador/[nome].tsx`) — histórico em gráfico de linha (últimos 90 registros), com tooltip ao tocar em qualquer ponto

## Identidade visual
 
Mesma paleta de cores do dashboard web (`src/constants/paleta.ts`), para manter consistência visual entre as duas plataformas.

## Ambiente
Criar app na pasta existente "mobile"
```bash
npx create-expo-app mobile
```

Para Acessar a API pelo celular precisamos do IP do computador, pois é onde está nosso servidor
```bash
ipconfig
```
Também preciamos permitir que o Uvicorn permita conexões da rede
```bash
uvicorn main:app --reload --host 0.0.0.0
```
Para testar a conexão podemos abrir no navegador do celular a API:
`http://SEU_IP:8000/selic/ultimo`

Precisamos das bibliotecas de gráfico, para instalar:
```bash
npm install react-native-chart-kit react-native-svg
```

## Como rodar
  
Copie `.env.example` para `.env` e preencha `EXPO_PUBLIC_API_URL` — pode apontar para a API publicada no Render (funciona de qualquer rede) ou para o IP local da sua máquina na rede Wi-Fi (necessário reiniciar `expo start` após qualquer mudança no `.env`).
 
```bash
cd mobile
npm install
npx expo start
```
 
Escaneie o QR code com o app **Expo Go** no celular.
 
## Decisão de navegação
 
O template padrão do `create-expo-app` vem com abas nativas (`NativeTabs`) e um sistema de temas mais elaborado. Optou-se por simplificar para uma navegação em pilha (Stack) simples (lista → detalhe), mantendo o foco no consumo de dados e visualização, sem a complexidade adicional de abas nativas não essenciais ao escopo do projeto.
