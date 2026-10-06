"""
neurona_and.py
Implementacion de una neurona artificial simple (Perceptron) para aprender la compuerta AND.
Clase 8: ¿Como Aprende una IA? Pesos, Neuronas y Error.
Asignatura: Inteligencia Artificial - COTECNOVA 2026.
Docente: Jhon James Cano Sanchez.
Estudiante: Davison Cruz.
"""
import matplotlib.pyplot as plt
import os

# ============================================================
# 1. Definir la funcion de activacion (escalon)
# ============================================================
def escalon(z):
    """Funcion de activacion escalon (Step Function)."""
    return 1 if z >= 0 else 0

# ============================================================
# 2. Definir la neurona
# ============================================================
def neurona(x1, x2, w1, w2, b):
    """Calcula la salida de la neurona a partir de la suma ponderada."""
    z = w1 * x1 + w2 * x2 + b
    return escalon(z)

# ============================================================
# 3. Datos de entrenamiento (Compuerta AND)
# ============================================================
# (x1, x2, y_real)
datos = [
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 0),
    (1, 1, 1),
]

# ============================================================
# 4. Parametros iniciales
# Usamos w1=0.1, w2=0.1, b=0.0 para visualizar la evolucion del aprendizaje
# ============================================================
w1 = 0.1
w2 = 0.1
b = 0.0
tasa_aprendizaje = 0.1  # alpha
max_epocas = 15

errores_por_epoca = []

print("=" * 60)
print("ENTRENAMIENTO DE UNA NEURONA PARA LA COMPUERTA AND")
print("=" * 60)
print(f"Parametros iniciales: w1={w1:.3f}, w2={w2:.3f}, b={b:.3f}")
print(f"Tasa de aprendizaje (alpha): {tasa_aprendizaje}\n")

# ============================================================
# 5. Bucle de Entrenamiento (Ajuste de Pesos y Bias)
# ============================================================
for epoca in range(max_epocas):
    error_total = 0
    print(f"--- Epoca {epoca + 1} ---")
    
    for x1, x2, y_real in datos:
        # 1. Prediccion (Forward Pass)
        y_pred = neurona(x1, x2, w1, w2, b)
        
        # 2. Calculo del error
        error = y_real - y_pred
        error_total += abs(error)
        
        # 3. Ajuste de pesos y bias (Regla de Aprendizaje del Perceptron)
        w1 += tasa_aprendizaje * error * x1
        w2 += tasa_aprendizaje * error * x2
        b += tasa_aprendizaje * error
        
        print(f"  Entrada: ({x1}, {x2}) | Real: {y_real} | Pred: {y_pred} | Error: {error:+d}")
    
    errores_por_epoca.append(error_total)
    print(f"  Error total en epoca: {error_total}")
    print(f"  Parametros actuales: w1={w1:.3f}, w2={w2:.3f}, b={b:.3f}\n")
    
    if error_total == 0:
        print(f"[OK] La neurona aprendio exitosamente en {epoca + 1} epocas.\n")
        break

# ============================================================
# 6. Prueba Final
# ============================================================
print("=" * 60)
print("PRUEBA FINAL DE LA COMPUERTA AND")
print("=" * 60)
for x1, x2, y_real in datos:
    y_pred = neurona(x1, x2, w1, w2, b)
    estado = "CORRECTO" if y_pred == y_real else "FALLO"
    print(f"  [{estado}] Entrada: ({x1}, {x2}) | Esperado: {y_real} | Predicho: {y_pred}")

print(f"\nPesos finales aprendidos: w1={w1:.3f}, w2={w2:.3f}, bias={b:.3f}")

# ============================================================
# 7. Graficar y Guardar la Evolucion del Error
# ============================================================
ruta_dir = os.path.dirname(os.path.abspath(__file__))
plt.figure(figsize=(8, 5))
plt.plot(range(1, len(errores_por_epoca) + 1), errores_por_epoca, marker='o', color='#b2182b', linewidth=2)
plt.title('Evolucion del Error durante el Entrenamiento - Compuerta AND', fontsize=12, fontweight='bold')
plt.xlabel('Epoca', fontsize=10)
plt.ylabel('Error Total', fontsize=10)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
ruta_grafico = os.path.join(ruta_dir, 'evolucion_error_and.png')
plt.savefig(ruta_grafico, dpi=150)
plt.close()
print(f"Grafico guardado: {ruta_grafico}")
