# importando bibliotecas
import os
from flask import Flask
import bntc_weaver as weaver

# recebendo variáveis - DEPOIS COLOCAR COMO AMBIENTE
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
TOKEN = os.environ['TELEGRAM_TOKEN']

# Criando o site
app = Flask(__name__)

# testando dados do spotify 
@app.route('/')
def index():
    return 'Boas vindas ao Benestic Weaver'

@app.route('/weaver-bot', methods=["POST"])
def weaver_bot():
    header_access = weaver.auth_spotify(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    req = weaver.bot_telegram(token=TOKEN, header_access=header_access)
    return req

if __name__ == '__main__':
    app.run()
