# Extrator de Dados do prot de tela do uber via Telegram e Google Vision

Esse é um código em Python que funciona como um chatbot no Telegram. O objetivo é extrair informações de um motorista de uber, como nome, placa do carro e modelo do carro, a partir de uma imagem de tela do aplicativo de transporte do motorista enviada para o chatbot. O código utiliza a API do Google Vision para fazer a análise da imagem e reconhecimento de texto (OCR), e a API do Google Sheets para armazenar os dados extraídos. o projeto foi criado apenas para uso pessoal com o objetivo de obter um regitros dos motoristas que cancelam a corrida. 

## Pacotes Utilizados

1. telebot: biblioteca para integração com o Telegram;
2. google.cloud.vision: biblioteca para utilização do Google Vision;
3. os: biblioteca para acesso ao sistema operacional, utilizada para definir as credenciais do Google Vision;
4. re: biblioteca para operações de expressões regulares;
5. google.oauth2.service_account: biblioteca para autenticação via credenciais;
6. googleapiclient.discovery: biblioteca para utilização das APIs do Google.

## Como Utilizar

Antes de executar o código, é necessário criar as credenciais para a API do Google Vision e do Google Sheets. Em seguida, é necessário criar um bot no Telegram e obter sua chave de API. Esses dados devem ser adicionados no código, nas linhas que iniciam com os.environ['GOOGLE_APPLICATION_CREDENTIALS'] e CHAV_API, respectivamente.

Após configurar as credenciais, é possível executar o código em um ambiente Python. Ao executar o código, o bot estará ativo e pronto para receber comandos do usuário.

Os comandos disponíveis são:

1. /start ou /help: exibe uma mensagem de boas-vindas e instruções de uso do bot;
2. /nome Fulano: busca o nome do motorista na planilha do Google Sheets;
3. /placa dados: busca informações do carro do motorista (placa e modelo) na planilha do Google Sheets.
4. 
O usuário deve enviar uma imagem da tela do aplicativo de transporte do motorista para o bot. O bot irá utilizar a API do Google Vision para extrair o texto da imagem e buscar as informações na planilha do Google Sheets. Se as informações forem encontradas, o bot irá retorná-las ao usuário no chat.

## Limitações
1. A extração de informações pode falhar se a qualidade da imagem enviada pelo usuário não for boa o suficiente para o OCR.
2. A extração de informações pode falhar se os dados do motorista não estiverem na planilha do Google Sheets.
