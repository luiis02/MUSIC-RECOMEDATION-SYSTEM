import re
import os
from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from song import Song
from BDcontroler import BDController
from user import User
import requests
import json
import mysql.connector
from bs4 import BeautifulSoup
from playlist import Playlist

#######################################################################################################
#######################################################################################################
#######################################################################################################

# Iniciando la aplicación Flask y el manejador de sesión
app = Flask(__name__)
app.secret_key = 'ClaveSupperSegura'
login_manager = LoginManager()
login_manager.init_app(app)
letra =""

# Cargando usuario
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Rutas
@app.route('/logout')
def logout():
    session.pop('username', None)
    logout_user()
    # Redirecciona a la página de inicio de sesión u otra página de tu elección
    return redirect(url_for('index'))

@app.route("/")
def index2():
    return redirect(url_for("index"))

@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            connection = mysql.connector.connect(
                host='35.239.140.3',
                user='root',
                password='root',
                database='music-system'
            )
            cursor = connection.cursor()

            query = "SELECT COUNT(*) FROM USER WHERE USERNAME = %s AND PSWD = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result is not None and result[0] == 1:
                user = User(username)
                login_user(user)
                session['username'] = username
                connection.close()
                return redirect(url_for('buscador'))
            else:
                connection.close()
                return render_template('login.html', warnings='USER/PSWD incorrecto')
        except mysql.connector.Error as error:
            print(f'Error al conectar a la base de datos: {error}')

    return render_template('login.html', warnings='')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        subname = request.form['subname']
        email = request.form['email']
        password = request.form['key']
        password2 = request.form['key2']

        if len(password) < 8:
            return render_template('register.html', warnings='La contraseña no tiene 8 caracteres')

        if password != password2:
            return render_template('register.html', warnings='Las contraseña no coinciden')

        try:
            connection = mysql.connector.connect(
                host='35.239.140.3',
                user='root',
                password='root',
                database='music-system'
            )
            cursor = connection.cursor()

            query = "SELECT COUNT(*) FROM USER WHERE USERNAME = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result is not None and result[0] == 1:
                return render_template('register.html', warnings='¡Vaya! Ese nombre de usuario ya está en uso')

            query = "SELECT COUNT(*) FROM USER WHERE EMAIL = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if result is not None and result[0] == 1:
                return render_template('register.html', warnings='¡Vaya! Ese correo ya está en uso')

        except mysql.connector.Error as error:
            print(f'Error al conectar a la base de datos: {error}')

        try:
            db = BDController()
            db.connect()
            query = 'INSERT INTO USER (username, nombre, apellido, email, pswd) VALUES (%s, %s, %s, %s, %s)'
            params = (username, name, subname, email, password)
            db.execute_query(query, params)
            db.close()
            return redirect(url_for('login'))  # Redirigir a la página de inicio de sesión
        except mysql.connector.Error as error:
            print(f'Error al conectar a la base de datos: {error}')

    return render_template('register.html', warnings='')

@app.route('/cancion/<titulo>/<artista>', methods=['GET', 'POST'])
@login_required
def cancion(titulo, artista):
    titulo = titulo.replace('_', ' ')
    artista = artista.replace('_', ' ')
    if request.method == 'POST':
        titulo = request.form['titulo'].replace(' ', '_')
        artista = request.form['artista'].replace(' ', '_')
        return redirect(url_for('cancion', titulo=titulo, artista=artista))
    song = Song(titulo, artista)
    return render_template('song.html', nombre=song.get_titulo(), artista=song.get_artista(), album=song.get_album(), duracion=song.get_duracion(), anio=song.get_anio(), video=song.fetch_youtube_video(), letra=song.get_lyrics())

@app.route('/buscador', methods=['GET', 'POST'])
@login_required
def buscador():
    if request.method == 'POST':
        titulo = request.form['titulo'].replace(' ', '_')
        artista = request.form['artista'].replace(' ', '_')
        return redirect(url_for('cancion', titulo=titulo, artista=artista))
    return render_template('buscador.html')

@app.route('/playlist')
@login_required
def playlist():
    connection = mysql.connector.connect(
        host='35.239.140.3',
        user='root',
        password='root',
        database='music-system'
    )
    cursor = connection.cursor()
    query = "SELECT * FROM PLAYLIST WHERE USERNAME=%s"
    cursor.execute(query, (session['username'],))
    playlists_data = cursor.fetchall()

    #for playlist in playlists_data:
        #print(playlist)
        
    return render_template('playlist.html', username=session['username'], playlists=playlists_data)


@app.route('/add_playlist', methods=['GET', 'POST'])
def add_playlist():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        playlist = Playlist(session['username'],name) 
        playlist.add_playlist(description)
        return redirect(url_for('playlist'))

    return render_template('add_playlist.html')

@app.route('/add_playlist_gust', methods=['GET', 'POST'])
def add_playlist_gust():
    try:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            song_n = request.form['song_n']
            gusto = request.form['name1']
           
            if (int(song_n)>10 or int(song_n)<1):
                    return render_template('add_playlist_gust.html', warnings='Introduce un número de canciones válido')
            
            bd = BDController()
            bd.connect()

            playlist = Playlist(session['username'],name) 
            playlist.add_playlist(description)
            conjunto = playlist.inicia_sin_anios(gusto, song_n)
            print('entro')
            for cancion in conjunto:
                nombre = cancion['nombre']
                artista = cancion['artista']
                playlist.add_song(nombre,artista)
                #print(f'Nombre: {nombre}, Artista: {artista}')

            return redirect(url_for('playlist'))
    except Exception as e:
        return redirect(url_for('playlist'))
    return render_template('add_playlist_gust.html', warnings="")

@app.route('/playlist/<playlist_name>')
@login_required
def playlist_details(playlist_name):
    # Obtiene las canciones en la playlist seleccionada.
    connection = mysql.connector.connect(
        host='35.239.140.3',
        user='root',
        password='root',
        database='music-system'
    )
    cursor = connection.cursor()
    query = "SELECT * FROM SONGATPLAYLIST WHERE NAMEPLAYLIST=%s AND USERNAME=%s"
    cursor.execute(query, (playlist_name, session['username']))
    songs_data = cursor.fetchall()

    return render_template('playlist_details.html', canciones=songs_data, playlist_name=playlist_name)

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")

@app.route('/delete_playlist/<playlist_name>')
def delete_playlist(playlist_name):
    name=session['username']
    playlist = Playlist(name,playlist_name)
    playlist.elimina_playlist()
    return redirect(url_for('playlist'))


@app.route('/delete_song/<playlist_name>/<song_name>/<artist_name>')
@login_required
def delete_song(playlist_name, song_name, artist_name):
    song_name = song_name.replace('_', ' ')
    artist_name = artist_name.replace('_', ' ')
    name = session['username']
    playlist = Playlist(name, playlist_name)
    playlist.elimina_cancion_de_playlist(song_name, artist_name)
    return redirect(url_for('playlist_details', playlist_name=playlist_name))


@app.route('/playlist/<playlist_name>/add_song', methods=['POST'])
def add_song(playlist_name):
    nombre = request.form.get('nombre')
    artista = request.form.get('artista')
    name = session['username']
    playlist = Playlist(name, playlist_name)
    if playlist:
        playlist.add_song(nombre, artista)
        return redirect(url_for('playlist_details', playlist_name=playlist_name))
    
    return "No se encontró la lista de reproducción", 404


################################################################################################
################################################################################################
################################################################################################

@app.errorhandler(AttributeError)
def manejar_atributo_error(e):
    return render_template('error.html')

@app.errorhandler(401)
def page_not_found(error):
    return render_template('errorcode.html',code="404", desc="Pagina no encontrada - mejor volver"), 404

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errorcode.html',code="404", desc="Pagina no encontrada - mejor volver"), 404

@app.errorhandler(500)
def page_not_found(error):
    return render_template('errorcode.html',code="500", desc="Ocurrio un error - mejor volver"), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    