# importando bibliotecas
from flask import Flask, request, render_template, flash, redirect, url_for, session, jsonify
from cityposer import Spotify_requesting as sr
from cityposer import cityposer_data as cpd
from json import loads, dumps
import os
import pandas as pd
import random

# Recebendo variáveis de ambiente
CLIENT_ID_SPOTIFY = os.environ.get('CLIENT_ID_SPOTIFY')
CLIENT_SECRET_SPOTIFY = os.environ.get('CLIENT_SECRET_SPOTIFY')
DATABASE_URL = os.environ.get('DATABASE_URL')

# inicializando
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET')
app.config['SESSION_TYPE'] = 'filesystem'
header_access = sr.auth_spotify(client_id=CLIENT_ID_SPOTIFY, client_secret=CLIENT_SECRET_SPOTIFY)

# Criando decoradores - links das páginas
@app.route("/", methods=['GET', 'POST']) #Home
def hello(header_access=header_access):
    # Verificando se houve postagem de algo no frontend
    if request.method == 'POST':

        # Recebendo dado do frontend
        artist_name = request.form.get('artist-input')

        # testando a biblioteca
        try:
            data = sr.get_search(artist_name, 'artist', limit= 10,header_access=header_access)

            # Validador da requisição
            if data['artists']['total'] == 0:
                    flash('Digite um nome de artista válido', 'error')
            else:
                # armazenando o dado na sessão do Flask
                session['artist_data'] = data
                return redirect(url_for('search'))

        # Caso API recuse resposta
        except Exception as error:
            pass
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST']) #Busca
def search(header_access=header_access):
    if request.method == 'POST':
    # Caso esteja recebendo um POST
        data_from_frontend = request.json
        try:
            # Criando dataframes com os dados
            select_artist_data = cpd.data_artist(data_from_frontend['id_artist'],header_access)
            album_data = cpd.data_album(data_from_frontend['id_artist'],header_access)
            track_data = cpd.data_track(data_from_frontend['id_artist'],header_access)

            # Gerando um código de usuário aleatório
            user_id = cpd.generate_userid()

            # Mandando dados para o servidor em Postgre
            tablename1 = cpd.send_data(user_id=user_id, df=select_artist_data, DATABASE_URL=DATABASE_URL, database_name='select_artist_data')
            session['tablename_artist_data'] = tablename1

            tablename2 = cpd.send_data(user_id=user_id, df=album_data, DATABASE_URL=DATABASE_URL, database_name='album_data')
            session['album_data'] = tablename2

            tablename3 = cpd.send_data(user_id=user_id, df=track_data, DATABASE_URL=DATABASE_URL, database_name='track_data')
            session['track_data'] = tablename3
            return jsonify(sucess=True)
        
        except Exception as error:
            print(f'Erro: {error}')
            return jsonify(sucess=False, error=str(error))

    # recebendo nessa função a busca anterior
    artist_data = session.get('artist_data')

    # acumulador para os dados
    show_data_list = []
    for data in artist_data['artists']['items']:
        try:
            show_data = {'name': data['name'], 'img': data['images'][0]['url'], 'id': data['id']}
            show_data_list.append(show_data)
        except:
            continue
    return render_template('search.html', show_data_json=dumps(show_data_list))

@app.route('/quiz-data', methods=['GET'])
def get_quiz_data():
    # Recebendo dados do servidor e mandando para o frontend
    artist_data_table = session.get('tablename_artist_data')
    album_data_table = session.get('album_data')
    track_data_table = session.get('track_data')

    # Requisições em SQL para gerar DF das questões
    # Questão 1
    sql_request_1 = f'''
    SELECT DISTINCT album_data.artist,
            AVG(valence) as valence_avg,
            AVG(energy) as energy_avg
    FROM public."{track_data_table}" as track_data
    JOIN public."{album_data_table}" as album_data
    ON track_data.id_y = album_data.id
    GROUP BY album_data.artist;
    '''
    question_1_df = cpd.consult_data(DATABASE_URL=DATABASE_URL, sql_request=sql_request_1)

    # Questão s2
    sql_request_2 = f'''
    SELECT DISTINCT "name", sum(duration_ms)
    FROM "{track_data_table}" as track_data
    GROUP BY "name"
    '''
    question_2_df = cpd.consult_data(DATABASE_URL=DATABASE_URL, sql_request=sql_request_2)

    # Questão 3
    sql_request_3 = f'''
    SELECT DISTINCT loudness, "track_data"."tracks.items.name" as "name"
    FROM "{track_data_table}" as track_data
    ORDER BY loudness DESC
    '''
    question_3_df = cpd.consult_data(DATABASE_URL=DATABASE_URL, sql_request=sql_request_3)

    # Questão 4
    sql_request_4 = f'''
    SELECT DISTINCT danceability, valence, "track_data"."tracks.items.name" as "name"
    FROM "{track_data_table}" AS track_data
    ORDER BY danceability ASC, valence DESC
    '''
    question_4_df = cpd.consult_data(DATABASE_URL=DATABASE_URL, sql_request=sql_request_4)

    # Questão 5
    sql_request_5 = f'''
    SELECT DISTINCT instrumentalness, speechiness, "track_data"."tracks.items.name" as "name"
    FROM "{track_data_table}" AS track_data
    ORDER BY instrumentalness ASC, speechiness DESC
    '''
    question_5_df = cpd.consult_data(DATABASE_URL=DATABASE_URL, sql_request=sql_request_5)


    # Convertendo DataFrames para listas de dicionários 
    question_1_list = question_1_df.to_dict(orient='records')
    question_2_list = question_2_df.to_dict(orient='records')
    question_3_list = question_3_df.to_dict(orient='records')
    question_4_list = question_4_df.to_dict(orient='records')
    question_5_list = question_5_df.to_dict(orient='records')

    # Deletando os dados no servidor
    cpd.delete_data(DATABASE_URL=DATABASE_URL, tablename=artist_data_table)
    cpd.delete_data(DATABASE_URL=DATABASE_URL, tablename=album_data_table)
    cpd.delete_data(DATABASE_URL=DATABASE_URL, tablename=track_data_table)

    return jsonify({
        'question_1': question_1_list,
        'question_2': question_2_list,
        'question_3': question_3_list,
        'question_4': question_4_list,
        'question_5': question_5_list,
    })

@app.route('/quiz', methods=['GET', 'POST']) #Quiz
def quiz():
    # carregar página do quiz
    return render_template('quiz.html') 

if __name__ == "__main__":
    app.run()
