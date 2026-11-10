"""
usar_modelo.py
Demostración de Inferencia en Tiempo Real para la Sustentación Final
Proyecto: Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago
Asignatura: Inteligencia Artificial - COTECNOVA 2026-02
Docente: Jhon James Cano Sánchez
Estudiantes: Davison Cruz López & Juan Diego Zapata Arbeláez (Grupo 02)
"""

import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_MODELO_CLF = os.path.join(BASE_DIR, "modelo_clasificacion_bordados.joblib")
RUTA_MODELO_REG = os.path.join(BASE_DIR, "modelo_regresion_bordados.joblib")

def main():
    print("=" * 85)
    print(" SISTEMA INTELIGENTE DE BORDADOS DE CARTAGO - DEMOSTRACIÓN DE PREDICCIÓN")
    print(" Carga de Modelos Entrenados con Scikit-Learn (Sin reentrenar)")
    print("=" * 85)
    
    if not os.path.exists(RUTA_MODELO_CLF) or not os.path.exists(RUTA_MODELO_REG):
        raise FileNotFoundError("Los modelos .joblib no existen. Ejecute primero src/modelo_proyecto.py")
        
    # 1. Cargar modelos serializados (Pipeline con escalador incluido)
    modelo_clf = joblib.load(RUTA_MODELO_CLF)
    modelo_reg = joblib.load(RUTA_MODELO_REG)
    print("[+] Modelos de Clasificación y Regresión cargados exitosamente.\n")
    
    # 2. Casos nuevos realistas para la sustentación
    casos_nuevos = pd.DataFrame([
        {
            "descripcion": "Guayabera de Gala (Lino + Calado Fino)",
            "area_cm2": 400.0,
            "madejas_hilo": 5.0,
        },
        {
            "descripcion": "Pañuelo Delicado (Algodón + Pata de Cabra)",
            "area_cm2": 100.0,
            "madejas_hilo": 1.0,
        },
        {
            "descripcion": "Mantel Imperial (Lino + Rococó Complejo)",
            "area_cm2": 1050.0,
            "madejas_hilo": 12.0,
        }
    ])
    
    X_nuevos = casos_nuevos[["area_cm2", "madejas_hilo"]]
    
    # 3. Predicciones con los modelos
    probs_alta = modelo_clf.predict_proba(X_nuevos)[:, 1]
    preds_clase = modelo_clf.predict(X_nuevos)
    horas_estimadas = modelo_reg.predict(X_nuevos)
    
    # Tarifa de referencia artesanal por hora (~ $7.500 COP base mano de obra)
    COSTO_HORA_COP = 7500
    VALOR_MADEJA_COP = 3500
    VALOR_TELA_BASE = 40000
    precios_sugeridos = (horas_estimadas * COSTO_HORA_COP) + (casos_nuevos["madejas_hilo"] * VALOR_MADEJA_COP) + VALOR_TELA_BASE
    
    # 4. Formatear reporte
    casos_nuevos["Prob_Alta_%"] = (probs_alta * 100).round(1)
    casos_nuevos["Clasificacion"] = ["Alta Dedicación" if p == 1 else "Estándar" for p in preds_clase]
    casos_nuevos["Horas_Estimadas"] = horas_estimadas.round(1)
    casos_nuevos["Precio_Sugerido_COP"] = [f"${int(round(pr, -3)):,}" for pr in precios_sugeridos]
    
    print("--- RESULTADOS DE INFERENCIA EN TIEMPO REAL ---")
    columnas_mostrar = ["descripcion", "area_cm2", "madejas_hilo", "Prob_Alta_%", "Clasificacion", "Horas_Estimadas", "Precio_Sugerido_COP"]
    print(casos_nuevos[columnas_mostrar].to_string(index=False))
    
    print("\n" + "=" * 85)
    print(" DEMOSTRACIÓN COMPLETADA: Listos para responder consultas en la sustentación final.")
    print("=" * 85)

if __name__ == "__main__":
    main()
