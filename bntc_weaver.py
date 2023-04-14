# benestic weaver
__version__ = '1.0.0'

# importando bibliotecas
import requests
import gspread
from flask import request
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen


# FUNÇÕES PARA RECEBER DADOS DO SPOTIFY
# função para receber o token de acesso da API
def auth_spotify(client_id=str, client_secret=str):
    '''
    Retorna um dicionário que será necessário para acessar requisições no spotify. Dicionário será válido somente por 1h.
    :param str client_id: [STR] token gerado pela plataforma de desenvolvedores do spotify necessário para acessar a API
    :param str client_secret: [STR] token secreto e sensível, que também é necessário para acessar a API. Gerado pela plataforma do Spotify Dev
    :return dict header_acess:
    '''

    # Recebendo token de acesso
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    data = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    requisicao = requests.post(f'https://accounts.spotify.com/api/token', headers=headers, data=data).json()

    # Extraindo dados da requisição
    token_type = requisicao['token_type']
    access_token = requisicao['access_token']
    header_access = {'Authorization': f'{token_type}  {access_token}'}  # qualquer requisição tem que ter esse header

    return header_access


# função para realizar query na API do Spotify
def get_search(query=str, type=list, limit=int, header_access=dict):
    '''
    Retorna um dicionário com resultados da query
    :param query: [STR] query de busca no spotify
    :param type: [STR] tipo da busca feita. São aceitos: "album", "artist", "playlist", "track", "show", "episode", "audiobook"
    :param limit: [INT] 
    '''
    query_data = {
        'q': query,
        'type': type,
        'limit': limit
        }
    result = requests.get(f'https://api.spotify.com/v1/search', headers=header_access, params=query_data).json()
    return result


# função para receber novos lançamentos de álbuns
def get_release(country=str, limit=int, header_access=dict):
    query_data = {
        'country': country,
        'type': type,
        'limit': limit
        }
    result = requests.get(f'https://api.spotify.com/v1/browse/new-releases', headers=header_access, params=query_data).json()
    return result


# função para recomendação do dia
def recommend_noti(header_access, seed_artist, seed_genres):
    '''
    Função retorna uma recomendação de música, dependendo do gênero e de um outro artista
    :param header_access: [DICT] header de autentificação
    :param seed_artist: [STR] Nome do artista base
    :param seed_genres: [STR] Gênero para base da busca
    :return str musica:
    '''

    # acumulador de singles
    list_singles = []
    artist = get_search(seed_artist, ['artist'], limit=1, header_access=header_access)
    artist_id = artist['artists']['items'][0]['id']

    # query da requsição
    query_data = {
    'limit': 100,
    'seed_artist': [artist_id],
    'seed_genres': [seed_genres]}
    recommend_not = requests.get(f'https://api.spotify.com/v1/recommendations', headers=header_access, params=query_data).json()

    # adicionando id de singles ao acumulador
    for n in recommend_not['tracks']:
        if n['album']['album_group'] == 'SINGLE':
            list_singles.append(n['album']['id'])
        
    id=list_singles[0]
    musica = requests.get(f'https://api.spotify.com/v1/albums/{id}', headers=header_access).json()
    return musica


# FUNÇÃO PARA CRIAÇÃO DE IMAGEM
def make_release_image(url=str):
    '''
    Função retorna imagem de capa do último lançamento
    :param url: [STR] URL da imagem do Spotify que será usada como capa
    :return PIL.Image.Image out:
    '''

    # gerando sobreposição da mascara com imagem do spotify
    url = url
    im1 = Image.open('lancamento.png').convert('RGBA')
    im2 = Image.open(urlopen(url)).convert('RGBA')
    n_im = Image.alpha_composite(im2, im1)
    date = str(datetime.date.today())

    #Gerando texto da imagem
    txt = Image.new('RGBA', n_im.size, (255, 255, 255, 0))

    #fonte
    fnt1 = ImageFont.truetype('Roboto-Regular.ttf', 15)

    # gerando imagem
    d = ImageDraw.Draw(txt)

    # gerando texto
    d.text((50, 495), f"data - {date}", font=fnt1, fill=(255, 255, 255, 255))
    out = Image.alpha_composite(n_im, txt)

    return out 

# FUNÇÃO PARA CRIAÇÃO DE IMAGEM
def make_music_image(url=str):
    '''
    Função retorna imagem de capa da música do dia
    :param url: [STR] URL da imagem do Spotify que será usada como capa
    :param linha_1: [STR] Linha 1 do título da playlist
    :param linha_2: [STR] Linha 2 do título da playlist
    :return PIL.Image.Image out:
    '''

    # gerando sobreposição da mascara com imagem do spotify
    url = url
    im1 = Image.open('musica.png').convert('RGBA')
    im2 = Image.open(urlopen(url)).convert('RGBA')
    n_im = Image.alpha_composite(im2, im1)
    date = str(datetime.date.today())

    #Gerando texto da imagem
    txt = Image.new('RGBA', n_im.size, (255, 255, 255, 0))

    #fonte
    fnt1 = ImageFont.truetype('Roboto-Regular.ttf', 15)

    # gerando imagem
    d = ImageDraw.Draw(txt)

    # gerando texto
    d.text((50, 495), f"data - {date}", font=fnt1, fill=(255, 255, 255, 255))
    out = Image.alpha_composite(n_im, txt)

    return out 


# FUNÇÕES PARA ENVIO DE INFORMAÇÕES PARA O TELEGRAM
# Função para funcionamento do bot
def bot_telegram(sheet1, sheet2, token=str, header_access=dict):
    '''
    A função configura o bot no telegram. Retorna a reposta da API para a requisição post da mensagem.
    :param token: [STR] Token do bot do telegram, que deve ser retirada pelo botfather
    :param header_access: [DICT] Dicionário para acesso a API do Spotify
    :param sheet1: Autorização por meio de função no Google Sheets que deve estar presente no app.py - Mensagem do usuário
    :param sheet2: Autorização por meio de função no Google Sheets que deve estar presente no app.py - Mensagem do bot
    '''
    
    #variáveis da função
    user_mens = request.json
    user_id = user_mens['message']['chat']['id']
    user_name = user_mens['message']['chat']['first_name']
    user_text = user_mens['message']['text']

    # funções do chat
    if user_text == '/start':
        bot_text = f'''Olá, {user_name}, tudo bem? Boas vindas ao Weaver. O que você gostaria de fazer?
/busca: Busca por algo específico no Spotify
/novo: Recebe informações sobre o último lançamento de faixa no Brasil
/sugestao_musica: (Coloque aqui, em ordem e entre vírgulas, um artista que você gosta e um gênero de música que você curte)'''
    
    elif user_text == '/busca':
        bot_text = '''Você pode buscar por diversas coisas no spotify. Aqui está uma lista de comandos que você pode mandar para mim:
/artistas: (coloque aqui o artista que você gostaria de saber)
/faixas: (coloque aqui a faixa de música que você gostaria de saber sobre)
/album: (coloque aqui o álbum que você quer saber mais sobre)
/playlist: (coloque aqui a playlist que você quer buscar)'''
        
    elif '/artistas' in user_text:
        query = user_text[9:].lower().strip()
        try:
            artist_info = get_search(query, type=['artist'], limit=1, header_access=header_access)
            bot_text = 'Não consegui encontrar nada. Tente novamente'
            artist_name = artist_info['artists']['items'][0]['name']
            artist_url = artist_info['artists']['items'][0]['external_urls']['spotify']
            artist_followers = artist_info['artists']['items'][0]['followers']['total']
            artist_gen = artist_info['artists']['items'][0]['genres']
            artist_pop = artist_info['artists']['items'][0]['popularity']
            if type(artist_gen) == list:
                artist_gen = ', '.join(artist_gen)
            bot_text = f'''Você buscou por {artist_name}!
O link de seu perfil é: {artist_url}.
{artist_name} tem {artist_followers} seguidores e tem {artist_pop}/100 de popularidade, de acordo com o Spotify.
{artist_name} faz parte do gênero: {artist_gen}.'''
        except: 
            bot_text = f'''Não consegui encontrar um resultado. Tente novamente!'''

    elif '/faixas' in user_text:
        query = user_text[8:].lower().strip()
        try:
            track_info = get_search(query, type=['track'], limit=1, header_access=header_access)
            bot_text = 'Não consegui encontrar nada. Tente novamente'
            track_name = track_info['tracks']['items'][0]['name']
            track_artist_name = track_info['tracks']['items'][0]['artists'][0]['name']
            track_url = track_info['tracks']['items'][0]['external_urls']['spotify']
            track_album_name = track_info['tracks']['items'][0]['album']['name']
            track_release_date = track_info['tracks']['items'][0]['album']['release_date']
            track_number = track_info['tracks']['items'][0]['track_number']
            track_pop = track_info['tracks']['items'][0]['popularity']
            bot_text = f'''Você buscou por {track_name}!
O link da música é: {track_url}
A música pertence a {track_artist_name}, no álbum {track_album_name}, sendo a {track_number}ª música.
Essa música foi publicada em {track_release_date}.
A popularidade dessa música é de {track_pop}/100'''
        except: 
            bot_text = f'''Não consegui encontrar um resultado. Tente novamente!'''
    
    elif '/album' in user_text:
        query = user_text[6:].lower().strip()
        try:
            album_info = get_search(query, type=['album'], limit=1, header_access=header_access)
            bot_text = 'Não consegui encontrar nada. Tente novamente'
            album_name = album_info['albums']['items'][0]['name']
            album_artist_name = album_info['albums']['items'][0]['artists'][0]['name']
            album_url = album_info['albums']['items'][0]['external_urls']['spotify']
            album_release_date = album_info['albums']['items'][0]['release_date']
            album_total_number = album_info['albums']['items'][0]['total_tracks']
            bot_text = f'''Você buscou por {album_name}!
O link da música é: {album_url}
O álbum pertence a {album_artist_name}.
Esse álbum foi publicado em {album_release_date}.
Tem o total de {album_total_number} faixas.'''
        except: 
            bot_text = f'''Não consegui encontrar um resultado. Tente novamente!'''

    elif '/playlist' in user_text:
        query = user_text[10:].lower().strip()
        try:
            playlist_info = get_search(query, type=['playlist'], limit=1, header_access=header_access)
            bot_text = 'Não consegui encontrar nada. Tente novamente'
            playlist_name = playlist_info['playlists']['items'][0]['name']
            playlist_url = playlist_info['playlists']['items'][0]['external_urls']['spotify']
            playlist_iscollab = playlist_info['playlists']['items'][0]['collaborative']
            playlist_owner = playlist_info['playlists']['items'][0]['owner']['display_name']
            if playlist_iscollab == False:
                playlist_iscollab = 'não é colaborativa'
            else:
                playlist_iscollab = 'é colaborativa'
            bot_text = f'''Encontrei uma playlist com o nome {playlist_name}.
O link da playlist é: {playlist_url}
A playlist {playlist_iscollab}!
O nome da pessoa que fez essa playlist é {playlist_owner}.        
        '''
        except: 
            bot_text = f'''Não consegui encontrar um resultado. Tente novamente!'''

    elif user_text == '/novo':
        new_artist = []
        new_info = get_release(country='BR', limit=1, header_access=header_access)
        bot_text = 'Não consegui encontrar nada. Tente novamente'
        new_type = new_info['albums']['items'][0]['album_type']
        new_url = new_info['albums']['items'][0]['external_urls']['spotify']
        new_name = new_info['albums']['items'][0]['name']
        new_release = new_info['albums']['items'][0]['release_date']
        new_image_url = new_info['albums']['items'][0]['images'][0]
        img = make_music_image(url=new_image_url)
        for n in new_info['albums']['items'][0]['artists']:
            new_artist.append(n['name'])
            new_artist = ', '.join(new_artist)
        bot_img = {"chat_id": user_id, 'photo': img}
        requests.post(f"https://api.telegram.org./bot{token}/sendPhoto", data=bot_img).json()
        bot_text = f'''O mais novo lançamento no Brasil é {new_name}, de {new_artist}.
O link do lançamento é: {new_url}
Esse lançamento é um {new_type}.
Foi lançado em {new_release}'''

    elif '/sugestao_musica' in user_mens:
        user_input = user_mens.split(',').strip()
        artist = user_input[0]
        genres = user_input[1]
        sugest = recommend_noti(header_access, [artist], [genres])
        data = recommend_noti(header_access, artist, genres)
        artist_name = data['artists'][0]['name']
        music_name = data['name']
        image_url = data['images'][0]['url']
        music_url = data['tracks']['items'][0]['external_urls']['spotify']
        img = make_music_image(url=image_url)
        bot_text = f'''A sugestão de música que você pediu chegou!
Para você que gosta de {artist} e {genres}, recomendo {music_name}, de {artist_name}!
Acesse a música aqui: {music_url}        
        '''
        bot_img = {"chat_id": user_id, 'photo': img}
        requests.post(f"https://api.telegram.org./bot{token}/sendPhoto", data=bot_img).json()

    else:
        bot_text = 'Desculpe, eu não entendi. Por favor, responda de acordo com as instruções de cada função!'
    
    bot_men = {"chat_id": user_id, "text": bot_text, "parse_mode": "HTML"}
    bot_answer = requests.post(f"https://api.telegram.org./bot{token}/sendMessage", data=bot_men).json()
    
    # mandando dados para o Google Sheets
    date = str(datetime.now())
    sheet1.append_row(['user', user_id, user_name, user_text, date])
    sheet2.append_row(['bot', bot_text, date])

    return bot_answer
