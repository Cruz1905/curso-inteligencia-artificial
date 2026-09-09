"""
eda_cultivos.py
Script para realizar un Análisis Exploratorio de Datos (EDA) básico
sobre un archivo CSV de cultivos, utilizando NumPy y Matplotlib.
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
import json

def cargar_datos(archivo_csv):
    """
    Carga un archivo CSV y retorna un array de NumPy con los datos numéricos
    y una lista con los nombres de las columnas.
    """
    datos = []
    nombres_columnas = []
    try:
        with open(archivo_csv, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            nombres_columnas = next(lector)  # Leer la primera fila (encabezados)

            for fila in lector:
                # Convertir las columnas numéricas a float
                # Las columnas 1 (hectareas) y 2 (produccion) son numéricas
                hectareas = float(fila[1])
                produccion = float(fila[2])
                # Guardamos también el nombre del cultivo y la región para referencia
                datos.append([fila[0], hectareas, produccion, fila[3], fila[4]])

        print(f" Datos cargados correctamente: {len(datos)} registros.")
    except FileNotFoundError:
        print(f" Error: El archivo '{archivo_csv}' no existe.")
        return None, None, None
    except Exception as e:
        print(f" Error al leer el archivo: {e}")
        return None, None, None

    # Convertir a array de NumPy (solo las columnas numéricas para análisis)
    # Seleccionamos las columnas 1 (hectareas) y 2 (produccion)
    datos_numericos = np.array([[fila[1], fila[2]] for fila in datos], dtype=float)

    return datos_numericos, datos, nombres_columnas

def analizar_datos(datos_numericos):
    """Calcula estadísticas descriptivas de los datos numéricos."""
    if datos_numericos is None or len(datos_numericos) == 0:
        return None

    hectareas = datos_numericos[:, 0]
    produccion = datos_numericos[:, 1]

    estadisticas = {
        'hectareas': {
            'media': float(np.mean(hectareas)),
            'mediana': float(np.median(hectareas)),
            'desviacion': float(np.std(hectareas)),
            'minimo': float(np.min(hectareas)),
            'maximo': float(np.max(hectareas))
        },
        'produccion': {
            'media': float(np.mean(produccion)),
            'mediana': float(np.median(produccion)),
            'desviacion': float(np.std(produccion)),
            'minimo': float(np.min(produccion)),
            'maximo': float(np.max(produccion))
        }
    }
    return estadisticas

def generar_visualizaciones(datos_numericos, datos_completos):
    """Genera gráficos para el análisis exploratorio."""
    if datos_numericos is None or len(datos_numericos) == 0:
        return

    hectareas = datos_numericos[:, 0]
    produccion = datos_numericos[:, 1]
    nombres = [fila[0] for fila in datos_completos]  # Nombres de los cultivos

    # 1. Gráfico de barras: Hectáreas por cultivo
    plt.figure(figsize=(10, 5))
    plt.bar(nombres, hectareas, color='skyblue')
    plt.title('Hectáreas por Cultivo')
    plt.xlabel('Cultivo')
    plt.ylabel('Hectáreas')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('hectareas_por_cultivo.png')
    plt.close()

    # 2. Gráfico de dispersión: Hectáreas vs Producción
    plt.figure(figsize=(8, 6))
    plt.scatter(hectareas, produccion, color='green', alpha=0.7)
    plt.title('Relación: Hectáreas vs Producción (toneladas)')
    plt.xlabel('Hectáreas')
    plt.ylabel('Producción (toneladas)')
    plt.grid(True)
    plt.savefig('hectareas_vs_produccion.png')
    plt.close()

    # 3. Histograma: Distribución de la producción
    plt.figure(figsize=(8, 5))
    plt.hist(produccion, bins=5, color='orange', edgecolor='black')
    plt.title('Distribución de la Producción')
    plt.xlabel('Producción (toneladas)')
    plt.ylabel('Frecuencia')
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.savefig('distribucion_produccion.png')
    plt.close()

def main():
    """Función principal del programa."""
    print("=" * 50)
    print(" ANÁLISIS EXPLORATORIO DE DATOS (EDA) - CULTIVOS")
    print("=" * 50)

    # Cargar datos
    datos_numericos, datos_completos, columnas = cargar_datos('cultivos_detalle.csv')
    if datos_numericos is None:
        return

    # Analizar datos
    estadisticas = analizar_datos(datos_numericos)
    if estadisticas:
        print("\n ESTADÍSTICAS DESCRIPTIVAS:")
        print("-" * 40)
        for variable, valores in estadisticas.items():
            print(f"\n{variable.upper()}:")
            for key, value in valores.items():
                print(f"  {key.capitalize()}: {value:.2f}")

    # Guardar estadísticas en archivo de texto (Página 27 de la guía)
    with open("estadisticas.txt", "w", encoding="utf-8") as f:
        json.dump(estadisticas, f, indent=4)
    print("\n Estadísticas guardadas en 'estadisticas.txt'.")

    # Generar visualizaciones
    print("\n GENERANDO VISUALIZACIONES...")
    generar_visualizaciones(datos_numericos, datos_completos)
    print(" Visualizaciones guardadas como archivos PNG.")

    print("\n Análisis completado exitosamente.")

if __name__ == "__main__":
    main()
