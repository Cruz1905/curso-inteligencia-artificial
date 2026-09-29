"""
preparacion_datos_proyecto.py
Actividad Complementaria Clase 8: Pandas, Seaborn y Preparacion ML
Proyecto: Sistema Inteligente de Tasacion para Bordados Tradicionales de Cartago
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

sns.set_theme(style="whitegrid", context="talk")

def main():
    print("=" * 65)
    print(" PROYECTO BORDADOS: PREPARACION DE DATOS CON PANDAS Y SEABORN")
    print("=" * 65)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(base_dir, "..", "data", "pedidos_bordados.csv")
    df = pd.read_csv(ruta_csv)

    print("\n--- 1. EXPLORACION GENERAL CON PANDAS ---")
    print(df.info())
    print("\nVALORES NULOS:")
    print(df.isnull().sum())

    print("\n--- 2. LIMPIEZA Y COLUMNAS DERIVADAS ---")
    # Columna derivada: costo por cm2 y rendimiento artesanal
    df["costo_por_cm2"] = (df["precio_cop"] / df["area_cm2"]).round(2)
    df["productividad_cm2_hora"] = (df["area_cm2"] / df["horas_trabajo"]).round(2)
    print("Columnas derivadas 'costo_por_cm2' y 'productividad_cm2_hora' creadas con exito.")

    print("\n--- 3. GENERACION DE VISUALIZACIONES CON SEABORN ---")
    img_dir = os.path.join(base_dir, "..")

    # Grafica 1: Histograma con curva de densidad KDE para precios
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="precio_cop", kde=True, color="#1b7837", bins=8)
    plt.title("Densidad y Distribucion de Precios Sugeridos (COP)")
    plt.xlabel("Precio Sugerido (COP)")
    plt.ylabel("Densidad / Frecuencia")
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, "densidad_precios_seaborn.png"), dpi=150)
    plt.close()
    print("Grafica guardada: densidad_precios_seaborn.png")

    # Grafica 2: Boxplot de horas de trabajo segun la tecnica artesanal
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df, x="tecnica", y="horas_trabajo", palette="Set2")
    plt.title("Distribucion y Dispersión de Horas por Técnica")
    plt.xlabel("Técnica Artesanal")
    plt.ylabel("Horas de Trabajo")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, "boxplot_horas_por_tecnica.png"), dpi=150)
    plt.close()
    print("Grafica guardada: boxplot_horas_por_tecnica.png")

    # Grafica 3: Dispersion con linea de regresion lineal (Area vs Horas)
    plt.figure(figsize=(8, 6))
    sns.regplot(data=df, x="area_cm2", y="horas_trabajo", color="#2166ac", scatter_kws={'s': 60})
    plt.title("Regresión Lineal: Área (cm²) vs Horas de Trabajo")
    plt.xlabel("Área del Bordado (cm²)")
    plt.ylabel("Horas de Confección")
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, "regresion_area_vs_horas.png"), dpi=150)
    plt.close()
    print("Grafica guardada: regresion_area_vs_horas.png")

    print("\n--- 4. CODIFICACION ONE-HOT PARA MACHINE LEARNING ---")
    df_ml = pd.get_dummies(df, columns=["tecnica", "tela", "complejidad"], prefix=["tec", "tela", "comp"])
    columnas_drop = ["id_pedido", "prenda"]
    df_ml = df_ml.drop(columns=columnas_drop, errors="ignore")

    ruta_ml = os.path.join(base_dir, "..", "data", "pedidos_bordados_preparados_ml.csv")
    df_ml.to_csv(ruta_ml, index=False)
    print(f"Dataset listo para ML guardado en: {ruta_ml}")
    print(f"Dimensiones finales: {df_ml.shape[0]} filas x {df_ml.shape[1]} columnas.")

if __name__ == "__main__":
    main()
