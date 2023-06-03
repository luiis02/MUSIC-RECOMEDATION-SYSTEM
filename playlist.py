import requests
import re
import json
from BDcontroler import BDController
class Playlist:
    def __init__(self, username, nombre):
        self.username = username
        self.nombre = nombre

    def get_owner(self):
        return self.owner

    def rename(self, new_name):
        self.nombre = new_name

    def get_name(self):
        return self.name

    def change_description(self, new_description):
        self.descripcion = new_description

    def get_descripcion(self):
        return self.descripcion


    #estilo es lo mismo que artista, es decir el usuario puede filtrar por estilos de musica o por cantantes
    def inicia_sin_anios(self,estilo,n_canciones):
        url = "https://chatgpt53.p.rapidapi.com/"
        promt = 'Recomiendame exactamente' + str(n_canciones) + ' canciones de ' + str(estilo) + ''' y similares con el siguiente formato: 
            {
            "canciones": [
                {
                    "nombre": "NOMBRE DE CANCION 1",
                    "artista": "ARTISTA 1"
                },
                {
                    "nombre": "NOMBRE DE CANCION 2",
                    "artista": "ARTISTA 2"
                },
                {
                    "nombre": "NOMBRE DE CANCION N",
                    "artista": "ARTISTA N"
                }
            ]
        }'''
        payload = { "messages": [
            {
                "role": "user",
                "content": promt
            }
        ] }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "fc3acc3b2amsh1281989174d218ep1307c6jsn7710d10a09d3",
            "X-RapidAPI-Host": "chatgpt53.p.rapidapi.com"
        }
        response = requests.post(url, json=payload, headers=headers)
        data=response.json()
        songs_int=data['choices'][0]['message']['content']
        songs_int=str(songs_int)
        print(songs_int)
        resultado = re.findall(r'\[.*\]', songs_int, re.DOTALL)
        contenido_corchetes = resultado[0]
        json_data = json.loads(contenido_corchetes)
        return json_data

    def elimina_playlist(self):
        db = BDController()
        db.connect()
        query = 'SELECT nombre, artista FROM SONGATPLAYLIST WHERE username=%s AND nameplaylist=%s'
        params = (self.username, self.nombre)
        results = db.execute_select(query, params)
        for result in results:
            nombre = result['nombre']
            artista = result['artista']
            db.eliminaCanciones(self.nombre, self.username,nombre,artista)
        db.eliminaPlaylist(self.nombre, self.username)

    def elimina_cancion_de_playlist(self, song_name, artist_name):
        bd_controller = BDController()
        bd_controller.connect()
        query = 'DELETE FROM SONGATPLAYLIST WHERE username=%s AND nameplaylist=%s AND nombre=%s AND artista=%s'
        params = (self.username, self.nombre, song_name, artist_name)
        bd_controller.execute_query(query, params)
        bd_controller.close()

    def add_playlist(self, description):
        bd_controller = BDController()
        bd_controller.connect()
        bd_controller.insertaPlaylist(self.nombre, self.username, description)
        bd_controller.close()
        
    def add_song(self, nombre,art):
        bd_controller = BDController()
        bd_controller.connect()
        bd_controller.insertaSong(nombre,art,self.nombre, self.username)
        bd_controller.close()
