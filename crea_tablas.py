import mysql.connector

# Crea una conexión a la base de datos
connection = mysql.connector.connect(
    host='35.239.140.3',
    user='root',
    password='root',
    database='music-system'
)

# Crea un cursor
cursor = connection.cursor()


cursor.execute("SHOW TABLES")
print(cursor.fetchall())
# Define la consulta para crear la tabla PLAYLIST
create_table_playlist = """
CREATE TABLE PLAYLIST(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NAMEPLAYLIST VARCHAR(32) NOT NULL,
    USERNAME VARCHAR(12) NOT NULL,
    DESCRIPCION TEXT,
    EXPLICITSONG BOOLEAN NOT NULL,
    CONSTRAINT UC_NAME_USERNAME UNIQUE (NAMEPLAYLIST, USERNAME)
);
"""

cursor.execute(create_table_playlist)

# Define la consulta para crear la tabla SONGATPLAYLIST
create_table_songatplaylist = """
CREATE TABLE SONGATPLAYLIST(
    NOMBRE VARCHAR(32) NOT NULL,
    ARTISTA VARCHAR(32) NOT NULL,
    NAMEPLAYLIST VARCHAR(32) NOT NULL,
    USERNAME VARCHAR(12) NOT NULL,
    EXPLICITSONG BOOLEAN,
    CONSTRAINT UC_NOMBRE_ARTISTA_PLAYLIST UNIQUE (NOMBRE, ARTISTA, NAMEPLAYLIST, USERNAME)
);
"""
cursor.execute(create_table_songatplaylist)


    
# Confirma los cambios
connection.commit()

# Cierra la conexión
cursor.close()
connection.close()
