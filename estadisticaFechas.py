from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

# Definimos los rangos horarios
RANGO_MANIANA = (9.5, 14.5)  # De 8:00 a 14:30 (14.5 es 14:30)
RANGO_TARDE = (15, 20)     # De 15:00 a 20:00

def filtrar_por_horarios(archivo_txt):
    conteo = defaultdict(int)

    try:
        with open(archivo_txt, 'r', encoding='utf-8') as file:
            for linea in file:
                fecha = linea.strip()
                try:
                    # Convertir la fecha a un objeto datetime
                    dt = datetime.strptime(fecha, "%d/%m/%Y %H:%M")
                    # Obtener la hora en formato decimal (e.g., 10:30 -> 10.5)
                    hora_decimal = dt.hour + dt.minute / 60

                    # Verificar a qué rango pertenece
                    if RANGO_MANIANA[0] <= hora_decimal <= RANGO_MANIANA[1]:
                        conteo['Mañana (8:00-14:30)'] += 1
                    elif RANGO_TARDE[0] <= hora_decimal <= RANGO_TARDE[1]:
                        conteo['Tarde (15:00-20:00)'] += 1
                    else:
                        conteo['Fuera de Rango'] += 1

                except ValueError:
                    print(f"Fecha inválida: {fecha}")
    except FileNotFoundError:
        print(f"El archivo {archivo_txt} no fue encontrado.")

    return conteo

# Ruta del archivo de entrada
archivo_txt = "fechas.txt"

# Filtrar y contar las ocurrencias
conteo_horarios = filtrar_por_horarios(archivo_txt)

# Imprimir el resultado
for rango, cantidad in conteo_horarios.items():
    print(f"{rango}: {cantidad}")

# Datos de la estadística a partir del conteo
horarios = list(conteo_horarios.keys())
valores = list(conteo_horarios.values())

# Crear la gráfica de barras
plt.figure(figsize=(8, 6))
plt.bar(horarios, valores)

# Mostrar valores exactos encima de las barras
for i, valor in enumerate(valores):
    plt.text(i, valor + 5, str(valor), ha='center', va='bottom')

plt.title('Distribución por Horarios')
plt.ylabel('Cantidad')
plt.xlabel('Horario')
plt.tight_layout()

# Guardar la imagen y mostrarla
plt.savefig('estadistica_horarios.png')
plt.show()
