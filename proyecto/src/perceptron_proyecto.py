"""
perceptron_proyecto.py
Modelo de Inteligencia Artificial desde Cero: Perceptrón con Sigmoide y Descenso del Gradiente
Proyecto: Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago
Asignatura: Inteligencia Artificial - COTECNOVA 2026-02
Docente: Jhon James Cano Sánchez
Integrantes: Davison Cruz & Juan Diego Zapata
Entregable: Avance de Proyecto - Segundo Corte (Clases 8 y 9)
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# 1. FUNCIONES FUNDAMENTALES DEL MODELO (NUMPY PURO - SIN FRAMEWORKS)
# ==============================================================================

def sigmoide(z):
    """
    Función de activación sigmoide (mapea cualquier valor real a un rango de probabilidad [0, 1]).
    sigma(z) = 1 / (1 + e^(-z))
    """
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))

def calcular_perdida_logaritmica(y_real, y_pred, epsilon=1e-15):
    """
    Pérdida Logarítmica (Binary Cross-Entropy Loss):
    L = -1/N * sum(y * log(y_pred) + (1 - y) * log(1 - y_pred))
    Se utiliza epsilon para prevenir indeterminaciones numéricas log(0).
    """
    y_pred_segura = np.clip(y_pred, epsilon, 1.0 - epsilon)
    perdida = -np.mean(y_real * np.log(y_pred_segura) + (1.0 - y_real) * np.log(1.0 - y_pred_segura))
    return float(perdida)

# ==============================================================================
# 2. CARGA Y PREPARACIÓN DE VARIABLES PARA EL MODELO
# ==============================================================================

def cargar_y_preparar_datos(ruta_csv):
    """
    Carga el dataset y construye la matriz de características X y el vector objetivo y.
    - Variable objetivo: alta_dedicacion (1 si horas_trabajo >= mediana, 0 en caso contrario).
    - Variables de entrada: area_cm2 y madejas_hilo (escaladas con estandarización).
    """
    if not os.path.exists(ruta_csv):
        raise FileNotFoundError(f"No se encontró el dataset en la ruta: {ruta_csv}")

    df = pd.read_csv(ruta_csv)

    # Definición de la variable objetivo binaria a partir del tiempo de confección
    mediana_horas = float(df['horas_trabajo'].median())
    y = (df['horas_trabajo'] >= mediana_horas).astype(int).values

    # Variables de entrada cuantitativas conocidas antes de la confección
    # NOTA TÉCNICA: Ni 'horas_trabajo' ni 'precio_cop' se usan como variables de entrada
    # para evitar fuga de información (data leakage).
    X_crudo = df[['area_cm2', 'madejas_hilo']].values.astype(float)

    # Estandarización z-score: (X - mu) / sigma
    mu = np.mean(X_crudo, axis=0)
    sigma = np.std(X_crudo, axis=0)
    X_std = (X_crudo - mu) / sigma

    info_datos = {
        'df': df,
        'mediana_horas': mediana_horas,
        'mu': mu,
        'sigma': sigma,
        'conteo_clases': np.bincount(y)
    }

    return X_std, y, info_datos

# ==============================================================================
# 3. ENTRENAMIENTO DEL PERCEPTRÓN MEDIANTE DESCENSO DEL GRADIENTE
# ==============================================================================

def entrenar_perceptron(X, y, tasa_aprendizaje=0.1, epocas=1000, seed=42):
    """
    Entrena el perceptrón simple con función de activación sigmoide usando descenso del gradiente en lote.
    """
    np.random.seed(seed)
    n_muestras, n_caracteristicas = X.shape

    # Inicialización de pesos y sesgo (bias)
    w = np.zeros(n_caracteristicas)
    b = 0.0

    historial_perdida = []
    historial_exactitud = []

    print("=" * 70)
    print(" INICIO DE ENTRENAMIENTO: PERCEPTRÓN CON SIGMOIDE Y GRADIENTE DESCENDENTE")
    print("=" * 70)
    print(f"Parámetros iniciales: w1={w[0]:.4f}, w2={w[1]:.4f}, b={b:.4f}")
    print(f"Hiperparámetros: Tasa de aprendizaje (alpha) = {tasa_aprendizaje} | Épocas = {epocas}")
    print("-" * 70)

    for epoca in range(epocas):
        # 1. Forward Pass (Combinación lineal + Función sigmoide)
        z = np.dot(X, w) + b
        y_prob = sigmoide(z)

        # 2. Cálculo de la función de pérdida (Log Loss)
        perdida = calcular_perdida_logaritmica(y, y_prob)
        historial_perdida.append(perdida)

        # 3. Métrica de exactitud (umbral de decisión estándar = 0.5)
        predicciones = (y_prob >= 0.5).astype(int)
        exactitud = np.mean(predicciones == y) * 100.0
        historial_exactitud.append(exactitud)

        # 4. Cálculo analítico de gradientes: dL/dw = 1/N * X.T * (y_prob - y), dL/db = 1/N * sum(y_prob - y)
        error = y_prob - y
        gradiente_w = np.dot(X.T, error) / n_muestras
        gradiente_b = np.sum(error) / n_muestras

        # 5. Regla de actualización de parámetros
        w -= tasa_aprendizaje * gradiente_w
        b -= tasa_aprendizaje * gradiente_b

        # Registro de épocas clave
        if (epoca + 1) == 1 or (epoca + 1) % 200 == 0 or (epoca + 1) == epocas:
            print(f"Época {epoca + 1:4d}/{epocas} | Pérdida: {perdida:.4f} | Exactitud: {exactitud:5.1f}% | w1={w[0]:.3f}, w2={w[1]:.3f}, b={b:.3f}")

    print("=" * 70)
    print(" ENTRENAMIENTO FINALIZADO EXITOSAMENTE")
    print("=" * 70)

    return w, b, historial_perdida, historial_exactitud

# ==============================================================================
# 4. GENERACIÓN DE VISUALIZACIONES ACADÉMICAS
# ==============================================================================

def generar_graficos_modelo(X, y, w, b, historial_perdida, historial_exactitud, ruta_salida):
    """
    Genera y almacena los dos gráficos requeridos por la guía docente:
    1. Curva de aprendizaje (evolución de la pérdida logarítmica y exactitud).
    2. Frontera de decisión en el espacio bidimensional de variables estandarizadas.
    """
    os.makedirs(ruta_salida, exist_ok=True)

    # --------------------------------------------------------------------------
    # Gráfico 1: Curva de Aprendizaje (Pérdida vs Épocas)
    # --------------------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(8, 5))

    color_perdida = '#b2182b'
    ax1.set_xlabel('Época de Entrenamiento', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Pérdida Logarítmica (Binary Cross-Entropy)', color=color_perdida, fontsize=11, fontweight='bold')
    linea1 = ax1.plot(range(1, len(historial_perdida) + 1), historial_perdida, color=color_perdida, linewidth=2.2, label='Pérdida Logarítmica')
    ax1.tick_params(axis='y', labelcolor=color_perdida)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Eje secundario para la exactitud
    ax2 = ax1.twinx()
    color_acc = '#2166ac'
    ax2.set_ylabel('Exactitud (%)', color=color_acc, fontsize=11, fontweight='bold')
    linea2 = ax2.plot(range(1, len(historial_exactitud) + 1), historial_exactitud, color=color_acc, linestyle='--', linewidth=1.8, label='Exactitud (%)')
    ax2.tick_params(axis='y', labelcolor=color_acc)
    ax2.set_ylim(40, 105)

    plt.title('Curva de Aprendizaje del Perceptrón (Descenso del Gradiente)', fontsize=12, fontweight='bold', pad=12)
    fig.tight_layout()

    ruta_curva = os.path.join(ruta_salida, 'curva_aprendizaje_perceptron.png')
    plt.savefig(ruta_curva, dpi=300)
    plt.close()
    print(f"[+] Gráfica guardada: {ruta_curva}")

    # --------------------------------------------------------------------------
    # Gráfico 2: Frontera de Decisión en 2D (Área vs Madejas)
    # --------------------------------------------------------------------------
    plt.figure(figsize=(9, 6))

    # Malla para pintar regiones de probabilidad
    x_min, x_max = X[:, 0].min() - 0.7, X[:, 0].max() + 0.7
    y_min, y_max = X[:, 1].min() - 0.7, X[:, 1].max() + 0.7
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 250), np.linspace(y_min, y_max, 250))

    grid_puntos = np.c_[xx.ravel(), yy.ravel()]
    zz = sigmoide(np.dot(grid_puntos, w) + b)
    zz = zz.reshape(xx.shape)

    # Fondo sombreado de regiones de decisión (P >= 0.5)
    plt.contourf(xx, yy, zz, levels=[0.0, 0.5, 1.0], colors=['#e0f3f8', '#fee0d2'], alpha=0.65)
    contour_line = plt.contour(xx, yy, zz, levels=[0.5], colors=['#252525'], linewidths=2.5, linestyles='--')

    # Graficar las muestras de datos reales
    # Clase 0: Baja/Media Dedicación (< 29h)
    plt.scatter(X[y == 0, 0], X[y == 0, 1], color='#2166ac', edgecolor='black', s=85, label='Baja/Media Dedicación (< 29 h)', zorder=3)
    # Clase 1: Alta Dedicación (>= 29h)
    plt.scatter(X[y == 1, 0], X[y == 1, 1], color='#b2182b', edgecolor='black', s=85, marker='s', label='Alta Dedicación (≥ 29 h)', zorder=3)

    plt.title('Frontera de Decisión Lineal del Perceptrón en el Plano Estandarizado', fontsize=12, fontweight='bold', pad=12)
    plt.xlabel('Superficie del Bordado (Área cm² - Estandarizada)', fontsize=11, fontweight='bold')
    plt.ylabel('Insumo de Hilo (Madejas - Estandarizada)', fontsize=11, fontweight='bold')
    plt.grid(True, linestyle=':', alpha=0.5)

    # Anotación formal de la recta
    plt.annotate(r'Frontera: $w_1 x_1 + w_2 x_2 + b = 0$',
                 xy=(0.1, - (w[0]*0.1 + b)/w[1]),
                 xytext=(0.4, -1.2),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.2, headwidth=6),
                 fontsize=10, fontweight='bold', backgroundcolor='#ffffff')

    plt.legend(loc='upper left', framealpha=0.9)
    plt.tight_layout()

    ruta_frontera = os.path.join(ruta_salida, 'frontera_decision_perceptron.png')
    plt.savefig(ruta_frontera, dpi=300)
    plt.close()
    print(f"[+] Gráfica guardada: {ruta_frontera}")

# ==============================================================================
# 5. EJECUCIÓN PRINCIPAL Y REPORTE TÉCNICO
# ==============================================================================

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_csv = os.path.join(base_dir, '..', 'data', 'pedidos_bordados.csv')
    ruta_salida = os.path.join(base_dir, '..')

    print("=" * 70)
    print(" SISTEMA INTELIGENTE DE BORDADOS DE CARTAGO - AVANCE 2 (SEGUNDO CORTE)")
    print(" Modelo Perceptrón desde Cero con Descenso del Gradiente")
    print("=" * 70)

    # 1. Cargar y preparar
    X, y, info = cargar_y_preparar_datos(ruta_csv)
    df = info['df']

    print(f"\n[+] Total de muestras cargadas: {len(df)} pedidos representativos.")
    print(f"[+] Umbral de clasificación: Mediana de tiempo = {info['mediana_horas']:.1f} horas.")
    print(f"[+] Balance de clases: {info['conteo_clases'][0]} pedidos estándar (0) vs {info['conteo_clases'][1]} pedidos alta dedicación (1).")
    print(f"[+] Media de variables: Área = {info['mu'][0]:.1f} cm², Madejas = {info['mu'][1]:.1f}")
    print(f"[+] Desv. estándar:     Área = {info['sigma'][0]:.1f} cm², Madejas = {info['sigma'][1]:.1f}\n")

    # 2. Entrenar modelo
    w, b, hist_loss, hist_acc = entrenar_perceptron(X, y, tasa_aprendizaje=0.1, epocas=1000)

    # 3. Predicciones finales y matriz
    z_final = np.dot(X, w) + b
    prob_final = sigmoide(z_final)
    preds_finales = (prob_final >= 0.5).astype(int)
    exactitud_final = np.mean(preds_finales == y) * 100.0

    print("\n--- RESUMEN DE RESULTADOS CUANTITATIVOS ---")
    print(f"Pérdida inicial: {hist_loss[0]:.4f}")
    print(f"Pérdida final:   {hist_loss[-1]:.4f} (descenso de {hist_loss[0] - hist_loss[-1]:.4f})")
    print(f"Exactitud final: {exactitud_final:.1f}% ({np.sum(preds_finales == y)}/{len(y)} aciertos)")
    print(f"Pesos finales aprendidos: w1 (Área) = {w[0]:.4f}, w2 (Madejas) = {w[1]:.4f}, Sesgo (b) = {b:.4f}")

    print("\n--- TABLA DE EVALUACIÓN MUESTRA A MUESTRA ---")
    print(" ID | Prenda          | Técnica          | Horas | Real | Pred | Prob  | Estado")
    print("-" * 72)
    for i, fila in df.iterrows():
        estado = "ACIERTO" if preds_finales[i] == y[i] else "FALLO"
        print(f" {int(fila['id_pedido']):2d} | {fila['prenda'][:15]:15s} | {fila['tecnica'][:16]:16s} | {fila['horas_trabajo']:5.1f} |   {y[i]}  |   {preds_finales[i]}  | {prob_final[i]:.3f} | {estado}")

    # 4. Generar y almacenar figuras
    generar_graficos_modelo(X, y, w, b, hist_loss, hist_acc, ruta_salida)

    # 5. Interpretación de dominio para el informe
    print("\n" + "=" * 70)
    print(" INTERPRETACIÓN TÉCNICA Y DE DOMINIO ARTESANAL")
    print("=" * 70)
    print("1. Significado del signo de los pesos:")
    print(f"   - w1 (Área) = {w[0]:+.3f} > 0: A mayor superficie neta del bordado, se incrementa")
    print("     directamente la probabilidad de que la pieza requiera alta dedicación horaria.")
    print(f"   - w2 (Madejas) = {w[1]:+.3f} > 0: El mayor consumo de hilo es un proxy directo de")
    print("     densidad de puntadas y complejidad, aumentando también la probabilidad.")
    print("2. Separabilidad lineal:")
    print("   - Los datos en el plano bidimensional estandarizado (Área vs Madejas) muestran")
    print("     una separabilidad casi lineal para la clasificación global por mediana.")
    print("3. Limitación del modelo simple unicapa:")
    print("   - Un modelo de clasificación binaria no captura el valor continuo exacto de horas")
    print("     ni el precio final en COP. Para el objetivo final del proyecto se requiere un")
    print("     modelo de REGRESIÓN que incorpore además variables categóricas (tela y técnica).")
    print("=" * 70)

if __name__ == "__main__":
    main()
