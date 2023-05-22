import re
import os
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from song import Song
from BDcontroler import BDController
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
login_manager = LoginManager()
login_manager.init_app(app)
letra =""

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/logout')
def logout():
    logout_user()
    # Redirecciona a la página de inicio de sesión u otra página de tu elección
    return redirect(url_for('index'))
    
@app.route("/")
def index2():
    name = os.environ.get("NAME", "World")
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

@app.route("/secret")
@login_required
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

@app.route("/acerca")
def acerca():
    return render_template("acerca.html")



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
        
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    