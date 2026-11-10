"""
Paso 5: ver el sobreajuste.
Un árbol de decisión muy profundo memoriza los datos de entrenamiento,
pero no mejora con los datos de prueba.
Genera: sobreajuste_arbol.png
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(BASE_DIR, "..", "data", "cultivos_cartago.csv")

df = pd.read_csv(RUTA_DATOS)
X = df[["precipitacion_mm", "temperatura_c"]]
y = df["cosecha_exitosa"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Entrenar árboles cada vez más profundos y medir en entrenamiento y en prueba
filas = []
for profundidad in range(1, 13):
    arbol = DecisionTreeClassifier(max_depth=profundidad, random_state=42)
    arbol.fit(X_train, y_train)
    filas.append({
        "Profundidad": profundidad,
        "Entrenamiento": arbol.score(X_train, y_train),
        "Prueba": arbol.score(X_test, y_test),
    })

tabla = pd.DataFrame(filas)
print(tabla.round(3).to_string(index=False))

plt.figure(figsize=(8, 5))
plt.plot(tabla["Profundidad"], tabla["Entrenamiento"], marker="o", label="Entrenamiento")
plt.plot(tabla["Profundidad"], tabla["Prueba"], marker="s", label="Prueba")
plt.title("Sobreajuste: exactitud según la profundidad del árbol")
plt.xlabel("Profundidad del árbol (max_depth)")
plt.ylabel("Exactitud")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
ruta_grafico = os.path.join(BASE_DIR, "sobreajuste_arbol.png")
plt.savefig(ruta_grafico, dpi=150)
plt.close()
print(f"\nGráfico guardado: {ruta_grafico}")
