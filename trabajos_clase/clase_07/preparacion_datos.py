"""
preparacion_datos.py
Script para cargar, limpiar y preparar un dataset de ventas
utilizando Pandas y visualizar con Seaborn.
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Configurar el estilo de Seaborn
sns.set_theme(style="whitegrid", context="talk")

def cargar_datos(archivo_csv):
    """Carga el archivo CSV y retorna un DataFrame."""
    try:
        df = pd.read_csv(archivo_csv)
        print(f"Datos cargados correctamente: {df.shape[0]} filas, {df.shape[1]} columnas.")
        return df
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_csv}' no existe.")
        return None

def explorar_datos(df):
    """Muestra informacion general y estadisticas descriptivas."""
    print("\nPRIMERAS 5 FILAS:")
    print(df.head())
    print("\nINFORMACION GENERAL:")
    print(df.info())
    print("\nESTADISTICAS DESCRIPTIVAS:")
    print(df.describe())
    print("\nVALORES NULOS POR COLUMNA:")
    print(df.isnull().sum())

def limpiar_datos(df):
    """Limpia el DataFrame: maneja nulos y crea columnas derivadas."""
    df_limpio = df.copy()

    # 1. Manejar valores nulos en 'cliente_edad' con la mediana
    mediana_edad = df_limpio['cliente_edad'].median()
    df_limpio['cliente_edad'] = df_limpio['cliente_edad'].fillna(mediana_edad)
    print(f"\nValores nulos en 'cliente_edad' imputados con la mediana: {mediana_edad}")

    # 2. Crear columna 'total_venta'
    df_limpio['total_venta'] = df_limpio['precio_unitario'] * df_limpio['cantidad']
    print("Columna 'total_venta' creada.")

    return df_limpio

def visualizar_datos(df, ruta_salida="."):
    """Genera visualizaciones con Seaborn."""
    os.makedirs(ruta_salida, exist_ok=True)

    # 1. Distribucion del total de ventas
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x='total_venta', bins=10, kde=True, color='skyblue')
    plt.title('Distribucion del Total de Ventas')
    plt.xlabel('Total de Venta ($)')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, 'distribucion_ventas.png'), dpi=150)
    plt.close()
    print("Grafico guardado: distribucion_ventas.png")

    # 2. Total de ventas por categoria
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='categoria', y='total_venta', estimator=np.sum, errorbar=None, palette='viridis')
    plt.title('Total de Ventas por Categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Total de Ventas ($)')
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, 'ventas_por_categoria.png'), dpi=150)
    plt.close()
    print("Grafico guardado: ventas_por_categoria.png")

    # 3. Relacion entre edad y total de venta
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='cliente_edad', y='total_venta', hue='categoria', style='metodo_pago', s=100)
    plt.title('Relacion: Edad del Cliente vs Total de Venta')
    plt.xlabel('Edad del Cliente')
    plt.ylabel('Total de Venta ($)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, 'edad_vs_venta.png'), dpi=150)
    plt.close()
    print("Grafico guardado: edad_vs_venta.png")

def preparar_ml(df):
    """Prepara el DataFrame para Machine Learning: codificacion y seleccion."""
    df_ml = df.copy()

    # 1. Codificacion One-Hot para 'categoria' y 'metodo_pago'
    df_ml = pd.get_dummies(df_ml, columns=['categoria', 'metodo_pago'], prefix=['cat', 'pago'])
    print("\nCodificacion One-Hot aplicada.")

    # 2. Eliminar columnas no numericas irrelevantes para el modelo
    columnas_a_eliminar = ['id_venta', 'fecha', 'producto', 'ciudad']
    df_ml = df_ml.drop(columns=columnas_a_eliminar, errors='ignore')
    print("Columnas no numericas eliminadas.")

    # 3. Mostrar las primeras filas del DataFrame listo para ML
    print("\nDATAFRAME LISTO PARA MACHINE LEARNING (primeras 5 filas):")
    print(df_ml.head())

    return df_ml

def main():
    """Funcion principal del programa."""
    print("=" * 60)
    print("PREPARACION DE DATOS PARA MACHINE LEARNING - VENTAS")
    print("=" * 60)

    ruta_csv = os.path.join(os.path.dirname(__file__), 'ventas_tienda.csv')
    if not os.path.exists(ruta_csv):
        ruta_csv = 'ventas_tienda.csv'

    df = cargar_datos(ruta_csv)
    if df is None:
        return

    explorar_datos(df)
    df_limpio = limpiar_datos(df)
    carpeta_salida = os.path.dirname(ruta_csv) if os.path.dirname(ruta_csv) else "."
    visualizar_datos(df_limpio, carpeta_salida)
    df_ml = preparar_ml(df_limpio)

    ruta_guardado = os.path.join(carpeta_salida, 'ventas_preparadas_ml.csv')
    df_ml.to_csv(ruta_guardado, index=False)
    print(f"\nDataset preparado guardado como '{ruta_guardado}'")
    print("\nProceso completado exitosamente.")

if __name__ == "__main__":
    main()
