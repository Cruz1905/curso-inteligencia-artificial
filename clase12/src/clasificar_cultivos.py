"""
Paso 1: comparar tres modelos de clasificación con Scikit-Learn.
Datos: cultivos_cartago.csv (los mismos de la clase del perceptrón).
Genera: matriz_confusion.png y modelo_cultivos.joblib
"""

import os
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# Definición de rutas relativas seguras
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(BASE_DIR, "..", "data", "cultivos_cartago.csv")

# 1. Cargar los datos
df = pd.read_csv(RUTA_DATOS)
X = df[["precipitacion_mm", "temperatura_c"]]  # entradas
y = df["cosecha_exitosa"]  # lo que se quiere predecir (0 o 1)

# 2. Separar los datos: 80 % para entrenar y 20 % para probar
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Lotes para entrenar: {len(X_train)} | Lotes para probar: {len(X_test)}")

# 3. Los tres modelos (cada uno escala los datos antes de aprender)
modelos = {
    "Regresión logística": Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", LogisticRegression()),
    ]),
    "KNN (5 vecinos)": Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", KNeighborsClassifier(n_neighbors=5)),
    ]),
    "Árbol de decisión": Pipeline([
        ("escalado", StandardScaler()),
        ("modelo", DecisionTreeClassifier(max_depth=3, random_state=42)),
    ]),
}

# 4. Entrenar cada modelo y medirlo con los datos de prueba
resultados = []
for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)  # aprende solo con los datos de entrenamiento
    y_pred = modelo.predict(X_test)  # predice datos que nunca vio
    resultados.append({
        "Modelo": nombre,
        "Exactitud": accuracy_score(y_test, y_pred),
        "Precisión": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1": f1_score(y_test, y_pred),
        "Val. cruzada": cross_val_score(modelo, X, y, cv=5).mean(),
    })

tabla = pd.DataFrame(resultados)
print("\nComparación de modelos (datos de prueba):")
print(tabla.round(3).to_string(index=False))

# 5. Elegir el modelo con el F1 más alto
nombre_mejor = tabla.loc[tabla["F1"].idxmax(), "Modelo"]
mejor_modelo = modelos[nombre_mejor]
print(f"\nMejor modelo según F1: {nombre_mejor}")

if nombre_mejor == "Regresión logística":
    regresion = mejor_modelo.named_steps["modelo"]
    w1, w2 = regresion.coef_[0]
    b = regresion.intercept_[0]
    print(f"Pesos aprendidos: w1 = {w1:.2f}, w2 = {w2:.2f}, b = {b:.2f}")

# 6. Matriz de confusión del mejor modelo
matriz = confusion_matrix(y_test, mejor_modelo.predict(X_test))
print("\nMatriz de confusión (filas = valor real, columnas = predicción):")
print(matriz)

plt.figure(figsize=(6, 5))
sns.heatmap(matriz, annot=True, fmt="d", cmap="Blues", cbar=False,
            xticklabels=["Predijo 0", "Predijo 1"], yticklabels=["Real 0", "Real 1"])
plt.title(f"Matriz de confusión – {nombre_mejor}")
plt.tight_layout()
ruta_matriz = os.path.join(BASE_DIR, "matriz_confusion.png")
plt.savefig(ruta_matriz, dpi=150)
plt.close()
print(f"Gráfico guardado: {ruta_matriz}")

# 7. Guardar el mejor modelo en un archivo
ruta_modelo = os.path.join(BASE_DIR, "modelo_cultivos.joblib")
joblib.dump(mejor_modelo, ruta_modelo)
print(f"Modelo guardado: {ruta_modelo}")
