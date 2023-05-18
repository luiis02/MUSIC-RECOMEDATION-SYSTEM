import re
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from song import Song
from BDcontroler import BDcontroler
from user import User
import requests
import json
import mysql.connector
from bs4 import BeautifulSoup

#######################################################################################################
#######################################################################################################
#######################################################################################################

app = Flask(__name__)
app.secret_key = 'ClaveSupperSegura'
letra =""
@app.route("/")
def index2():
    name = os.environ.get("NAME", "World")
    return redirect(url_for("index"))

@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/cancion/<titulo>/<artista>', methods=['GET', 'POST'])
def cancion(titulo, artista):
    titulo = titulo.replace('_', ' ')
    artista = artista.replace('_', ' ')
    if request.method == 'POST':
        titulo = request.form['titulo'].replace(' ', '_')
        artista = request.form['artista'].replace(' ', '_')
        return redirect(url_for('cancion', titulo=titulo, artista=artista))
    song = Song(titulo, artista)
    global letra
    letra = song.get_lyrics()
    return render_template('song.html', nombre=song.get_titulo(), artista=song.get_artista(), album=song.get_album(), duracion=song.get_duracion(), anio=song.get_anio(), video=song.fetch_youtube_video())

@app.route('/buscador', methods=['GET', 'POST'])
def buscador():
    if request.method == 'POST':
        titulo = request.form['titulo'].replace(' ', '_')
        artista = request.form['artista'].replace(' ', '_')
        return redirect(url_for('cancion', titulo=titulo, artista=artista))
    return render_template('buscador.html')

@app.route("/lyrics")
def imprime_lyrics():
    global letra
    return render_template('lyrics.html', lyrics=letra)

@app.route("/secret")
def muestra():
    db = BDcontroler()

    db.connect()

    # Ejecutar una consulta
    results = db.execute_query("SHOW TABLES")

    # Almacenar los resultados en una lista
    rows = []
    for row in results:
        rows.append(row)

    # Cerrar la conexión
    db.close()

    # Retornar la lista completa de resultados
    return rows
login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'root' and password == '123':
            user = User(username)
            login_user(user)
            return redirect(url_for('protected_page'))
        else:
            return 'Credenciales inválidas'

    return render_template('login.html')

@app.route('/protected')
@login_required
def protected_page():
    return 'Esta es una página protegida. Solo los usuarios autenticados pueden acceder a ella.'


################################################################################################
################################################################################################
################################################################################################

@app.errorhandler(AttributeError)
def manejar_atributo_error(e):
    return render_template('error.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errorcode.html',code="404", desc="Pagina no encontrada - mejor volver"), 404
        
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    