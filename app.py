from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é meu site. (Vitor Arthur)"

if __name__ == '__main__':
    app.run()
