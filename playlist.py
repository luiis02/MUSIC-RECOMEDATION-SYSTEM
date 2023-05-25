#canciones es un SET cuidado
class Playlist:
    def __init__(self, id, nombre, descripcion, canciones, owner,estilo,numero,explicit):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.owner = owner
        self.canciones = self.busca_estilo(estilo,numero,explicit)

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
    def inicia_con_anios(estilo,n_canciones,anio_init,anio_fin):
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
    
    
    #estilo es lo mismo que artista, es decir el usuario puede filtrar por estilos de musica o por cantantes
    def inicia_sin_anios(estilo,n_canciones):
        url = "https://chatgpt53.p.rapidapi.com/"
        promt= str(n_canciones) + " canciones de " + str(estilo) + " y simulares. Cada una con el siguiente formato: {(Nombre de canción),(nombre de artista)}"
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
    