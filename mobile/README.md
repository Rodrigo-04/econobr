# mobile

App React Native (Expo) que consome a mesma API do econobr.

## Telas planejadas
- Lista de indicadores
- Detalhe com gráfico
- Conversor de moeda (opcional)

## ambiente
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
```
http://SEU_IP:8000/selic/ultimo
```

## executando
Executa o App, podemos escanear o QR Code no App Expo Go e simular no prórpio aparelho, ou no localhost.
```bash
npx expo start
```

