import pandas as pd
import matplotlib.pyplot as plt

# Configuración
archivo_entrada = "datos.csv"
archivo_salida = "estadisticas_llamadas_largas_turnos.csv"

# Procesar el archivo en chunks
chunksize = 100000
df_resultado = pd.DataFrame()

for chunk in pd.read_csv(
    archivo_entrada,
    chunksize=chunksize,
    sep=";",
    usecols=["Nombre Agente", "TalkingTime", "Inicio"],
    dtype={"Nombre Agente": str, "TalkingTime": str, "Inicio": str},
    low_memory=False
):
    # Convertir la columna "TalkingTime" a numérico
    chunk["TalkingTime"] = pd.to_numeric(chunk["TalkingTime"], errors="coerce")
    
    # Convertir la columna "Inicio" a formato de fecha-hora
    chunk["FechaHora"] = pd.to_datetime(chunk["Inicio"], format="%d/%m/%Y %H:%M:%S", errors="coerce", dayfirst=True)
    
    # Extraer la hora
    chunk["Hora"] = chunk["FechaHora"].dt.hour
    
    # Filtrar datos válidos
    chunk = chunk[
        (chunk["Nombre Agente"].notna()) & 
        (chunk["TalkingTime"] > 60) &  # Llamadas largas
        (chunk["FechaHora"].notna())
    ]
    
    # Crear la columna "Turno"
    chunk["Turno"] = pd.cut(
        chunk["Hora"],
        bins=[0, 9, 15, 21, 24],
        labels=["Madrugada", "Mañana", "Tarde", "Noche"],
        right=False
    )
    
    # Filtrar solo turnos válidos (mañana y tarde)
    chunk = chunk[chunk["Turno"].isin(["Mañana", "Tarde"])]
    
    # Agrupar por agente y turno
    conteo = chunk.groupby(["Nombre Agente", "Turno"], observed=False).size().reset_index(name="Llamadas Largas")
    
    # Acumular resultados en un DataFrame
    df_resultado = pd.concat([df_resultado, conteo])

# Pivotear los resultados para tener columnas separadas por turno
df_resumen = df_resultado.pivot_table(
    index="Nombre Agente",
    columns="Turno",
    values="Llamadas Largas",
    aggfunc="sum",
    fill_value=0
).reset_index()

# Renombrar las columnas para que sean más claras
df_resumen.rename(columns={"Mañana": "Llamadas Largas Mañana", "Tarde": "Llamadas Largas Tarde"}, inplace=True)

# Guardar el resultado en un archivo CSV
df_resumen.to_csv(archivo_salida, index=False, sep=";")

# Generar gráfico para Turno Mañana
df_resumen.plot(
    x="Nombre Agente",
    y="Llamadas Largas Mañana",
    kind="bar",
    figsize=(12, 6),
    color="blue"
)
plt.title("Llamadas Largas (> 1 minuto) - Turno Mañana")
plt.xlabel("Nombre Agente")
plt.ylabel("Cantidad de Llamadas")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("estadisticas_llamadas_largas_manana.png")
plt.show()

# Generar gráfico para Turno Tarde
df_resumen.plot(
    x="Nombre Agente",
    y="Llamadas Largas Tarde",
    kind="bar",
    figsize=(12, 6),
    color="orange"
)
plt.title("Llamadas Largas (> 1 minuto) - Turno Tarde")
plt.xlabel("Nombre Agente")
plt.ylabel("Cantidad de Llamadas")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("estadisticas_llamadas_largas_tarde.png")
plt.show()

print(f"Estadísticas guardadas en '{archivo_salida}' y gráficos generados en 'estadisticas_llamadas_largas_manana.png' y 'estadisticas_llamadas_largas_tarde.png'.")
