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

    def busca_estilo(parametro,n_canciones,explicit):
        canciones = set()
        url = "https://spotify23.p.rapidapi.com/search/"
        querystring = {"q":parametro,"type":"playlist","offset":"0","limit":"10","numberOfTopResults":"5"}
        headers = {
            "X-RapidAPI-Key": "0b03f3647emsh6ed656bfbda0b7bp1f2920jsn8f3dd2c3f62c",
            "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        playlists = data['playlists']['items'][:5]
        random.shuffle(playlists)

        for playlist in playlists:
            url = "https://spotify23.p.rapidapi.com/playlist_tracks/"
            playlist_id = playlist['data']['uri'].split(":")[-1]
            querystring = {"id":playlist_id,"offset":"0","limit":"100"}
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()
            tracks = data['items']
            random.shuffle(tracks)  
            for track in tracks:
                if len(canciones) >= n_canciones:
                    break 
                song = track['track']
                if not explicit and song['explicit']:
                    continue
                cancion = {}
                cancion['uri'] = song['id']
                cancion['name'] = song['name']
                if 'artists' in song and len(song['artists']) > 0:
                    cancion['artist'] = song['artists'][0]['name']
                else:
                    cancion['artist'] = 'Unknown'
                canciones.add(tuple(cancion.items()))
        return canciones