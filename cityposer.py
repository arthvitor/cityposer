# cityposer
__version__ = '1.0.0'

# importando bibliotecas
# from bs4 import BeautifulSoup as bs
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
from datetime import date
from time import sleep
import pandas as pd
import requests
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker
import random
import string


# CLASSE PARA REQUISIÇÕES NO SPOTIFY
class Spotify_requesting:

    # inicializando classe
    def __init__(self, client_id, client_secret) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    # Função de autenticação na API do Spotify
    def auth_spotify(client_id=str, client_secret=str):
        '''
        Retorna um dicionário que será necessário para acessar requisições no spotify. Dicionário será válido somente por 1h.
        :param str client_id: [STR] token gerado pela plataforma de desenvolvedores do spotify necessário para acessar a API
        :param str client_secret: [STR] token secreto e sensível, que também é necessário para acessar a API. Gerado pela plataforma do Spotify Dev
        :return dict header_acess:
        '''

        # Recebendo token de acesso
        passkey = Spotify_requesting(client_id, client_secret)
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        data = f'grant_type=client_credentials&client_id={passkey.client_id}&client_secret={passkey.client_secret}'
        requisicao = requests.post(f'https://accounts.spotify.com/api/token', headers=headers, data=data).json()

        # Extraindo dados da requisição
        token_type = requisicao['token_type']
        access_token = requisicao['access_token']
        header_access = {'Authorization': f'{token_type}  {access_token}'}  # qualquer requisição tem que ter esse header

        return header_access
    
    # função para realizar query na API do Spotify
    def get_search(query=str, type=str, limit=int, header_access=dict):
        '''
        Retorna um dicionário com resultados da query
        :param query: [STR] query de busca no spotify
        :param type: [STR] tipo da busca feita. São aceitos: "album", "artist", "playlist", "track", "show", "episode", "audiobook"
        :param limit: [INT] Limite de resultados que serão retornados
        '''
        query_data = {
            'q': query,
            'type': type,
            'limit': limit
            }
        result = requests.get(f'https://api.spotify.com/v1/search', headers=header_access, params=query_data).json()
        return result
    
    # Coletando informações sobre artistas
    def get_artist(id_artist=str, header_access=dict):
        '''
        Retorna um dicionário com resultado sobre o artista
        :param id_artist: [STR] id do artista que será buscada
        :param header_acess: [DICT] Dicionário para que haja autorização para a requisição
        :return dict result:
        '''
        id = id_artist
        query_data = {
            'id': id
        }
        result = requests.get(f'https://api.spotify.com/v1/artists/{id}', headers=header_access, params=query_data).json()
        return result
    
    # Coletando informações sobre os álbuns dos artistas
    def get_albums_id(id_artist=str, header_access=dict):
        '''
        Retorna um dicionário com resultado da query sobre os albuns dos artistas
        :param id_artist: [STR] id do artista que será buscada
        :param header_acess: [DICT] Dicionário para que haja autorização para a requisição
        :return dict result:
        '''
        id = id_artist
        query_data = {
            'id': id
        }
        result = requests.get(f'https://api.spotify.com/v1/artists/{id}/albums', headers=header_access, params=query_data).json()
        return result
    
    # Coletando informações sobre os álbuns dos artistas
    def get_several_albums(id_albums=str, header_access=dict):
        '''
        Retorna um dicionário com resultado da query sobre as faixas de albuns por lista
        :param id_artist: [STR] id do artista que será buscada
        :param header_acess: [DICT] Dicionário para que haja autorização para a requisição
        :return dict result:
        '''
        id = id_albums
        query_data = {
            'ids': id
        }
        result = requests.get(f'https://api.spotify.com/v1/albums', headers=header_access, params=query_data).json()
        return result
    
    # Coletando Ids das tracks de um album
    def get_album(id_album=str, limit=int, header_access=dict):
        '''
        Retorna um dicionário com resultados da query sobre um único album
        :param id_album: [STR] id do album que será buscada
        :param limit: [INT] limite de faixas que serão retornadas na requisição
        :param header_acess: [DICT] Dicionário para que haja autorização para a requisição
        :return dict result:
        '''
        id = id_album
        query_data = {
            'limit': limit
            }
        result = requests.get(f'https://api.spotify.com/v1/albums/{id}/tracks', headers=header_access, params=query_data).json()
        return result
    
    # Coletando informações das tracks por uma lista de IDs
    def get_tracks_info(id_track=list, header_access=dict):
        '''
        Retorna um dicionário com resultados da query com as informações das tracks na lista recebida
        :param id_album: [LIST] ids das tracks
        :param header_acess: [DICT] Dicionário para que haja autorização para a requisição
        '''
        query_data = {
            'ids': id_track
            }
        result = requests.get(f'https://api.spotify.com/v1/audio-features', headers=header_access, params=query_data).json()
        return result

# CLASSE PARA REALIZAÇÃO DE AUTOMAÇÃO EM SELENIUM NO TWITTER
class Twitter_requesting:

    # inicializando classe
    def __init__(self, twitter_id, twitter_pass) -> None:
        self.twitter_id = twitter_id
        self.twitter_pass = twitter_pass
        pass
    
    # Configurando scrapper do Twitter
    def scrapper_config(twitter_id, twitter_pass, req_arg):
        '''
        :param twitter_id: [STR] Id de usuário para login no Twitter
        :param twitter_pass: [STR] Senha da conta para login no Twitter
        :param req_arg: [STR] Argumentos de acordo com a busca avançada booleana do Twitter
        '''

        # recebendo chaves de autentificação
        cred = Twitter_requesting(twitter_id, twitter_pass)

        # Configurando Selenium
        options = Options()
        options.headless = True
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        
        # iniciando captura dos dados
        # Página de Login - Username
        driver.get('https://twitter.com/i/flow/login')
        sleep(5)
        driver.find_element(By.CSS_SELECTOR, 'input.r-30o5oe').send_keys(cred.twitter_id)
        botao_user = driver.find_element(By.XPATH, "//div[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-usiww2 r-13qz1uu r-2yi16 r-1qi8awa r-ymttw5 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']")
        driver.execute_script("arguments[0].click();", botao_user)

        # Página de Login - Password
        sleep(2)
        driver.find_element(By.XPATH, "//input[@class='r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7']").send_keys(cred.twitter_pass)
        botao_senha = driver.find_element(By.XPATH, "//div[@class='css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-19yznuf r-64el8z r-1dye5f7 r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l']")
        driver.execute_script("arguments[0].click();", botao_senha)

        # Entrando na página de busca
        sleep(5)
        botao_pesquisa = driver.find_element(By.XPATH, "//a[@href='/explore']")
        driver.execute_script("arguments[0].click();", botao_pesquisa)

        # Recebendo requsição
        pesquisa = req_arg # Operadores de busca avançada booleana do Twitter

        # inserindo texto e mandando pesquisar
        sleep(3)
        driver.find_element(By.XPATH, "//input[@class='r-30o5oe r-1dz5y72 r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-xyw6el r-13qz1uu r-fdjqy7']").send_keys(pesquisa, Keys.ENTER)

        # Raspando informação
        tweets = list()  # acumulador
        contador = -1

        # Desce a página, e captura de 3 em 3 tweets que estão disponíveis
        while True:
            twitter = driver.page_source
            sleep(5)
            driver.execute_script("window.scrollBy(0, 2000);")

            # fazendo teste lógico
            if contador == -1:
                contador += 1  
                tweets.append(twitter)
                continue
            elif twitter != tweets[contador]:
                tweets.append(twitter)
            elif twitter == tweets[contador]:
                break

            # Contador para o caso de não ser a primeira condição
            contador += 1
        
        return tweets

    # recebendo dados estruturados da requisição
    def parse_tweets(tweets=list):
        '''
        :param tweets: [LIST] Lista de dados capturados no Twitter que ainda não estão estruturados
        '''

        # Recebendo dados capturados e restruturando com BeautifulSoup
        twitter = list()
        for l in tweets:
            linha = bs(l)
            linha_tweet = linha.findAll('div', {'data-testid': 'cellInnerDiv'})
            twitter.append(linha_tweet)
        
        # Estruturando dados em uma lista
        # acumulador
        twitter_dados = list()

        # coletando dados montagem da base
        for l in twitter: # loop para acessar os dados da lista
            for t in l:
                # conteúdo do tweet
                try:
                    tweet = t.find('div', {'class': 'css-1rynq56 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim'}).text 
                except:
                    continue
                        
                # nome de usuário
                username = t.find('a', {'class': 'css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21'}).text 

                # link do perfil do usuário
                username_link = f"twitter.com{t.find('a', {'class': 'css-175oi2r r-1wbh5a2 r-dnmrzs r-1ny4l3l r-1loqt21'}).get('href')}"

                # Se o tweet é um reply ou não (booleano)
                try:
                    t.find('div', {'class': 'css-175oi2r r-4qtqp9 r-zl2h9q'}).text
                    reply = True
                except:
                    reply = False
                
                # link do post
                link = f"twitter.com{t.find('a', {'class': 'css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-xoduu5 r-1q142lx r-1w6e6rj r-9aw3ui r-3s2u2q r-1loqt21'}).get('href')}"

                # data do post
                data_post = t.find('time', {'class': 'css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-xoduu5 r-1q142lx r-1w6e6rj r-9aw3ui r-3s2u2q r-1loqt21'}.get('datetime')).get('datetime')[0:10]

                # data da coleta
                data_coleta = date.today()

                # estatísticas do tweet
                estatisticas = t.findAll('div', {'class': 'css-175oi2r r-1kbdv8c r-18u37iz r-1wtj0ep r-1ye8kvj r-1s2bzr4'})[0].get('aria-label')
                estatisticas = estatisticas.split(',')

                metricas = dict()

                for m in estatisticas:
                    data_metrica = m.strip().split(' ')

                    # respostas
                    if {'resposta', 'respostas'} & set(data_metrica):
                        metricas.update({data_metrica[1][0:8]: data_metrica[0]})
                        
                    # reposts
                    elif {'repost', 'reposts'} & set(data_metrica):
                        metricas.update({data_metrica[1][0:6]: data_metrica[0]})

                    # curtidas
                    elif {'curtidas', 'curtida'} & set(data_metrica):
                        metricas.update({data_metrica[1][0:7]: data_metrica[0]})

                    # visualizações
                    elif {'visualizações', 'visualização'} & set(data_metrica):
                        metricas.update({data_metrica[1][0:4]: data_metrica[0]})
                
                # armazenando todos os dados dentro de uma lista
                twitter_dados.append([tweet, username, username_link, reply, link, data_post, data_coleta, metricas])

        return twitter_dados

# CLASSE PARA TRATAMENTO DOS DADOS DO SPOTIFY
class cityposer_data:
    # inicializando classe
    def __init__(self) -> None:
        pass

    # Função para recolhimento dos dados do Twitter
    def data_artist(keyword=str, header_access=dict):
        """
        :param keyword: [STR] Parâmetros de busca na API do Spotify
        :param header_acess: [DICT] Dicionário de chaves autenticação na API do Spotify
        """
        
        # DATAFRAME PARA ARTISTA
        # dados dos artistas
        artista = Spotify_requesting.get_artist(id_artist=keyword, header_access=header_access)

        # acumulando dados para o dataframe
        data_artist = {'name': [artista['name']], 'followers': [artista['followers']['total']], 'genres': [artista['genres']], 'img': [artista['images'][0]['url']], 'popularity': [artista['popularity']]}

        # Criando dataframe
        data_artist = pd.DataFrame(data_artist)

        return data_artist
    
    def data_album(keyword=str, header_access=dict):
        """
        :param keyword: [STR] Parâmetros de busca na API do Spotify
        :param header_acess: [DICT] Dicionário de chaves autenticação na API do Spotify
        """

        # DATAFRAME DAS MÚSICAS
        # dados dos artistas
        artista = Spotify_requesting.get_artist(id_artist=keyword, header_access=header_access)

        # dados do album pelo artista
        albuns = Spotify_requesting.get_albums_id(keyword, header_access=header_access)

        # Tratando dados para serem recebidos pelo dataframe
        data_albuns = list()
        for a in albuns['items']:
            type_album = a['album_type']
            link = a['external_urls']['spotify']
            id = a['id']
            img = a['images'][0]['url']
            name_album = a['name']
            release_date = a['release_date']
            total_tracks = a['total_tracks']
            artist = artista['name']
            data_albuns.append([type_album, link, id, img, name_album, release_date, total_tracks, artist])

        # Criando dataframe
        data_album = pd.DataFrame(data_albuns, columns=['type_album', 'link', 'id', 'img', 'name_album', 'release_date', 'total_tracks', 'artist'])

        return data_album
    
    # Função para pormenorizar a lista de IDs
    def chunks(lst, chunk_size):
        """Divide a lista em lotes menores."""
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]
    
    # Função para receber dados das faixas dos albuns
    def data_track(keyword=str, header_access=dict, chunk_size=100):
        """
        :param keyword: [STR] Parâmetros de busca na API do Spotify
        :param header_acess: [DICT] Dicionário de chaves autenticação na API do Spotify
        """
        # dados do album pelo artista
        albuns = Spotify_requesting.get_albums_id(keyword, header_access=header_access)

        # CRIANDO DATAFRAME PARA TRACKS - ANALISE
        # armazenando os dados de IDs dos albuns
        album_ids = list()
        for a in albuns['items']:
            album_ids.append(a['id'])
        album_ids = ','.join(album_ids)

        # Recebendo os dados de ID das tracks dos albuns
        ids_tracks = Spotify_requesting.get_several_albums(id_albums=album_ids, header_access=header_access)

        # tratando os dados para fazer a requisição de IDs e receber as análises de cada uma
        tracks_id = list()
        for a in ids_tracks['albums']:
            for t in a['tracks']['items']:
                tracks_id.append(t['id'])
        
         # Quebrar as IDs de faixas em lotes menores
        tracks_id_chunks = list(cityposer_data.chunks(tracks_id, chunk_size))

        # Lista para armazenar os resultados de cada lote
        all_dados_tracks = []

        # Fazer solicitações para cada lote
        for chunk in tracks_id_chunks:
            chunk_ids = ','.join(chunk)

            # Fazer requisição para receber os dados analisados do Spotify para o lote atual
            dados_tracks = Spotify_requesting.get_tracks_info(id_track=chunk_ids, header_access=header_access)

            # Adicionar os resultados à lista
            all_dados_tracks.append(dados_tracks)
        
        # Concatenar os resultados de todos os lotes
        final_dados_tracks = {}
        for dados_tracks in all_dados_tracks:
            final_dados_tracks.update(dados_tracks)

        # Verificando as variáveis que precisam estar junto à tabela
        tracks_info = pd.DataFrame(final_dados_tracks['audio_features'])
        tracks_info.head(1)

        # CRIANDO DATAFRAME DAS TRACKS - DADOS SOBRE
        # Normalizando os dados
        df_tracks = pd.json_normalize(ids_tracks['albums'], max_level=1)
        df_tracks.drop(['artists', 'available_markets', 'genres', 'copyrights', 'images'], axis=1, inplace=True)
        track_items = df_tracks.explode(column='tracks.items')

        # Redefinir índices
        track_items.reset_index(drop=True, inplace=True)

        # Criando dataframe resultante
        df_result = pd.concat([track_items, pd.json_normalize(track_items['tracks.items']).add_prefix('tracks.items.')], axis=1).drop('tracks.items', axis=1)
        df_result.drop(['tracks.items.artists', 'tracks.items.available_markets'], axis=1, inplace=True)
        df_result.head(1)

        # JUNTANDO OS DATAFRAMES DAS TRACKS
        tracks_info = tracks_info.merge(df_result, left_on='id', right_on='tracks.items.id')

        return tracks_info
    
    # Função para mandar dados para o servidor
    def send_data(user_id, df, DATABASE_URL, database_name):
        try:
            alchemyEngine = create_engine(DATABASE_URL, pool_recycle=3600)
            postgreSQLConnection = alchemyEngine.connect()
            tablename = f'{user_id}_{database_name}'
            df.to_sql(tablename, con=postgreSQLConnection, if_exists='replace', index=False)
        except Exception as ex:
            print(f"Erro ao salvar dados no banco de dados: {ex}")
        finally:
            postgreSQLConnection.close()
        
        return tablename
    
    # Função para ler dados do servidor
    def consult_data(DATABASE_URL, sql_request):
        try: 
            engine = create_engine(DATABASE_URL, pool_recycle=3600)
            postgreSQLConnection = engine.connect()
            sql_request = sql_request
            df = pd.read_sql(sql_request, con=postgreSQLConnection)

        except Exception as ex:
            print(f"Erro ao ler os dados: {ex}")
            pass

        finally:
            postgreSQLConnection.close()
        return df
    
    # Função para deletar os dados da base assim que terminar o quiz
    def delete_data(DATABASE_URL, tablename):
        try:
            engine = create_engine(DATABASE_URL, pool_recycle=3600)
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            if tablename in existing_tables:
                table = Table(tablename, MetaData(), autoload_with=engine)
                table.drop(bind=engine)
            else:
                print(f"A tabela {tablename} não existe.")
        
        except Exception as ex:
            print(f"Erro ao deletar tabela do banco de dados: {ex}")

        finally:
            engine.dispose()

    # Função para geração de ID aleatório de usuário - Identificação da tabela utilizada
    def generate_userid(length=5):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))
