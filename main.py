import os
import shutil
import re

def detectar_encoding(ruta_archivo):
    """Intenta diferentes encodings comunes en español"""
    encodings = ['cp1252', 'latin-1', 'iso-8859-1', 'utf-8']
    
    for encoding in encodings:
        try:
            with open(ruta_archivo, 'r', encoding=encoding) as f:
                f.read()
            return encoding
        except UnicodeDecodeError:
            continue
    
    raise ValueError(f"No se pudo determinar la codificación del archivo {ruta_archivo}")

def procesar_csv(ruta_entrada, ruta_salida):
    # Crear directorio de salida si no existe
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    # Buscar todos los archivos .csv en el directorio de entrada
    archivos_csv = [f for f in os.listdir(ruta_entrada) if f.endswith('.csv')]

    for archivo in archivos_csv:
        ruta_archivo = os.path.join(ruta_entrada, archivo)

        # Crear nuevo nombre de archivo
        nombre_base = archivo[:-4]  # quitar .csv
        nuevo_nombre = f"{nombre_base}-sin-comentarios.csv"
        ruta_nuevo = os.path.join(ruta_salida, nuevo_nombre)

        try:
            # Detectar la codificación correcta
            encoding = detectar_encoding(ruta_archivo)
            print(f"Usando encoding {encoding} para {archivo}")

            # Leer el archivo original
            with open(ruta_archivo, 'r', encoding=encoding) as f:
                contenido = f.read()

            # Encontrar y eliminar el contenido entre los patrones
            patron = r'ID;Respuesta;.*?;;'
            nuevo_contenido = re.sub(patron, '', contenido, flags=re.DOTALL)

            # Guardar el nuevo archivo (mantenemos la misma codificación)
            with open(ruta_nuevo, 'w', encoding=encoding) as f:
                f.write(nuevo_contenido)

            print(f"Procesado: {archivo} -> {nuevo_nombre}")

        except Exception as e:
            print(f"Error procesando {archivo}: {str(e)}")

# Uso del script
directorio_entrada = "/home/pablo/Documentos/20250424-script-procesa-encuestas/originales"
directorio_salida = "/home/pablo/Documentos/20250424-script-procesa-encuestas/procesados"

procesar_csv(directorio_entrada, directorio_salida)