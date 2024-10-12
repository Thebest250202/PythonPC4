import os

def contar_lineas_codigo(ruta_archivo):
    # Verificar si el archivo tiene la extensión .py
    if not ruta_archivo.endswith('.py'):
        return  # No se retorna nada si la extensión no es .py

    # Verificar si la ruta es válida
    if not os.path.isfile(ruta_archivo):
        return  # No se retorna nada si la ruta no es válida

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()  # Leer todas las líneas del archivo
            contador_lineas = 0
            
            for linea in lineas:
                linea = linea.strip()  # Eliminar espacios en blanco al inicio y al final
                # Excluir líneas en blanco y comentarios
                if linea and not linea.startswith('#'):
                    contador_lineas += 1
            
            print(f"Cantidad de líneas de código (sin comentarios ni líneas en blanco): {contador_lineas}")
    
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

# Solicitar la ruta del archivo al usuario
ruta = input("Ingrese la ruta del archivo .py: ")
contar_lineas_codigo(ruta)
