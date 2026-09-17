"""
eda_proyecto.py
Proyecto: Sistema Inteligente de Tasación para Bordados Tradicionales de Cartago
Asignatura: Inteligencia Artificial - COTECNOVA
Integrantes: Davison Cruz y Juan Diego Zapata
"""
import csv
import os
import numpy as np
import matplotlib.pyplot as plt

def cargar_pedidos(archivo_csv):
    """
    Carga el dataset de pedidos de bordado, retornando:
    - lista_pedidos: Lista de diccionarios con la informacion completa procesada.
    - datos_numericos: Array NumPy con columnas [area_cm2, madejas_hilo, horas_trabajo, precio_cop].
    """
    lista_pedidos = []
    if not os.path.exists(archivo_csv):
        print(f"Error: El archivo {archivo_csv} no existe.")
        return None, None

    with open(archivo_csv, mode="r", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            pedido = {
                "id": int(fila["id_pedido"]),
                "prenda": fila["prenda"],
                "tecnica": fila["tecnica"],
                "tela": fila["tela"],
                "area_cm2": float(fila["area_cm2"]),
                "complejidad": fila["complejidad"],
                "madejas_hilo": int(fila["madejas_hilo"]),
                "horas_trabajo": float(fila["horas_trabajo"]),
                "precio_cop": float(fila["precio_cop"])
            }
            # Agregamos calculo derivado con funcion propia
            pedido["rendimiento_cm2_hora"] = calcular_rendimiento(pedido["area_cm2"], pedido["horas_trabajo"])
            lista_pedidos.append(pedido)

    # Convertimos a matriz NumPy para el analisis matematico
    datos_numericos = np.array([
        [p["area_cm2"], p["madejas_hilo"], p["horas_trabajo"], p["precio_cop"]]
        for p in lista_pedidos
    ], dtype=float)

    return lista_pedidos, datos_numericos

def calcular_rendimiento(area, horas):
    """
    Funcion propia de dominio: Calcula los cm2 bordados por cada hora de trabajo artesanal.
    """
    if horas <= 0:
        return 0.0
    return round(area / horas, 2)

def analizar_con_numpy(datos_numericos):
    """
    Calcula estadisticas descriptivas con NumPy para horas y precio.
    """
    horas = datos_numericos[:, 2]
    precios = datos_numericos[:, 3]

    estadisticas = {
        "horas": {
            "promedio": float(np.mean(horas)),
            "mediana": float(np.median(horas)),
            "desviacion_std": float(np.std(horas)),
            "minimo": float(np.min(horas)),
            "maximo": float(np.max(horas))
        },
        "precios": {
            "promedio": float(np.mean(precios)),
            "mediana": float(np.median(precios)),
            "desviacion_std": float(np.std(precios)),
            "minimo": float(np.min(precios)),
            "maximo": float(np.max(precios))
        }
    }
    return estadisticas

def generar_visualizaciones(lista_pedidos, datos_numericos, ruta_salida="."):
    """
    Genera y guarda visualizaciones claras con Matplotlib para la sustentacion.
    """
    os.makedirs(ruta_salida, exist_ok=True)
    areas = datos_numericos[:, 0]
    horas = datos_numericos[:, 2]
    precios = datos_numericos[:, 3]

    # 1. Grafico de dispersion: Area vs Horas de Trabajo
    plt.figure(figsize=(8, 5))
    plt.scatter(areas, horas, color="#1b7837", edgecolor="black", s=70, alpha=0.8, label="Pedidos muestreados")
    # Linea de tendencia poligonal/lineal
    z = np.polyfit(areas, horas, 1)
    p = np.poly1d(z)
    plt.plot(areas, p(areas), color="#b2182b", linestyle="--", linewidth=1.8, label="Tendencia estimada")
    plt.title("Relacion: Area Bordada (cm2) vs Horas de Trabajo", fontsize=12, fontweight="bold")
    plt.xlabel("Area del Bordado (cm²)", fontsize=10)
    plt.ylabel("Horas de Confeccion Manual", fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, "dispersion_area_vs_horas.png"), dpi=150)
    plt.close()

    # 2. Grafico de barras: Promedio de horas por tecnica artesanal
    tecnicas = {}
    for p in lista_pedidos:
        tec = p["tecnica"]
        tecnicas.setdefault(tec, []).append(p["horas_trabajo"])

    nombres_tec = list(tecnicas.keys())
    promedios_horas = [float(np.mean(tecnicas[t])) for t in nombres_tec]

    plt.figure(figsize=(9, 5))
    barras = plt.bar(nombres_tec, promedios_horas, color="#2166ac", edgecolor="black", width=0.55)
    plt.title("Promedio de Horas de Trabajo segun la Tecnica Artesanal", fontsize=12, fontweight="bold")
    plt.xlabel("Tecnica de Bordado Tradicional", fontsize=10)
    plt.ylabel("Horas Promedio", fontsize=10)
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    for barra in barras:
        yval = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2.0, yval + 1, f"{yval:.1f}h", ha="center", va="bottom", fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, "barras_horas_por_tecnica.png"), dpi=150)
    plt.close()

    # 3. Histograma: Distribucion de precios sugeridos
    plt.figure(figsize=(8, 5))
    plt.hist(precios / 1000, bins=6, color="#4393c3", edgecolor="black", alpha=0.85)
    plt.title("Distribucion de Precios Sugeridos en Pedidos (en Miles de COP)", fontsize=12, fontweight="bold")
    plt.xlabel("Precio (Miles de COP)", fontsize=10)
    plt.ylabel("Numero de Pedidos", fontsize=10)
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(ruta_salida, "distribucion_precios.png"), dpi=150)
    plt.close()

def main():
    print("=" * 65)
    print(" AVANCE DE PROYECTO: EDA - BORDADOS TRADICIONALES DE CARTAGO")
    print(" Integrantes: Davison Cruz y Juan Diego Zapata | COTECNOVA 2026")
    print("=" * 65)

    ruta_csv = os.path.join(os.path.dirname(__file__), "..", "data", "pedidos_bordados.csv")
    pedidos, datos_num = cargar_pedidos(ruta_csv)

    if pedidos is None:
        return

    print(f"\n[+] Registros cargados: {len(pedidos)} pedidos.")
    estadisticas = analizar_con_numpy(datos_num)

    print("\n--- ESTADISTICAS DESCRIPTIVAS CON NUMPY ---")
    print(f"HORAS DE TRABAJO:")
    print(f"  - Promedio: {estadisticas['horas']['promedio']:.2f} h")
    print(f"  - Mediana:  {estadisticas['horas']['mediana']:.2f} h")
    print(f"  - Desv. Est: {estadisticas['horas']['desviacion_std']:.2f} h")
    print(f"  - Rango:    {estadisticas['horas']['minimo']:.1f} h a {estadisticas['horas']['maximo']:.1f} h")

    print(f"\nPRECIO SUGERIDO (COP):")
    print(f"  - Promedio: ${estadisticas['precios']['promedio']:,.0f} COP")
    print(f"  - Mediana:  ${estadisticas['precios']['mediana']:,.0f} COP")
    print(f"  - Desv. Est: ${estadisticas['precios']['desviacion_std']:,.0f} COP")
    print(f"  - Rango:    ${estadisticas['precios']['minimo']:,.0f} a ${estadisticas['precios']['maximo']:,.0f} COP")

    ruta_img = os.path.join(os.path.dirname(__file__), "..")
    generar_visualizaciones(pedidos, datos_num, ruta_img)
    print("\n[+] Visualizaciones generadas exitosamente en la carpeta del proyecto.")

    print("\n--- HALLAZGOS CLAVE DEL ANALISIS EXPLORATORIO ---")
    print("1. El 'Calado Fino' exige en promedio mas de 50 horas por pieza, casi el triple que el Punto de Cruz y Pata de Cabra.")
    print("2. El precio y las horas tienen una fuerte correlacion lineal con el area, pero la complejidad y la tela (ej. Lino y Seda) agregan una varianza significativa que justifica un modelo de regresion de IA.")
    print("=" * 65)

if __name__ == "__main__":
    main()
