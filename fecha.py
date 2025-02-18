import pandas as pd

# Configuración
archivo_entrada = "datos.csv"

# Procesar el archivo en chunks para manejar grandes volúmenes de datos
chunksize = 100000
fecha_min = None
fecha_max = None

for chunk in pd.read_csv(
    archivo_entrada,
    chunksize=chunksize,
    sep=";",
    usecols=["Inicio"],
    dtype={"Inicio": str},
    low_memory=False
):
    # Convertir la columna "Inicio" a formato de fecha
    chunk["Inicio"] = pd.to_datetime(chunk["Inicio"], format="%d/%m/%Y %H:%M:%S", errors="coerce", dayfirst=True)
    
    # Obtener la fecha mínima y máxima del chunk
    min_chunk = chunk["Inicio"].min()
    max_chunk = chunk["Inicio"].max()
    
    # Actualizar la fecha mínima y máxima global
    if fecha_min is None or (min_chunk is not pd.NaT and min_chunk < fecha_min):
        fecha_min = min_chunk
    if fecha_max is None or (max_chunk is not pd.NaT and max_chunk > fecha_max):
        fecha_max = max_chunk

# Mostrar los resultados
if fecha_min and fecha_max:
    print(f"La fecha más antigua en los datos es: {fecha_min.strftime('%d/%m/%Y')}")
    print(f"La fecha más reciente en los datos es: {fecha_max.strftime('%d/%m/%Y')}")
else:
    print("No se encontraron fechas válidas en los datos.")
