from googleapiclient.discovery import build
import requests
import json
from bs4 import BeautifulSoup
import re
import os

class Song:
    def __init__(self,titulo,artista):
        self.titulo=titulo
        self.artista=artista
        self.duracion=""
        self.album=""
        self.anio=""
        self.init_anio_and_album()
        self.url=self.buscar_video_youtube()
        self.letra=self.genera_letra()
    def get_url(self):
        return self.url
    def get_titulo(self):
        return self.titulo
    def get_artista(self):
        return self.artista
    
    def get_album(self):
        return self.album

    def get_anio(self):
        return self.anio

    def get_duracion(self):
        return self.duracion
        
    def get_lyrics(self):
        return self.letra
    
    def fetch_youtube_video(self):
        return self.buscar_video_youtube()

    def init_anio_and_album(self):
        entrada=self.titulo + " " + self.artista
        entrada=entrada.replace("_"," ")
        url = "https://spotify23.p.rapidapi.com/search/"
        querystring = {"q": entrada,"type":"multi","offset":"0","limit":"10","numberOfTopResults":"5"}
        headers = {
            "content-type": "application/octet-stream",
            "X-RapidAPI-Key": "fc3acc3b2amsh1281989174d218ep1307c6jsn7710d10a09d3",
            "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data=response.json()
        album=data["albums"]["items"][0]["data"]["name"]
        self.album=album
        anio=data["albums"]["items"][0]["data"]["date"]["year"]
        self.anio=anio
    def buscar_video_youtube(self):
        url = "https://youtube-search-results.p.rapidapi.com/youtube-search/"
        frase = self.titulo + " " + self.artista
        querystring = {"q": frase}
        headers = {
            "content-type": "application/octet-stream",
            "X-RapidAPI-Key": "0b03f3647emsh6ed656bfbda0b7bp1f2920jsn8f3dd2c3f62c",
            "X-RapidAPI-Host": "youtube-search-results.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        if 'items' in data:
            item0 = data["items"][0]
            url = item0["url"]
            self.duracion = item0["duration"]
            return url
        else:
            return None

        
    def genera_letra(self):
        ubi="none_ubi"
        composicion=self.titulo+" "+self.artista
        composicion = composicion.replace("_", " ")
        
        DEVELOPER_KEY = 'AIzaSyBiClX6N8cRESLv02xRtnpNLgG2bI1TEKM'
        CX = 'c5795771047404109'
        service = build('customsearch', 'v1', developerKey=DEVELOPER_KEY)
        result = service.cse().list(q='letras.com '+ composicion, cx=CX).execute()
        
        url2=result['items'][0]['link']
        print(url2)
        
        response = requests.get(url2)
        html = response.content
        # Crear un objeto BeautifulSoup con el HTML obtenido
        soup = BeautifulSoup(html, 'html.parser')
        parrafos=""
        lyrics=""
        parrafos = soup.find('div', class_='cnt-letra').find_all('p')
        for p in parrafos:
            lyrics=lyrics+p.text+"\n"
        texto_separado = re.sub(r"([a-z])([A-Z])", r"\1\n\2", lyrics)
        return texto_separado    




