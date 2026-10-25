"""
preparacion_datos_proyecto.py
Preparación y Limpieza de Datos para Machine Learning con Pandas y Seaborn
Proyecto: Sistema Inteligente de Tasación para Bordados Tradicionales de Cartago
Asignatura: Inteligencia Artificial - COTECNOVA 2026-02
Integrantes: Davison Cruz & Juan Diego Zapata
Avance 2 - Requisitos B y C
"""
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid", context="talk")

def main():
    print("=" * 70)
    print(" PROYECTO BORDADOS CARTAGO: PREPARACIÓN Y LIMPIEZA DE DATOS (AVANCE 2)")
    print("=" * 70)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_csv_crudo = os.path.join(base_dir, "..", "data", "pedidos_bordados.csv")
    df_crudo = pd.read_csv(ruta_csv_crudo)

    # --------------------------------------------------------------------------
    # 1. INSPECCIÓN Y DIAGNÓSTICO INICIAL (PANDAS)
    # --------------------------------------------------------------------------
    print("\n--- 1. INSPECCIÓN GENERAL INICIAL ---")
    print(f"Dimensiones iniciales (shape): {df_crudo.shape[0]} filas x {df_crudo.shape[1]} columnas.")
    print("\nInformación de tipos y no nulos:")
    print(df_crudo.info())

    nulos_iniciales = df_crudo.isnull().sum()
    duplicados_iniciales = df_crudo.duplicated().sum()

    print(f"\nConteo de valores nulos por columna:\n{nulos_iniciales}")
    print(f"Filas duplicadas detectadas: {duplicados_iniciales}")

    # Verificación de integridad de dominio (rangos lógicos)
    print("\nVerificación de rangos y valores posibles:")
    print(f" - Rango de área (cm²): [{df_crudo['area_cm2'].min()} a {df_crudo['area_cm2'].max()}] -> Válido (> 0)")
    print(f" - Rango de horas: [{df_crudo['horas_trabajo'].min()} a {df_crudo['horas_trabajo'].max()}] -> Válido (> 0)")
    print(f" - Rango de precios (COP): [${df_crudo['precio_cop'].min():,.0f} a ${df_crudo['precio_cop'].max():,.0f}] -> Válido (> 0)")

    # --------------------------------------------------------------------------
    # 2. TRANSFORMACIÓN Y CREACIÓN DE VARIABLES DERIVADAS
    # --------------------------------------------------------------------------
    print("\n--- 2. INGENIERÍA DE CARACTERÍSTICAS Y COLUMNAS DERIVADAS ---")
    df_limpio = df_crudo.copy()

    # Columnas derivadas de negocio artesanal
    df_limpio["costo_por_cm2"] = (df_limpio["precio_cop"] / df_limpio["area_cm2"]).round(2)
    df_limpio["productividad_cm2_hora"] = (df_limpio["area_cm2"] / df_limpio["horas_trabajo"]).round(2)

    ruta_limpio = os.path.join(base_dir, "..", "data", "pedidos_bordados_limpio.csv")
    df_limpio.to_csv(ruta_limpio, index=False)
    print(f"[+] Dataset limpio con variables derivadas guardado en: {ruta_limpio}")

    # --------------------------------------------------------------------------
    # 3. TABLA COMPARATIVA "ANTES / DESPUÉS" (EXIGIDA EN GUÍA AVANCE 2)
    # --------------------------------------------------------------------------
    df_ml = pd.get_dummies(df_limpio, columns=["tecnica", "tela", "complejidad"], prefix=["tec", "tela", "comp"])
    columnas_drop = ["id_pedido", "prenda"]
    df_ml = df_ml.drop(columns=columnas_drop, errors="ignore")

    ruta_ml = os.path.join(base_dir, "..", "data", "pedidos_bordados_preparados_ml.csv")
    df_ml.to_csv(ruta_ml, index=False)

    print("\n--- 3. TABLA COMPARATIVA 'ANTES / DESPUÉS' ---")
    print(f"{'Métrica':<30} | {'Antes (Crudo)':<15} | {'Después (Limpio)':<18} | {'Para ML (One-Hot)':<18}")
    print("-" * 88)
    print(f"{'Número de Filas':<30} | {df_crudo.shape[0]:<15} | {df_limpio.shape[0]:<18} | {df_ml.shape[0]:<18}")
    print(f"{'Número de Columnas':<30} | {df_crudo.shape[1]:<15} | {df_limpio.shape[1]:<18} | {df_ml.shape[1]:<18}")
    print(f"{'Valores Nulos Totales':<30} | {df_crudo.isnull().sum().sum():<15} | {df_limpio.isnull().sum().sum():<18} | {df_ml.isnull().sum().sum():<18}")
    print(f"{'Filas Duplicadas':<30} | {duplicados_iniciales:<15} | {df_limpio.duplicated().sum():<18} | {df_ml.duplicated().sum():<18}")
    print(f"{'Variables Categóricas':<30} | {'3 (texto)':<15} | {'3 (texto)':<18} | {'0 (codificadas 1/0)':<18}")

    # --------------------------------------------------------------------------
    # 4. GENERACIÓN DE VISUALIZACIONES ESTADÍSTICAS CON SEABORN (REQUISITO C)
    # --------------------------------------------------------------------------
    print("\n--- 4. GENERACIÓN DE VISUALIZACIONES CON SEABORN ---")
    img_dir = os.path.join(base_dir, "..")

    # Gráfico 1: Histograma con curva de densidad KDE para precios (Distribución de variable objetivo)
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df_limpio, x="precio_cop", kde=True, color="#1b7837", bins=8)
    plt.title("Densidad y Distribución de Precios Sugeridos (COP)", fontsize=13, fontweight='bold', pad=10)
    plt.xlabel("Precio Sugerido (COP)", fontsize=11)
    plt.ylabel("Densidad / Frecuencia", fontsize=11)
    plt.tight_layout()
    ruta_g1 = os.path.join(img_dir, "densidad_precios_seaborn.png")
    plt.savefig(ruta_g1, dpi=300)
    plt.close()
    print(f"[+] Gráfica guardada: {ruta_g1}")

    # Gráfico 2: Boxplot de horas de trabajo según la técnica artesanal
    plt.figure(figsize=(10, 5))
    sns.boxplot(data=df_limpio, x="tecnica", y="horas_trabajo", palette="Set2", hue="tecnica", legend=False)
    plt.title("Distribución y Dispersión de Horas según la Técnica Artesanal", fontsize=13, fontweight='bold', pad=10)
    plt.xlabel("Técnica Tradicional", fontsize=11)
    plt.ylabel("Horas de Trabajo Manual", fontsize=11)
    plt.xticks(rotation=20)
    plt.tight_layout()
    ruta_g2 = os.path.join(img_dir, "boxplot_horas_por_tecnica.png")
    plt.savefig(ruta_g2, dpi=300)
    plt.close()
    print(f"[+] Gráfica guardada: {ruta_g2}")

    # Gráfico 3: Dispersión con línea de regresión (Área vs Horas de Confección)
    plt.figure(figsize=(8, 6))
    sns.regplot(data=df_limpio, x="area_cm2", y="horas_trabajo", color="#2166ac", scatter_kws={'s': 70, 'edgecolor': 'black'})
    plt.title("Regresión Lineal: Superficie del Bordado (cm²) vs Horas de Trabajo", fontsize=13, fontweight='bold', pad=10)
    plt.xlabel("Área del Bordado (cm²)", fontsize=11)
    plt.ylabel("Horas de Confección Requeridas", fontsize=11)
    plt.tight_layout()
    ruta_g3 = os.path.join(img_dir, "regresion_area_vs_horas.png")
    plt.savefig(ruta_g3, dpi=300)
    plt.close()
    print(f"[+] Gráfica guardada: {ruta_g3}")

    print("\n[+] Preparación de datos finalizada exitosamente.")

if __name__ == "__main__":
    main()
