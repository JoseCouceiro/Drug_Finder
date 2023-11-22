import sqlite3
from sqlite3 import Error

"""Este módulo establece las conexión con la base de datos mediante la función "create_conection" y envía las instrucciones usando la función execute_querty(). Es código reciclado de clase"""

#def Crear conexión

def create_connection(path):
    try:
        connection = sqlite3.connect(path)
        print("Connection stablished. Generating database in 'outputs' folder")
    except Error as e:
        pass
        print(f"Error : '{e}'")

    return connection

#def Ejecutar consulta DDL
def execute_query(connection,query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        pass
        print(f"Error: '{e}'")
