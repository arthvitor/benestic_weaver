![benestic_weaver](https://user-images.githubusercontent.com/61673650/230957503-f96a2302-9e58-4347-aab8-a0ec101aeefa.png)

# Benestic Weaver
Boas vindas ao Benestic Weaver, um bot do Telegram que transmite informações da API do Spotify. Essa automação é feita em Flask e hospedada no render.
Para conferir a página do bot, clique nesse link: https://benestic-weaver.onrender.com

## Primeiros Passos
Para utilizar esse app, você deve ter conhecimentos de automação em núvem, Flask e hospedagem no Render, além de uma conta de desenvolvedor no Telegram, Spotify e Google.



1. Baixe os arquivos:
  a) `app.py` - Com as definições para o site e o uso das funções do bot;
  b) `bntc_weaver.py` - Módulo Python local para utilização das funções presentes no `app.py`
  c) `requerements.txt` - Arquivo que informa o Render quais bibliotecas e módulos que precisaram ser instalados no ambiente virtual
2. Subir os arquivos, com as devidas alterações para o seu projeto, em um repositório público no GitHub;
3. Criar um ambiente virtual Python no Render, utilizando os códigos desse repositório como base;
4. Definir as variáveis de ambiente no Render, com as chaves de cada API que será utilizada no projeto;
5. Implementar o site, usando o botão Deploy, dentro do dashboard do Render.

## Telegram Webhook:
Para que o aplicativo funcione de maneira adequada, é necessário criar um Webhoock, junto a API do Telegram, com o seguinte código:
```
import requests

dados = {'url': '(LINK DO SEU BOT NO RENDER)'}
resposta = requests.post(f'https://api.telegram.org/bot(TOKEN DA API DO TELEGRAM)/setWebhook', data=dados)
print(resposta.text)
```

## Para quê serve o Weaver:
O Weaver é um bot capaz de trazer informações sobre artistas, álbuns, playlists e músicas para um usuário do Telegram. Também pode ser utilizado como base para aplicações mais fáceis da API, utilizando localmente o módulo bntc_weaver.py, disponível nesse repositório. 

Ainda será desenvolvido novas funções com o decorrer do tempo para deixar o bot mais útil para mais lugares.

## O que é Benestic?
Benestic é um studio de criatividade e inovação, fundado por três comunicadores para trazer novos ares a área de assessoria de comunicação e análise de dados, com atendimento mais humano e aceleração de carreiras. Para saber mais sobre a Benestic Studio, entre em nosso instagram: https://www.instagram.com/benestic.studio/

## Finalidade desse projeto
Esse projeto foi desenvolvido como trabalho final para a disciplina Algoritmo de Automação, da pós-graduação em Jornalismo de Dados, Automação e Data Storytelling, do Insper. Também é um produto da Benestic Studio. 

## Contatos:
Benestic Studio: benestic.studio@gmail.com
Vitor Arthur (desenvolvedor do projeto): vitorarthur.profissional@gmail.com
