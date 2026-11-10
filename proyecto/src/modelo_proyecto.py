"""
modelo_proyecto.py
Modelo Final de Machine Learning con Scikit-Learn
Proyecto: Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago
Asignatura: Inteligencia Artificial - COTECNOVA 2026-02
Docente: Jhon James Cano Sánchez
Estudiantes: Davison Cruz López & Juan Diego Zapata Arbeláez (Grupo 02)
Clase 12: Entrenamiento, Evaluación, Selección y Guardado de Modelos
"""

import os
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, mean_absolute_error,
                             mean_squared_error, r2_score)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROYECTO_DIR = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(PROYECTO_DIR, "data", "pedidos_bordados_limpio.csv")

def cargar_y_preparar_datos():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"No se encontró el dataset en: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    # Variable objetivo de clasificación: Alta Dedicación (horas >= mediana)
    mediana_horas = float(df['horas_trabajo'].median())
    df['alta_dedicacion'] = (df['horas_trabajo'] >= mediana_horas).astype(int)
    
    return df, mediana_horas

def entrenar_modelos_clasificacion(df):
    print("=" * 80)
    print(" 1. CLASIFICACIÓN: ALTA DEDICACIÓN HORARIA (0 = Estándar, 1 = Alta Dedicación)")
    print("=" * 80)
    
    # Variables de entrada para el modelo
    X = df[['area_cm2', 'madejas_hilo']]
    y = df['alta_dedicacion']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Muestras de entrenamiento: {len(X_train)} | Muestras de prueba: {len(X_test)}")
    
    modelos = {
        "Regresión Logística": Pipeline([
            ("escalado", StandardScaler()),
            ("modelo", LogisticRegression(random_state=42))
        ]),
        "KNN (3 vecinos)": Pipeline([
            ("escalado", StandardScaler()),
            ("modelo", KNeighborsClassifier(n_neighbors=3))
        ]),
        "Árbol de Decisión": Pipeline([
            ("escalado", StandardScaler()),
            ("modelo", DecisionTreeClassifier(max_depth=3, random_state=42))
        ]),
        "Red Neuronal (MLP)": Pipeline([
            ("escalado", StandardScaler()),
            ("modelo", MLPClassifier(hidden_layer_sizes=(8, 4), max_iter=1500, random_state=42))
        ])
    }
    
    resultados = []
    for nombre, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        resultados.append({
            "Modelo": nombre,
            "Exactitud": accuracy_score(y_test, y_pred),
            "Precisión": precision_score(y_test, y_pred, zero_division=0),
            "Recall": recall_score(y_test, y_pred, zero_division=0),
            "F1-Score": f1_score(y_test, y_pred, zero_division=0),
            "Val. Cruzada (k=5)": cross_val_score(modelo, X, y, cv=5).mean()
        })
        
    tabla = pd.DataFrame(resultados)
    print("\nComparación de Modelos de Clasificación en Datos de Prueba:")
    print(tabla.round(3).to_string(index=False))
    
    nombre_mejor = tabla.loc[tabla["F1-Score"].idxmax(), "Modelo"]
    mejor_modelo = modelos[nombre_mejor]
    print(f"\n[+] Mejor Modelo de Clasificación (según F1-Score): {nombre_mejor}")
    
    # Matriz de confusión
    y_pred_test = mejor_modelo.predict(X_test)
    matriz = confusion_matrix(y_test, y_pred_test)
    print("\nMatriz de Confusión en Prueba:")
    print(matriz)
    
    plt.figure(figsize=(6, 5))
    sns.heatmap(matriz, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["Predijo Estándar", "Predijo Alta"],
                yticklabels=["Real Estándar", "Real Alta"])
    plt.title(f"Matriz de Confusión - {nombre_mejor}")
    plt.tight_layout()
    ruta_cm = os.path.join(PROYECTO_DIR, "matriz_confusion_proyecto.png")
    plt.savefig(ruta_cm, dpi=200)
    plt.close()
    print(f"[+] Gráfico guardado: {ruta_cm}")
    
    # Guardar modelo
    ruta_joblib = os.path.join(BASE_DIR, "modelo_clasificacion_bordados.joblib")
    joblib.dump(mejor_modelo, ruta_joblib)
    print(f"[+] Modelo de clasificación guardado en: {ruta_joblib}")
    
    return mejor_modelo

def entrenar_modelos_regresion(df):
    print("\n" + "=" * 80)
    print(" 2. REGRESIÓN: ESTIMACIÓN NUMÉRICA CONTINUA DE TIEMPO (HORAS DE TRABAJO)")
    print("=" * 80)
    
    # Variables explicativas cuantitativas
    entradas = ['area_cm2', 'madejas_hilo']
    X = df[entradas]
    y = df['horas_trabajo']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    modelos_reg = {
        "Regresión Lineal": Pipeline([
            ("escalado", StandardScaler()),
            ("modelo", LinearRegression())
        ]),
        "Ridge": Pipeline([
            ("escalado", StandardScaler()),
            ("modelo", Ridge(alpha=1.0, random_state=42))
        ]),
        "KNN Regressor": Pipeline([
            ("escalado", StandardScaler()),
            ("modelo", KNeighborsRegressor(n_neighbors=3))
        ]),
        "Árbol de Regresión": Pipeline([
            ("escalado", StandardScaler()),
            ("modelo", DecisionTreeRegressor(max_depth=3, random_state=42))
        ])
    }
    
    resultados_reg = []
    for nombre, modelo in modelos_reg.items():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        resultados_reg.append({
            "Modelo": nombre,
            "MAE (horas)": mae,
            "RMSE (horas)": rmse,
            "R²": r2
        })
        
    tabla_reg = pd.DataFrame(resultados_reg)
    print("\nComparación de Modelos de Regresión en Datos de Prueba:")
    print(tabla_reg.round(3).to_string(index=False))
    
    nombre_mejor_reg = tabla_reg.loc[tabla_reg["R²"].idxmax(), "Modelo"]
    mejor_modelo_reg = modelos_reg[nombre_mejor_reg]
    print(f"\n[+] Mejor Modelo de Regresión (según R²): {nombre_mejor_reg}")
    
    # Gráfico Real vs Predicho
    y_pred_reg = mejor_modelo_reg.predict(X_test)
    plt.figure(figsize=(7, 6))
    plt.scatter(y_test, y_pred_reg, color="navy", edgecolors="black", s=80, alpha=0.9)
    minimo, maximo = min(y_test.min(), y_pred_reg.min()), max(y_test.max(), y_pred_reg.max())
    plt.plot([minimo, maximo], [minimo, maximo], color="red", linestyle="--", label="Predicción Ideal")
    plt.title(f"Regresión: Horas Reales vs Estimadas ({nombre_mejor_reg})")
    plt.xlabel("Horas de Trabajo Reales")
    plt.ylabel("Horas de Trabajo Estimadas")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    ruta_reg_plot = os.path.join(PROYECTO_DIR, "real_vs_predicho_proyecto.png")
    plt.savefig(ruta_reg_plot, dpi=200)
    plt.close()
    print(f"[+] Gráfico guardado: {ruta_reg_plot}")
    
    # Guardar modelo de regresión
    ruta_reg_joblib = os.path.join(BASE_DIR, "modelo_regresion_bordados.joblib")
    joblib.dump(mejor_modelo_reg, ruta_reg_joblib)
    print(f"[+] Modelo de regresión guardado en: {ruta_reg_joblib}")
    
    return mejor_modelo_reg

def main():
    print("=" * 80)
    print(" SISTEMA INTELIGENTE DE BORDADOS DE CARTAGO - MODELO FINAL (CLASE 12)")
    print("=" * 80)
    
    df, mediana_horas = cargar_y_preparar_datos()
    print(f"[+] Dataset cargado: {len(df)} piezas bordadas artesanales.")
    print(f"[+] Umbral de Alta Dedicación: {mediana_horas:.1f} horas.\n")
    
    entrenar_modelos_clasificacion(df)
    entrenar_modelos_regresion(df)
    
    print("\n" + "=" * 80)
    print(" ENTRENAMIENTO, EVALUACIÓN Y PERSISTENCIA COMPLETADOS EXITOSAMENTE")
    print("=" * 80)

if __name__ == "__main__":
    main()
