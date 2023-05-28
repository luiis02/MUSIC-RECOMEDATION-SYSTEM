from playlist import Playlist
import json
import re

playlist = Playlist("", "")
conjunto = playlist.inicia_sin_anios("hombres g", 10)

for cancion in conjunto:
    nombre = cancion['nombre']
    artista = cancion['artista']
    print(f'Nombre: {nombre}, Artista: {artista}')
