import pandas as pd
import matplotlib.pyplot as plt

# Rutas de entrada y salida
archivo_csv = 'archivo.csv'
estadistica_mensual = 'estadistica_mensual.csv'
estadistica_diaria = 'estadistica_diaria.csv'
grafico_mensual = 'estadistica_mensual.png'
grafico_diario = 'estadistica_diaria.png'

# Rango horario
MANIANA = (9, 14.5)  # 14.5 representa 14:30
TARDE = (15, 20)

def detectar_columnas(archivo):
    """Detecta los encabezados reales del archivo."""
    try:
        with open(archivo, 'r', encoding='utf-8-sig') as file:
            encabezados = file.readline().strip().split(';')
        return encabezados
    except Exception as e:
        raise ValueError(f"No se pudieron detectar los encabezados: {e}")

def cargar_datos(archivo):
    """Carga el CSV seleccionando dinámicamente las columnas necesarias."""
    encabezados = detectar_columnas(archivo)
    columna_inicio = next((col for col in encabezados if 'Inicio' in col), None)
    columna_origen = next((col for col in encabezados if 'Origen Corte' in col), None)
    columna_tipificacion = next((col for col in encabezados if 'Tipificación' in col), None)

    if not columna_inicio or not columna_origen or not columna_tipificacion:
        raise ValueError(f"Las columnas necesarias no fueron encontradas. Encabezados detectados: {encabezados}")

    try:
        df = pd.read_csv(
            archivo, 
            delimiter=';', 
            usecols=[columna_inicio, columna_origen, columna_tipificacion], 
            encoding='utf-8-sig'
        )
        df.rename(columns={
            columna_inicio: 'Inicio',
            columna_origen: 'Origen Corte',
            columna_tipificacion: 'Tipificación'
        }, inplace=True)

        # Convertir la columna 'Inicio' al formato correcto
        df['Inicio'] = pd.to_datetime(df['Inicio'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

        # Filtrar registros inválidos
        registros_invalidos = df[df['Inicio'].isna()]
        if not registros_invalidos.empty:
            print(f"Registros con fechas inválidas: {len(registros_invalidos)}")
            print(registros_invalidos)

        # Filtrar solo datos de diciembre
        df = df.dropna(subset=['Inicio'])
        df = df[df['Inicio'].dt.month == 12]

        # Excluir filas con tipificación "No Disp."
        df = df[df['Tipificación'].str.strip().str.lower() != 'no disp.']

        return df
    except Exception as e:
        raise ValueError(f"Error al cargar el archivo: {e}")

def categorizar_horario(hora):
    """Categoriza la hora en mañana o tarde."""
    hora_decimal = hora.hour + hora.minute / 60
    if MANIANA[0] <= hora_decimal <= MANIANA[1]:
        return 'Mañana'
    elif TARDE[0] <= hora_decimal <= TARDE[1]:
        return 'Tarde'
    else:
        return 'Fuera de horario'

def calcular_estadisticas(df):
    """Calcula las estadísticas requeridas."""
    # Filtrar solo los cortes realizados por "Agente"
    df = df[df['Origen Corte'].str.strip().str.lower() == 'agente']

    # Crear columna de horario (Mañana o Tarde)
    df['Horario'] = df['Inicio'].apply(lambda x: categorizar_horario(x))

    # Estadística mensual
    df['Mes'] = df['Inicio'].dt.to_period('M')
    mensual = df.groupby(['Mes']).Horario.value_counts().unstack(fill_value=0).reset_index()
    mensual.rename(columns={'Mañana': 'Cantidad Mañana', 'Tarde': 'Cantidad Tarde'}, inplace=True)

    # Estadística diaria
    df['Fecha'] = df['Inicio'].dt.date
    diaria = df.groupby(['Fecha']).Horario.value_counts().unstack(fill_value=0).reset_index()
    diaria.rename(columns={'Mañana': 'Cantidad Mañana', 'Tarde': 'Cantidad Tarde'}, inplace=True)

    return mensual, diaria

def agregar_valores_inicio_por_color(ax):
    """Agrega valores al inicio de cada color (segmento) en las barras."""
    for p in ax.patches:
        x = p.get_x() + p.get_width() / 2.
        y = p.get_y()  # Posición inicial del segmento
        height = p.get_height()  # Altura del segmento

        if height > 0:  # Mostrar solo para valores positivos
            ax.annotate(f'{int(height)}', 
                        (x, y), 
                        ha='center', va='bottom', fontsize=10, color='black', xytext=(0, -5), 
                        textcoords='offset points')

def generar_graficos(df_mensual, df_diario):
    """Genera gráficos de estadísticas mensuales y diarias con valores anotados."""
    # Gráfico mensual
    plt.figure(figsize=(10, 6))
    ax = df_mensual.plot(x='Mes', y=['Cantidad Mañana', 'Cantidad Tarde'], kind='bar', stacked=True, legend=True)
    agregar_valores_inicio_por_color(ax)
    plt.title('Estadísticas Mensuales por Horario')
    plt.ylabel('Cantidad')
    plt.xlabel('Mes')
    plt.tight_layout()
    plt.savefig(grafico_mensual)
    print(f"Gráfico mensual guardado en: {grafico_mensual}")

    # Gráfico diario
    plt.figure(figsize=(12, 8))
    ax = df_diario.plot(x='Fecha', y=['Cantidad Mañana', 'Cantidad Tarde'], kind='bar', stacked=True, legend=True)
    agregar_valores_inicio_por_color(ax)
    plt.title('Estadísticas Diarias por Horario')
    plt.ylabel('Cantidad')
    plt.xlabel('Fecha')
    plt.tight_layout()
    plt.savefig(grafico_diario)
    print(f"Gráfico diario guardado en: {grafico_diario}")

def guardar_estadisticas(df_mensual, df_diario):
    """Guarda las estadísticas en archivos CSV delimitados por ';'."""
    df_mensual.to_csv(estadistica_mensual, index=False, sep=';', encoding='utf-8-sig')
    df_diario.to_csv(estadistica_diaria, index=False, sep=';', encoding='utf-8-sig')

def main():
    """Ejecución principal del script."""
    try:
        print("Cargando datos...")
        datos = cargar_datos(archivo_csv)

        print("Calculando estadísticas...")
        estadistica_mensual, estadistica_diaria = calcular_estadisticas(datos)

        print("Guardando estadísticas...")
        guardar_estadisticas(estadistica_mensual, estadistica_diaria)

        print("Generando gráficos...")
        generar_graficos(estadistica_mensual, estadistica_diaria)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
