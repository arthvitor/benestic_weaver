# importando bibliotecas
import os
import bntc_weaver as weaver
from flask import Flask
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# recebendo variáveis - DEPOIS COLOCAR COMO AMBIENTE
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
TOKEN = os.environ['TELEGRAM_TOKEN']
GOOGLE_SHEETS_CREDENTIALS = os.environ['GOOGLE_SHEETS_CREDENTIALS']  
PLAN_TOKEN = os.environ['PLAN_TOKEN']  #ADICIONAR

# autorizando realização de funções no sheets
with open("credenciais.json", mode='w') as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha = api.open_by_key(PLAN_TOKEN)
sheet1 = planilha.worksheet("user_request")
sheet2 = planilha.worksheet("bot_request")

# Criando o site
app = Flask(__name__)

# testando dados do spotify 
@app.route('/')
def index():
    return 'Boas vindas ao Benestic Weaver'

@app.route('/weaver-bot', methods=["POST"])
def weaver_bot():
    header_access = weaver.auth_spotify(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    req = weaver.bot_telegram(sheet1=sheet1, sheet2=sheet2, token=TOKEN, header_access=header_access)
    return req

if __name__ == '__main__':
    app.run()
