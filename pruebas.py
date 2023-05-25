import requests
import re
url = "https://chatgpt53.p.rapidapi.com/"
n_canciones=8
estilo="hombres g"
anio_init=1960
anio_fin=1990
promt= str(n_canciones) + " canciones de " + str(estilo) + " y simulares desde " + str(anio_init) + " hasta " + str(anio_fin) + ". Cada una con el siguiente formato: {(Nombre de canción),(nombre de artista)}"
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
filas = songs_int.splitlines()
vector=[]
for fila in filas:
    fila=str(fila)
    if("," in fila):
        partes = fila.split(", ")
    elif("-" in fila):
        partes = fila.split("- ")

    parte1 = partes[0]
    parte2 = partes[1]

    posicion = 0

    posiciones_comillas = []
    while True:
        posicion = parte1.find('"', posicion)
        if posicion == -1:
            break
        posiciones_comillas.append(posicion)
        posicion += 1
    parte1=parte1[(posiciones_comillas[0]+1):posiciones_comillas[1]]
    vector.append([parte1,parte2])
    print(parte1+","+parte2)
    
