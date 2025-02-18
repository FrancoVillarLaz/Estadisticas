import pandas as pd
import matplotlib.pyplot as plt

# Configuración
archivo_entrada = "datos.csv"
archivo_salida = "estadisticas_agentes_turnos.csv"

# Lista de agentes permitidos
agentes_filtrados = [
    "MZA 33", "MZA 34", "MZA 35", "MZA 15", "MZA 16", "MZA 18", "MZA 19", 
    "MZA 20", "MZA 21", "MZA 22", "MZA 31", "MZA 12", "MZA 13", "MZA 14", 
    "MZA 41", "MZA 42", "MZA 43", "MZA 48", "MZA 49", "MZA 50"
]

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
    # Filtrar solo los agentes permitidos
    chunk = chunk[chunk["Nombre Agente"].isin(agentes_filtrados)]
    
    # Convertir la columna "Inicio" a formato de fecha-hora
    chunk["FechaHora"] = pd.to_datetime(chunk["Inicio"], format="%d/%m/%Y %H:%M:%S", errors="coerce", dayfirst=True)
    
    # Extraer la hora
    chunk["Hora"] = chunk["FechaHora"].dt.hour
    
    # Filtrar datos válidos
    chunk = chunk[
        (chunk["Nombre Agente"].notna()) & 
        (chunk["Origen Corte"] == "Agente") & 
        (chunk["FechaHora"].notna())
    ]
    
    # Crear la columna "Turno"
    chunk = chunk[chunk["Hora"].notna()]  # Eliminar filas donde "Hora" sea NaN
    chunk["Turno"] = pd.cut(
        chunk["Hora"],
        bins=[0, 9, 15, 21, 24],
        labels=["Madrugada", "Mañana", "Tarde", "Noche"],
        right=False
    )
    
    # Filtrar solo turnos válidos (mañana y tarde)
    chunk = chunk[chunk["Turno"].isin(["Mañana", "Tarde"])]
    
    # Agrupar por agente y turno
    conteo = chunk.groupby(["Nombre Agente", "Turno"], observed=False).size().reset_index(name="Cantidad de Cortes")
    
    # Acumular resultados en un DataFrame
    df_resultado = pd.concat([df_resultado, conteo])

# Pivotear los resultados para obtener una columna para cada turno (mañana y tarde)
df_resumen = df_resultado.pivot_table(
    index="Nombre Agente",
    columns="Turno",
    values="Cantidad de Cortes",
    aggfunc="sum",
    fill_value=0
).reset_index()

# Renombrar las columnas para que sean más claras
df_resumen.rename(columns={"Mañana": "Cortes Turno Mañana", "Tarde": "Cortes Turno Tarde"}, inplace=True)

# Guardar el resultado en un archivo CSV
df_resumen.to_csv(archivo_salida, index=False, sep=";")

# Generar gráfico para Turno Mañana
df_resumen.plot(
    x="Nombre Agente",
    kind="bar",
    figsize=(12, 6),
    y="Cortes Turno Mañana",
    color="blue",
    stacked=False
)
plt.title("Cantidad de Cortes - Turno Mañana")
plt.xlabel("Nombre Agente")
plt.ylabel("Cantidad de Cortes")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("estadisticas_agentes_turno_manana.png")
plt.show()

# Generar gráfico para Turno Tarde
df_resumen.plot(
    x="Nombre Agente",
    kind="bar",
    figsize=(12, 6),
    y="Cortes Turno Tarde",
    color="orange",
    stacked=False
)
plt.title("Cantidad de Cortes - Turno Tarde")
plt.xlabel("Nombre Agente")
plt.ylabel("Cantidad de Cortes")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("estadisticas_agentes_turno_tarde.png")
plt.show()

print(f"Estadísticas guardadas en '{archivo_salida}' y gráficos generados en 'estadisticas_agentes_turno_manana.png' y 'estadisticas_agentes_turno_tarde.png'.")
