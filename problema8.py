import csv
import sqlite3
from pymongo import MongoClient

mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['tipo_cambio_db']
mongo_collection = mongo_db['sunat_info']

# Leer el archivo ventas.csv
def leer_ventas():
    ventas = []
    with open('ventas.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            ventas.append({
                'producto': row['producto'],
                'precio_dolares': float(row['precio_dolares']),
                'fecha_compra': row['fecha_compra']
            })
    return ventas

def obtener_tipo_cambio_mongodb(fecha):
   resultado = mongo_collection.find_one({'fecha': fecha})
   return resultado['venta'] if resultado else None

# Función para calcular y mostrar precios
def calcular_precios(ventas):
    print(f"{'Producto':<15} {'Precio (USD)':<15} {'Precio (S/.':<15}")
    for venta in ventas:
        fecha = venta['fecha_compra']
        obtener_tipo_cambio_mongodb(fecha) 
        
        if obtener_tipo_cambio_mongodb:
            precio_dolares = venta['precio_dolares']
            precio_soles = precio_dolares * obtener_tipo_cambio_mongodb
            print(f"{venta['producto']:<15} {precio_dolares:<15} {precio_soles:<15.2f}")
        else:
            print(f"Tipo de cambio no encontrado para la fecha: {fecha}")

# Ejecutar el proceso
ventas = leer_ventas()
calcular_precios(ventas)

# Cerrar conexiones
mongo_client.close()  # Descomenta si usas MongoDB
