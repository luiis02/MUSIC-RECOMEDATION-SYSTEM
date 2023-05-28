import requests
import re
import json

#canciones es un SET cuidado
class Playlist:
    def __init__(self, id, nombre):
        self.id = id
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

    def get_canciones(self):
        return canciones

    # uri puede ser nulo
    # id tambien aunque no es recomendable
    def add_cancion(self, uri, id, name, artist):
        cancion = {}
        if uri is None and len(self.canciones) > 0:
            last_uri = self.canciones[-1]['uri']
            cancion['uri'] = None
        else:
            cancion['uri'] = uri
        cancion['id'] = id
        cancion['name'] = name
        cancion['artist'] = artist
        self.canciones.append(cancion)
   
    #estilo es lo mismo que artista, es decir el usuario puede filtrar por estilos de musica o por cantantes
    def inicia_sin_anios(self,estilo,n_canciones):
        url = "https://chatgpt53.p.rapidapi.com/"
        promt = str(n_canciones) + ' canciones de ' + str(estilo) + ''' y similares con el siguiente formato: 
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
                    "nombre": "NOMBRE DE CANCION 3",
                    "artista": "ARTISTA 3"
                },
                {
                    "nombre": "NOMBRE DE CANCION 4",
                    "artista": "ARTISTA 4"
                },
                {
                    "nombre": "NOMBRE DE CANCION 5",
                    "artista": "ARTISTA 5"
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
        resultado = re.findall(r'\[.*\]', songs_int, re.DOTALL)
        contenido_corchetes = resultado[0]
        json_data = json.loads(contenido_corchetes)
        return json_data

    