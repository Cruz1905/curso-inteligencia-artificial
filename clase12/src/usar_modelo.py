"""
Paso 2: usar el modelo guardado para predecir lotes nuevos.
No se entrena nada: solo se carga el archivo y se predice.
"""

import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_modelo = os.path.join(BASE_DIR, "modelo_cultivos.joblib")

# 1. Cargar el modelo guardado en el Paso 1 (ya incluye el escalado)
modelo = joblib.load(ruta_modelo)

# 2. Lotes nuevos (mismos nombres de columna que en el entrenamiento)
lotes_nuevos = pd.DataFrame({
    "precipitacion_mm": [220.0, 60.0, 150.0],
    "temperatura_c": [23.5, 30.0, 26.0],
})

# 3. Predecir la probabilidad de éxito y la clase (0 o 1)
probabilidad = modelo.predict_proba(lotes_nuevos)[:, 1]
prediccion = modelo.predict(lotes_nuevos)

lotes_nuevos["probabilidad_exito_%"] = (probabilidad * 100).round(1)
lotes_nuevos["resultado"] = ["Exitosa" if p == 1 else "No exitosa" for p in prediccion]

print("Predicciones con el modelo guardado:")
print(lotes_nuevos.to_string(index=False))
