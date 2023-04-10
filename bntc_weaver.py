# benestic weaver
__version__ = '0.0.1'

# importando bibliotecas
import requests
from flask import request


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

# FUNÇÕES PARA ENVIO DE INFORMAÇÕES PARA O TELEGRAM
# Função para funcionamento do bot
def bot_telegram(token=str, header_access=dict):
    '''
    A função configura o bot no telegram. Retorna a reposta da API para a requisição post da mensagem.
    :param token: [STR] Token do bot do telegram, que deve ser retirada pelo botfather
    :param header_access: [DICT] Dicionário para acesso a API do Spotify
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
/novo: Recebe informações sobre o último lançamento de faixa no Brasil.'''
    
    elif user_text == '/busca':
        bot_text = '''Você pode buscar por diversas coisas no spotify. Aqui está uma lista de comandos que você pode mandar para mim:
/artistas: (coloque aqui o artista que você gostaria de saber)
/faixas: (coloque aqui a faixa de música que você gostaria de saber sobre)
/album: (coloque aqui o álbum que você quer saber mais sobre)
/playlist: (coloque aqui a playlist que você quer buscar)'''
        
    elif '/artistas' in user_text:
        query = user_text[9:].lower().strip()
        artist_info = get_search(query, type=['artist'], limit=1, header_access=header_access)
        artist_name = artist_info['artists']['items'][0]['name']
        artist_url = artist_info['artists']['items'][0]['external_urls']['spotify']
        artist_followers = artist_info['artists']['items'][0]['followers']['total']
        artist_gen = artist_info['artists']['items'][0]['genres']
        artist_pop = artist_info['artists']['items'][0]['popularity']
        bot_text = f'''Você buscou por {artist_name}!
O link de seu perfil é: {artist_url}.
{artist_name} tem {artist_followers} seguidores e tem {artist_pop}/100 de popularidade, de acordo com o Spotify.
{artist_name} faz parte do gênero: {artist_gen}.'''
    
    elif '/faixas' in user_text:
        query = user_text[8:].lower().strip()
        track_info = get_search(query, type=['track'], limit=1, header_access=header_access)
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
    
    elif '/album' in user_text:
        query = user_text[6:].lower().strip()
        album_info = get_search(query, type=['album'], limit=1, header_access=header_access)
        album_name = album_info['albums']['items'][0]['name']
        album_artist_name = album_info['albums']['items'][0]['artists'][0]['name']
        album_url = album_info['albums']['items'][0]['external_urls']['spotify']
        album_release_date = album_info['albums']['items'][0]['release_date']
        album_total_number = track_info['albums']['items'][0]['total_tracks']
        bot_text = f'''Você buscou por {album_name}!
O link da música é: {album_url}
O álbum pertence a {album_artist_name}.
Esse álbum foi publicado em {album_release_date}.
Tem o total de {album_total_number} faixas.'''

    elif '/playlist' in user_text:
        query = user_text[10:].lower().strip()
        playlist_info = get_search(query, type=['playlist'], limit=1, header_access=header_access)
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

    elif user_text == '/novo':
        new_artist = []
        new_info = get_release(country='BR', limit=1, header_access=dict)
        new_type = new_info['albums']['items'][0]['album_type']
        new_url = new_info['albums']['items'][0]['external_urls']['spotify']
        new_name = new_info['albums']['items'][0]['name']
        new_release = new_info['albums']['items'][0]['release_date']
        for n in new_info['albums']['items'][0]['artists']:
            new_artist.append(n['name'])
        bot_text = f'''O mais novo lançamento no Brasil é {new_name}, de {new_artist}.
O link do lançamento é: {new_url}
Esse lançamento é um/uma {new_type}.
Foi lançado em {new_release}
        '''

    else:
        bot_text = 'Desculpe, eu não entendi. Por favor, responda de acordo com as instruções de cada função!'
    
    bot_men = {"chat_id": user_id, "text": bot_text, "parse_mode": "HTML"}
    bot_answer = requests.post(f"https://api.telegram.org./bot{token}/sendMessage", data=bot_men).json()
    return bot_answer
