import pandas as pd
import matplotlib.pyplot as plt

# Configuración
archivo_entrada = "datos.csv"  # Cambia al nombre del archivo CSV
archivo_salida = "estadisticas_agentes.csv"
imagen_salida = "estadisticas_agentes.png"

# Procesar el archivo en chunks
chunksize = 100000  # Tamaño del chunk
resultado = {}

for chunk in pd.read_csv(
    archivo_entrada,
    chunksize=chunksize,
    sep=";",  # Usa el separador adecuado
    usecols=["Nombre Agente", "Origen Corte"],  # Carga solo columnas relevantes
    dtype={"Nombre Agente": str, "Origen Corte": str},  # Fuerza las columnas a ser tipo string
    low_memory=False  # Previene advertencias de bajo uso de memoria
):
    # Filtrar datos según las condiciones
    chunk_filtrado = chunk[
        (chunk["Nombre Agente"].notna()) & 
        (chunk["Origen Corte"] == "Agente")
    ]
    
    # Contar las veces que cada agente aparece
    conteo = chunk_filtrado["Nombre Agente"].value_counts().to_dict()
    
    # Sumar los resultados al acumulador
    for agente, cantidad in conteo.items():
        resultado[agente] = resultado.get(agente, 0) + cantidad

# Crear DataFrame con los resultados
df_resultado = pd.DataFrame(
    {"Nombre Agente": resultado.keys(), "Cantidad de Cortes": resultado.values()}
)

# Añadir fila con el total de cortes
total_cortes = df_resultado["Cantidad de Cortes"].sum()
df_resultado = pd.concat(
    [df_resultado, pd.DataFrame({"Nombre Agente": ["Total"], "Cantidad de Cortes": [total_cortes]})],
    ignore_index=True
)

# Guardar resultados en un CSV
df_resultado.to_csv(archivo_salida, sep=";", index=False)

# Generar gráfico
plt.figure(figsize=(10, 6))
plt.bar(df_resultado["Nombre Agente"][:-1], df_resultado["Cantidad de Cortes"][:-1])
plt.title("Cortes por Agente")
plt.xlabel("Nombre Agente")
plt.ylabel("Cantidad de Cortes")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(imagen_salida)
plt.show()

print(f"Estadísticas guardadas en '{archivo_salida}' y gráfico en '{imagen_salida}'.")
