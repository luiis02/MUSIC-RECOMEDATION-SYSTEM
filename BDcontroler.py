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
        return self.cursor.fetchall()
    
    def execute_query(self, query, params=None):
        try:
            if params is None:
                self.cursor.execute(query)
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
            self.connection.close()

