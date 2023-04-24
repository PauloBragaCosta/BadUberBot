import telebot
from google.cloud import vision
import os
import re
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './Credencial_do_google_vision.json'

CHAV_API = "Chave API do telegram"
bot = telebot.TeleBot(CHAV_API)

# Cria um cliente da API do Google Vision
client = vision.ImageAnnotatorClient()

def extract_info(text):
    # Extrair o nome da mensagem
    name = re.search(r'Envie uma mensagem para\s([\w\s]+)', text)
    if name:
        name = name.group(1).strip() # remova espaços em branco desnecessários do nome
    else:
        name = None # retorne "None" caso o nome não seja encontrado

    # Extrair a placa do carro
    plate = re.search(r'\b[A-Z]{3}[ -]?\d[A-Z0-9]{1,3}\b', text)
    
    if plate:
        plate = plate.group(0) # atribua o valor da placa ao grupo de captura 0
    else:
        plate = None # retorne "None" caso a placa não seja encontrada

    # Extrair o modelo do carro
    if plate:
        model = re.search(r'(?<=' + plate + r')\s*([\w\s]+)', text) # pesquise o modelo depois da placa do carro
    else:
        model = re.search(r'([\w\s]+)', text) # pesquise o modelo em qualquer lugar do texto

    if model:
        model = model.group(1).strip() # remova espaços em branco desnecessários do modelo
    else:
        model = None # retorne "None" caso o modelo não seja encontrado

    return {'Nome': name, 'Placa do carro': plate, 'Modelo do carro': model}



def append_values(spreadsheet_id, range_name, values):
    """
    Appends values to a spreadsheet.
    """
    # Carregar credenciais do arquivo JSON
    creds = Credentials.from_service_account_file('./Credencial_do_google_sheets.json')
    try:
        service = build('sheets', 'v4', credentials=creds)
        # Encontre a primeira linha vazia
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        first_empty_row = len(rows) + 1
        # Acrescente os valores
        body = {
            'values': values
        }
        range_name = f"{range_name.split('!')[0]}!A{first_empty_row}"
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bem-vindo! Para começar, envie uma captura de tela da tela do motorista assim vou extrair os dados dele. Utilie o comando (/nome Fulano)e (/placa dados) para fazer uma busca na planilha dos dados")


@bot.message_handler(commands=['nome'])
def handle_search_command(message):
    try:
        command = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Por favor, informe um comando para buscar na planilha.")
        return

    # Autentica com as credenciais padrão
    creds = Credentials.from_service_account_file('./Credencial_do_google_sheets.json')

    # Cria o serviço para acessar a API do Google Sheets
    service = build('sheets', 'v4', credentials=creds)

    # ID da planilha e intervalo de células a serem lidos
    spreadsheet_id = "Chave que tem no HTML da planilha"
    range_name = 'Página1!A:A'

    # Busca os valores do intervalo especificado
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        if not values:
            bot.reply_to(message, 'Nenhum dado encontrado.')
        else:
            search_value = command
            result_found = False
            for i, row in enumerate(values):
                if row[0] == search_value:
                    bot.reply_to(message, f'Motorista encontrado na linha {i+1}, ele e um péssimo uber!')
                    result_found = True
                    break
            if not result_found:
                bot.reply_to(message, 'Valor não encontrado.')
    except HttpError as error:
        bot.reply_to(message, f'Ocorreu um erro: {error}')


@bot.message_handler(commands=['placa'])
def handle_search_command(message):
    try:
        command = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Por favor, informe um comando para buscar na planilha.")
        return

    # Autentica com as credenciais padrão
    creds = Credentials.from_service_account_file('./Credencial_do_google_sheets.json')

    # Cria o serviço para acessar a API do Google Sheets
    service = build('sheets', 'v4', credentials=creds)

    # ID da planilha e intervalo de células a serem lidos
    spreadsheet_id = "Chave que tem no HTML da planilha"
    range_name = 'Página1!C:C'

    # Busca os valores do intervalo especificado
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        if not values:
            bot.reply_to(message, 'Nenhum dado encontrado.')
        else:
            search_value = command
            result_found = False
            for i, row in enumerate(values):
                if row[0] == search_value:
                    bot.reply_to(message, f'Motorista encontrado na linha {i+1}, ele e um péssimo uber!')
                    result_found = True
                    break
            if not result_found:
                bot.reply_to(message, 'Valor não encontrado.')
    except HttpError as error:
        bot.reply_to(message, f'Ocorreu um erro: {error}')



@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Obtém a ID do arquivo da foto enviada pelo usuário
    file_id = message.photo[-1].file_id
    # Obtém informações sobre o arquivo
    file_info = bot.get_file(file_id)
    # Obtém o conteúdo do arquivo
    file_content = bot.download_file(file_info.file_path)
    
    # Cria uma imagem a partir do conteúdo do arquivo
    image = vision.Image(content=file_content)
    # Usa a API do Google Vision para extrair texto da imagem
    response = client.document_text_detection(image=image)
    
    text = response.text_annotations[0].description

    info = extract_info(text)

    append_values("Chave que tem no HTML da planilha", "Página1", [[info['Nome'], info['Modelo do carro'], info['Placa do carro'], text]])
    
    reply_text = f"Driver's name: {info['Nome']}\nCar model: {info['Modelo do carro']}\nLicense plate: {info['Placa do carro']}"

    
    # Envia o texto extraído de volta ao usuário
    bot.reply_to(message, reply_text)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
