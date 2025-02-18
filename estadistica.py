import pandas as pd
import matplotlib.pyplot as plt

# Leer el archivo procesado
archivo_salida = "estadisticas_agentes_por_dia.csv"
df_resultado = pd.read_csv(archivo_salida, sep=";")

# Agrupar para eliminar duplicados y sumar las ocurrencias
df_resultado = df_resultado.groupby(["Fecha", "Nombre Agente"], as_index=False).sum()

# Gráfico 1: Barras apiladas (Cortes por día y agente)
df_pivot = df_resultado.pivot_table(index="Fecha", columns="Nombre Agente", values="Cantidad de Cortes", aggfunc="sum").fillna(0)

plt.figure(figsize=(12, 6))
df_pivot.plot(kind="bar", stacked=True, figsize=(12, 6), legend=True)
plt.title("Cortes por Día y Agente")
plt.xlabel("Fecha")
plt.ylabel("Cantidad de Cortes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("grafico_barras_apiladas.png")
plt.show()

# Gráfico 2: Líneas (Total de cortes por día)
df_totales = df_resultado.groupby("Fecha")["Cantidad de Cortes"].sum().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(df_totales["Fecha"], df_totales["Cantidad de Cortes"], marker="o")
plt.title("Total de Cortes por Día")
plt.xlabel("Fecha")
plt.ylabel("Cantidad de Cortes")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_lineas_totales.png")
plt.show()

# Gráfico 3: Barras (Cortes de un agente específico)
agente_especifico = "MZA 13"  # Cambia por el nombre del agente deseado
df_agente = df_resultado[df_resultado["Nombre Agente"] == agente_especifico]

plt.figure(figsize=(12, 6))
plt.bar(df_agente["Fecha"], df_agente["Cantidad de Cortes"])
plt.title(f"Cortes Diarios de {agente_especifico}")
plt.xlabel("Fecha")
plt.ylabel("Cantidad de Cortes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"grafico_barras_{agente_especifico}.png")
plt.show()
