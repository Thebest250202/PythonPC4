import requests
import sqlite3
from pymongo import MongoClient
from datetime import datetime, timedelta

# Configuración de la conexión a MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')  # Cambia la URI si es necesario
mongo_db = mongo_client['tipo_cambio_db']
mongo_collection = mongo_db['sunat_info']

# Crear conexión a SQLite
sqlite_conn = sqlite3.connect('base.db')
sqlite_cursor = sqlite_conn.cursor()

# Crear tabla en SQLite
sqlite_cursor.execute('''
CREATE TABLE IF NOT EXISTS sunat_info (
    fecha TEXT PRIMARY KEY,
    compra REAL,
    venta REAL
)
''')

# Función para obtener datos del API de SUNAT
def obtener_precio_dolar():
    url = 'https://api.apis.net.pe/v1/tipo-cambio-sunat'
    headers = {'Content-Type': 'application/json'}

    # Lista para almacenar los datos
    datos = []

    # Obtener datos desde el 1 de enero hasta el 31 de diciembre de 2023
    fecha_inicio = datetime(2023, 1, 1)
    fecha_fin = datetime(2023, 12, 31)

    for n in range((fecha_fin - fecha_inicio).days + 1):
        fecha = (fecha_inicio + timedelta(n)).strftime('%Y-%m-%d')
        response = requests.get(f"{url}/{fecha}", headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                compra = data['data']['compra']
                venta = data['data']['venta']
                datos.append((fecha, compra, venta))
                # Insertar en MongoDB
                mongo_collection.insert_one({'fecha': fecha, 'compra': compra, 'venta': venta})
            else:
                print(f"No se encontraron datos para la fecha: {fecha}")
        else:
            print(f"Error al obtener datos para la fecha: {fecha}")

    return datos

# Obtener datos y almacenarlos
datos_dolar = obtener_precio_dolar()

# Insertar datos en SQLite
sqlite_cursor.executemany('INSERT OR REPLACE INTO sunat_info (fecha, compra, venta) VALUES (?, ?, ?)', datos_dolar)
sqlite_conn.commit()

# Mostrar contenido de la tabla en SQLite
sqlite_cursor.execute('SELECT * FROM sunat_info')
resultados = sqlite_cursor.fetchall()

print("Contenido de la tabla sunat_info:")
for fila in resultados:
    print(f"Fecha: {fila[0]}, Compra: {fila[1]}, Venta: {fila[2]}")

# Cerrar conexiones
sqlite_cursor.close()
sqlite_conn.close()
mongo_client.close()
