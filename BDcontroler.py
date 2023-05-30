import mysql.connector

class BDController:
    def __init__(self):
        self.host = '35.239.140.3'
        self.user = 'root'
        self.password = 'root'
        self.database = 'music-system'
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def execute_select(self, query, params=None):
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        
        column_names = [column[0] for column in self.cursor.description]
        results = []
        
        for row in self.cursor.fetchall():
            results.append(dict(zip(column_names, row)))
        
        return results
    
    def execute_query(self, query, params=None):
        try:
            if params is None:
                self.cursor.execute(query)
                self.connection.commit()
            else:
                self.cursor.execute(query, params)
                self.connection.commit()
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f'Error al ejecutar la consulta: {error}')

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.commit()  # Realizar commit antes de cerrar la conexión
            self.connection.close()

    def insertaPlaylist(self, name,username,description):
        connection = mysql.connector.connect(
            host='35.239.140.3',
            user='root',
            password='root',
            database='music-system'
        )

        cursor = connection.cursor()
        query = "INSERT INTO PLAYLIST (NAMEPLAYLIST, USERNAME, DESCRIPCION) VALUES (%s, %s ,%s)"
        cursor.execute(query, (name, username, description))
        connection.commit()

    def insertaSong(self, nom,art,nomp,username):
        connection = mysql.connector.connect(
            host='35.239.140.3',
            user='root',
            password='root',
            database='music-system'
        )

        cursor = connection.cursor()
        query = "INSERT INTO SONGATPLAYLIST (NOMBRE, ARTISTA,NAMEPLAYLIST, USERNAME, EXPLICITSONG) VALUES (%s, %s ,%s, %s, 0)"
        cursor.execute(query, (nom, art, nomp, username))
        print("ole tu")
        connection.commit()

    def eliminaPlaylist(self, nombre,username):
        connection = mysql.connector.connect(
            host='35.239.140.3',
            user='root',
            password='root',
            database='music-system'
        )
        cursor = connection.cursor()
        query = 'DELETE FROM PLAYLIST WHERE username=%s AND nameplaylist=%s'
        params = (username, nombre)
        cursor.execute(query, params)
        connection.commit()
    
    def eliminaCanciones(self, nombre,username, cancion,artista):
        connection = mysql.connector.connect(
            host='35.239.140.3',
            user='root',
            password='root',
            database='music-system'
        )
        cursor = connection.cursor()
        query = 'DELETE FROM SONGATPLAYLIST WHERE username=%s AND nameplaylist=%s AND nombre=%s AND artista=%s'
        params = (username, nombre, cancion, artista)
        cursor.execute(query, params)
        connection.commit()