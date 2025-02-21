import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
# Configuración
archivo_entrada = "datos.csv"
archivo_salida = "estadisticas_agentes_por_dia.csv"

# Procesar el archivo en chunks
chunksize = 100000
df_resultado = pd.DataFrame()

for chunk in pd.read_csv(
    archivo_entrada,
    chunksize=chunksize,
    sep=";",
    usecols=["Nombre Agente", "Origen Corte", "Inicio"],
    dtype={"Nombre Agente": str, "Origen Corte": str, "Inicio": str},
    low_memory=False
):
    # Convertir la columna "Inicio" a formato de fecha, asegurando dayfirst=True
    chunk["Fecha"] = pd.to_datetime(chunk["Inicio"], format="%d/%m/%Y %H:%M:%S", errors="coerce", dayfirst=True).dt.strftime("%d/%m")
    
    # Filtrar datos válidos
    chunk = chunk[
        (chunk["Nombre Agente"].notna()) &
        (chunk["Origen Corte"] == "Agente") &
        (chunk["Fecha"].notna())
    ]
    
    # Agrupar por agente y día
    conteo = chunk.groupby(["Nombre Agente", "Fecha"]).size().reset_index(name="Cantidad de Cortes")
    
    # Acumular resultados en un DataFrame
    df_resultado = pd.concat([df_resultado, conteo])

# Guardar resultados finales en un CSV
df_resultado.to_csv(archivo_salida, sep=";", index=False)

print(f"Estadísticas guardadas en '{archivo_salida}'.")
