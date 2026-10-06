"""
neuronas_logicas.py
Implementación de neuronas artificiales para las compuertas lógicas OR y NOT.
Actividad Independiente - Clase 8: Pesos, Neuronas y Error.
Asignatura: Inteligencia Artificial - COTECNOVA 2026.
Docente: Jhon James Cano Sánchez.
Estudiante: Davison Cruz.
"""
import matplotlib.pyplot as plt
import os

def escalon(z):
    """Función de activación escalón."""
    return 1 if z >= 0 else 0

def entrenar_compuerta_or():
    print("=" * 60)
    print("1. ENTRENAMIENTO DE LA COMPUERTA OR")
    print("=" * 60)
    
    # (x1, x2, y_esperado)
    datos = [
        (0, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 1),
    ]
    
    w1, w2, b = 0.0, 0.0, 0.0
    tasa = 0.1
    max_epocas = 15
    errores = []
    
    print(f"Parámetros iniciales: w1={w1:.2f}, w2={w2:.2f}, b={b:.2f} | Tasa={tasa}\n")
    
    for epoca in range(max_epocas):
        error_total = 0
        for x1, x2, y_real in datos:
            z = w1 * x1 + w2 * x2 + b
            y_pred = escalon(z)
            error = y_real - y_pred
            error_total += abs(error)
            
            # Ajuste de pesos
            w1 += tasa * error * x1
            w2 += tasa * error * x2
            b += tasa * error
            
        errores.append(error_total)
        print(f"Época {epoca + 1:2d} -> Error Total: {error_total} | w1={w1:.2f}, w2={w2:.2f}, b={b:.2f}")
        
        if error_total == 0:
            print(f"[OK] Compuerta OR convergió en {epoca + 1} épocas.\n")
            break
            
    print("Prueba Final OR:")
    for x1, x2, y_real in datos:
        pred = escalon(w1 * x1 + w2 * x2 + b)
        print(f"  Entrada: ({x1}, {x2}) | Esperado: {y_real} | Predicho: {pred}")
        
    return errores

def entrenar_compuerta_not():
    print("\n" + "=" * 60)
    print("2. ENTRENAMIENTO DE LA COMPUERTA NOT (1 Entrada)")
    print("=" * 60)
    
    # (x, y_esperado)
    datos = [
        (0, 1),
        (1, 0),
    ]
    
    w, b = 0.0, 0.0
    tasa = 0.1
    max_epocas = 15
    errores = []
    
    print(f"Parámetros iniciales: w={w:.2f}, b={b:.2f} | Tasa={tasa}\n")
    
    for epoca in range(max_epocas):
        error_total = 0
        for x, y_real in datos:
            z = w * x + b
            y_pred = escalon(z)
            error = y_real - y_pred
            error_total += abs(error)
            
            # Ajuste de peso y bias
            w += tasa * error * x
            b += tasa * error
            
        errores.append(error_total)
        print(f"Época {epoca + 1:2d} -> Error Total: {error_total} | w={w:.2f}, b={b:.2f}")
        
        if error_total == 0:
            print(f"[OK] Compuerta NOT convergió en {epoca + 1} épocas.\n")
            break
            
    print("Prueba Final NOT:")
    for x, y_real in datos:
        pred = escalon(w * x + b)
        print(f"  Entrada: ({x}) | Esperado: {y_real} | Predicho: {pred}")
        
    return errores

def main():
    errores_or = entrenar_compuerta_or()
    errores_not = entrenar_compuerta_not()
    
    # Guardar gráficas de evolución del error
    ruta_dir = os.path.dirname(os.path.abspath(__file__))
    
    plt.figure(figsize=(10, 4))
    
    # Subplot OR
    plt.subplot(1, 2, 1)
    plt.plot(range(1, len(errores_or) + 1), errores_or, marker='o', color='#2166ac', linewidth=2)
    plt.title('Evolución Error - Compuerta OR', fontweight='bold')
    plt.xlabel('Época')
    plt.ylabel('Error Total')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Subplot NOT
    plt.subplot(1, 2, 2)
    plt.plot(range(1, len(errores_not) + 1), errores_not, marker='s', color='#1b7837', linewidth=2)
    plt.title('Evolución Error - Compuerta NOT', fontweight='bold')
    plt.xlabel('Época')
    plt.ylabel('Error Total')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    ruta_img = os.path.join(ruta_dir, 'evolucion_error_or_not.png')
    plt.savefig(ruta_img, dpi=150)
    plt.close()
    print(f"\n[+] Gráfica comparativa guardada en: {ruta_img}")

if __name__ == "__main__":
    main()
