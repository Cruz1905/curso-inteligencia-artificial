"""
Paso 3: regresión lineal, es decir, predecir un NÚMERO (rendimiento en kg/ha)
en lugar de una clase 0/1.
Los datos son simulados (con rangos realistas para Cartago) y se generan aquí mismo.
Genera: ../data/rendimiento_cartago.csv y real_vs_predicho.png
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_DATOS = os.path.join(BASE_DIR, "..", "data", "rendimiento_cartago.csv")

# 1. Crear los datos (la semilla hace que siempre salgan iguales)
generador = np.random.default_rng(seed=7)
n = 150
df = pd.DataFrame({
    "precipitacion_mm": generador.uniform(40, 260, n).round(1),
    "temperatura_c": generador.uniform(21, 31, n).round(1),
    "fertilizante_kg_ha": generador.uniform(50, 300, n).round(0),
})
df["rendimiento_kg_ha"] = (
    2000
    + 6.0 * df["precipitacion_mm"]
    - 90.0 * (df["temperatura_c"] - 26)
    + 3.0 * df["fertilizante_kg_ha"]
    + generador.normal(0, 180, n)
).round(0)

os.makedirs(os.path.dirname(RUTA_DATOS), exist_ok=True)
df.to_csv(RUTA_DATOS, index=False)
print("Primeros datos:")
print(df.head())
print(f"\nRendimiento promedio: {df['rendimiento_kg_ha'].mean():.0f} kg/ha")

# 2. Entradas, salida y separación entrenamiento/prueba
entradas = ["precipitacion_mm", "temperatura_c", "fertilizante_kg_ha"]
X = df[entradas]
y = df["rendimiento_kg_ha"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Entrenar la regresión lineal
modelo = Pipeline([
    ("escalado", StandardScaler()),
    ("modelo", LinearRegression()),
])
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

# 4. Medir el error con los datos de prueba
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print("\nMétricas con los datos de prueba:")
print(f"MAE = {mae:.1f} kg/ha")
print(f"RMSE = {rmse:.1f} kg/ha")
print(f"R² = {r2:.3f}")

# 5. ¿Cuánto pesa cada variable?
regresion = modelo.named_steps["modelo"]
print("\nEfecto de cada variable (al subir una desviación estándar):")
for nombre, coef in zip(entradas, regresion.coef_):
    print(f"  {nombre}: {coef:+.1f} kg/ha")

# 6. Gráfico: valor real contra valor predicho
plt.figure(figsize=(7, 6))
plt.scatter(y_test, y_pred, color="teal", edgecolors="black")
minimo, maximo = y.min(), y.max()
plt.plot([minimo, maximo], [minimo, maximo], color="red", linestyle="--",
         label="Predicción perfecta")
plt.title(f"Regresión lineal: real vs. predicho (R² = {r2:.2f})")
plt.xlabel("Rendimiento real (kg/ha)")
plt.ylabel("Rendimiento predicho (kg/ha)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
ruta_grafico = os.path.join(BASE_DIR, "real_vs_predicho.png")
plt.savefig(ruta_grafico, dpi=150)
plt.close()
print(f"\nGráfico guardado: {ruta_grafico}")
