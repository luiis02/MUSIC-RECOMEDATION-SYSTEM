import mysql.connector

host = '35.239.140.3'
user = 'root'
password = 'root'
database = 'music-system'

try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    cursor = connection.cursor()

    # Datos para la inserción
    username = 'ejemplo'
    name = 'John'
    subname = 'Doe'
    email = 'johndoe@example.com'
    password = 'secretpassword'

    query = 'INSERT INTO USER (username, nombre, apellido, email, pswd) VALUES (%s, %s, %s, %s, %s)'
    params = (username, name, subname, email, password)

    cursor.execute(query, params)
    connection.commit()

    print('Inserción exitosa')

except mysql.connector.Error as error:
    print(f'Error al conectar a la base de datos: {error}')

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print('Conexión cerrada')

