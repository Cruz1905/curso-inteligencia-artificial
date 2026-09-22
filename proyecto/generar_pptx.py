import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def crear_presentacion():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Colores tema claro
    COLOR_FONDO = RGBColor(248, 249, 250)      # Blanco grisaceo muy claro
    COLOR_TITULO = RGBColor(24, 43, 73)        # Azul marino oscuro elegante
    COLOR_ACENTO = RGBColor(16, 124, 65)       # Verde esmeralda artesanal
    COLOR_TEXTO = RGBColor(51, 51, 51)         # Gris oscuro legible
    COLOR_TARJETA = RGBColor(255, 255, 255)    # Blanco puro para tarjetas
    COLOR_BORDE = RGBColor(222, 226, 230)      # Gris claro para bordes

    blank_slide_layout = prs.slide_layouts[6]

    def aplicar_fondo(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_FONDO
        bg.line.fill.background()
        return bg

    def agregar_encabezado(slide, titulo, seccion):
        # Franja decorativa sutil
        linea = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(0.15), Inches(0.9))
        linea.fill.solid()
        linea.fill.fore_color.rgb = COLOR_ACENTO
        linea.line.fill.background()

        # Texto categoria
        cat_box = slide.shapes.add_textbox(Inches(1.1), Inches(0.4), Inches(11), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = seccion.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_ACENTO

        # Titulo de lamina
        title_box = slide.shapes.add_textbox(Inches(1.1), Inches(0.75), Inches(11.5), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = titulo
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TITULO

    # ==================== SLIDE 1: PORTADA ====================
    s1 = prs.slides.add_slide(blank_slide_layout)
    aplicar_fondo(s1)

    # Tarjeta central blanca
    tarjeta = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    tarjeta.fill.solid()
    tarjeta.fill.fore_color.rgb = COLOR_TARJETA
    tarjeta.line.color.rgb = COLOR_BORDE
    tarjeta.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.6), Inches(1.4), Inches(10.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "COTECNOVA • CORPORACIÓN DE ESTUDIOS TECNOLÓGICOS DEL NORTE DEL VALLE"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_ACENTO
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf.add_paragraph()
    p1.text = "Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados de Cartago"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TITULO
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "Entregable Avance de Proyecto – Primer Corte (IA Aplicada)"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(100, 116, 139)
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf.add_paragraph()
    p3.text = "\nIntegrantes del Proyecto:\nDavison Cruz & Juan Diego Zapata"
    p3.font.size = Pt(16)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TITULO
    p3.alignment = PP_ALIGN.CENTER

    p4 = tf.add_paragraph()
    p4.text = "Docente: Jhon James Cano Sánchez • Septiembre 2026"
    p4.font.size = Pt(13)
    p4.font.color.rgb = COLOR_TEXTO
    p4.alignment = PP_ALIGN.CENTER

    # ==================== SLIDE 2: INTRODUCCIÓN Y PROBLEMÁTICA ====================
    s2 = prs.slides.add_slide(blank_slide_layout)
    aplicar_fondo(s2)
    agregar_encabezado(s2, "Contexto Local y Definición del Problema", "1. Introducción (2 Minutos)")

    # Card Izq: Problematica
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.8), Inches(5.3), Inches(5.0))
    c1.fill.solid()
    c1.fill.fore_color.rgb = COLOR_TARJETA
    c1.line.color.rgb = COLOR_BORDE
    tb1 = s2.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(4.9), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "🚨 La Problemática en Cartago"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)

    items_prob = [
        "Cartago es la Capital Mundial del Bordado con cientos de talleres artesanales.",
        "Cobro 'al ojo' y empírico: Los presupuestos se calculan por intuición visual sin medir el área exacta ni la técnica.",
        "Desfase de horas: Técnicas complejas como el calado fino demandan decenas de horas que no se remuneran.",
        "Retrasos frecuentes en las entregas prometidas y pérdidas económicas continuas para las artesanas."
    ]
    for item in items_prob:
        pi = tf1.add_paragraph()
        pi.text = f"• {item}"
        pi.font.size = Pt(13)
        pi.font.color.rgb = COLOR_TEXTO

    # Card Der: Objetivo del Sistema
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.5), Inches(5.0))
    c2.fill.solid()
    c2.fill.fore_color.rgb = COLOR_TARJETA
    c2.line.color.rgb = COLOR_BORDE
    tb2 = s2.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.1), Inches(4.5))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "🎯 Propósito y Solución con IA"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO

    items_obj = [
        "Desarrollar un modelo de Inteligencia Artificial basado en Regresión Supervisada.",
        "Predicción 1: Horas de confección manual requeridas según técnica y tamaño en cm².",
        "Predicción 2: Precio justo sugerido (COP) que garantice una ganancia digna por hora.",
        "Estimación de Insumos: Número de madejas de hilo necesarias según la complejidad.",
        "Impacto Social: Transformar la tradición artesanal de Cartago con herramientas de IA objetivas."
    ]
    for item in items_obj:
        pi = tf2.add_paragraph()
        pi.text = f"✔ {item}"
        pi.font.size = Pt(13)
        pi.font.color.rgb = COLOR_TEXTO

    # ==================== SLIDE 3: DATOS Y FUENTE ====================
    s3 = prs.slides.add_slide(blank_slide_layout)
    aplicar_fondo(s3)
    agregar_encabezado(s3, "Estructura del Dataset de Bordados", "2. Datos del Proyecto (2 Minutos)")

    # Card: Descripcion
    c_dat = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.8), Inches(11.3), Inches(5.0))
    c_dat.fill.solid()
    c_dat.fill.fore_color.rgb = COLOR_TARJETA
    c_dat.line.color.rgb = COLOR_BORDE

    tb_dat = s3.shapes.add_textbox(Inches(1.3), Inches(2.0), Inches(10.7), Inches(4.5))
    tfd = tb_dat.text_frame
    tfd.word_wrap = True
    p = tfd.paragraphs[0]
    p.text = "📁 Archivo de Datos: 'pedidos_bordados.csv' (20 registros representativos)"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITULO

    p_sub = tfd.add_paragraph()
    p_sub.text = "Fuente: Muestreo de piezas típicas de talleres y modistas de Cartago Valle con 9 columnas estructuradas:\n"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = COLOR_TEXTO

    cols = [
        ("prenda (Texto)", "Guayabera, Blusa, Mantel, Vestido, Servilletas, Pañuelo."),
        ("tecnica (Categórica)", "Calado Fino, Punto de Sombra, Rococó, Punto de Cruz, Pata de Cabra."),
        ("tela (Categórica)", "Lino 100%, Algodón, Seda."),
        ("area_cm2 (Numérica)", "Superficie bordada en centímetros cuadrados (de 80 a 1,200 cm²)."),
        ("complejidad (Ordinal)", "Nivel de dificultad del patrón (Baja, Media, Alta, Muy Alta)."),
        ("horas_trabajo (Numérica)", "Tiempo de costura manual (Variable objetivo 1)."),
        ("precio_cop (Numérica)", "Valor cobrado en pesos colombianos (Variable objetivo 2).")
    ]
    for nom, desc in cols:
        p_c = tfd.add_paragraph()
        p_c.text = f"• {nom}: {desc}"
        p_c.font.size = Pt(12)
        p_c.font.color.rgb = COLOR_TEXTO

    # ==================== SLIDE 4: ANÁLISIS CON NUMPY Y HALLAZGOS ====================
    s4 = prs.slides.add_slide(blank_slide_layout)
    aplicar_fondo(s4)
    agregar_encabezado(s4, "Análisis Exploratorio (EDA) con NumPy", "3. Análisis Matemático (3 Minutos)")

    # Card Tabla Estadisticas
    c_num = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.8), Inches(5.4), Inches(5.0))
    c_num.fill.solid()
    c_num.fill.fore_color.rgb = COLOR_TARJETA
    c_num.line.color.rgb = COLOR_BORDE

    tbn = s4.shapes.add_textbox(Inches(1.2), Inches(2.0), Inches(5.0), Inches(4.5))
    tfn = tbn.text_frame
    tfn.word_wrap = True
    p = tfn.paragraphs[0]
    p.text = "📊 Métricas Calculadas con NumPy"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITULO

    stats_texto = [
        "Métricas calculadas con np.mean, np.median, np.std, np.min y np.max:\n",
        "🕒 Horas de Confección:",
        "   • Promedio (Media): 37.30 horas",
        "   • Mediana: 29.00 horas",
        "   • Desviación Estándar: ±24.43 horas",
        "   • Rango: de 9.5 h (mínimo) a 115.0 h (máximo)\n",
        "💰 Precios Sugeridos:",
        "   • Promedio: $287,500 COP",
        "   • Mediana: $230,000 COP",
        "   • Desviación Estándar: ±$181,490 COP",
        "   • Rango: $85,000 COP a $850,000 COP"
    ]
    for st in stats_texto:
        ps = tfn.add_paragraph()
        ps.text = st
        ps.font.size = Pt(12)
        ps.font.color.rgb = COLOR_TEXTO

    # Card Hallazgos Clave
    c_hal = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.4), Inches(5.0))
    c_hal.fill.solid()
    c_hal.fill.fore_color.rgb = COLOR_TARJETA
    c_hal.line.color.rgb = COLOR_BORDE

    tbh = s4.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.0), Inches(4.5))
    tfh = tbh.text_frame
    tfh.word_wrap = True
    p = tfh.paragraphs[0]
    p.text = "💡 Hallazgos Relevantes para la IA"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO

    hallazgos = [
        "1. Disparidad extrema por técnica artesanal:\nEl 'Calado Fino' promedia más de 50 horas por pieza, casi el triple del 'Punto de Cruz' (17h) para superficies similares. Cobrar solo por tamaño arruina a la bordadora.",
        "2. Alta dispersión de precios sin estandarizar:\nLa enorme desviación estándar ($181.490 COP) refleja la inconsistencia del cobro 'al tanteo', donde piezas similares tienen variaciones de precio de hasta un 60%.",
        "3. La tela condiciona el rendimiento:\nEn Lino y Seda, el deshilado manual reduce la velocidad de bordado un 35% respecto al Algodón."
    ]
    for h in hallazgos:
        ph = tfh.add_paragraph()
        ph.text = f"• {h}\n"
        ph.font.size = Pt(12)
        ph.font.color.rgb = COLOR_TEXTO

    # ==================== SLIDE 5: VISUALIZACIONES ====================
    s5 = prs.slides.add_slide(blank_slide_layout)
    aplicar_fondo(s5)
    agregar_encabezado(s5, "Visualización de Datos con Matplotlib", "3. Visualizaciones del Proyecto")

    img_dir = "C:/Users/davis/OneDrive/Desktop/curso-inteligencia-artificial/proyecto"
    img1_path = os.path.join(img_dir, "barras_horas_por_tecnica.png")
    img2_path = os.path.join(img_dir, "dispersion_area_vs_horas.png")

    if os.path.exists(img1_path):
        s5.shapes.add_picture(img1_path, Inches(0.8), Inches(1.8), width=Inches(5.6))
    if os.path.exists(img2_path):
        s5.shapes.add_picture(img2_path, Inches(6.8), Inches(1.8), width=Inches(5.7))

    # Pie de foto
    lbl_box = s5.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.6))
    p_lbl = lbl_box.text_frame.paragraphs[0]
    p_lbl.text = "Gráfica 1 (Izquierda): Comparativa de horas por técnica • Gráfica 2 (Derecha): Correlación positiva y dispersión Área vs Horas"
    p_lbl.font.size = Pt(12)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = COLOR_TITULO
    p_lbl.alignment = PP_ALIGN.CENTER

    # ==================== SLIDE 6: CÓDIGO Y GITHUB ====================
    s6 = prs.slides.add_slide(blank_slide_layout)
    aplicar_fondo(s6)
    agregar_encabezado(s6, "Implementación en Python y Repositorio", "4. Código y Control de Versiones (2 Minutos)")

    c_cod = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.8), Inches(11.3), Inches(5.0))
    c_cod.fill.solid()
    c_cod.fill.fore_color.rgb = COLOR_TARJETA
    c_cod.line.color.rgb = COLOR_BORDE

    tbc = s6.shapes.add_textbox(Inches(1.3), Inches(2.0), Inches(10.7), Inches(4.5))
    tfc = tbc.text_frame
    tfc.word_wrap = True

    p = tfc.paragraphs[0]
    p.text = "⚙️ Script Principal: `src/eda_proyecto.py`"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_TITULO

    items_code = [
        "Lectura de Datos: Implementación de `csv.DictReader` con manejo de codificación UTF-8 para cargar cada pedido como un diccionario estructurado.",
        "Función Propia Creada: `calcular_rendimiento(area, horas)` que computa los cm² avanzados por hora de trabajo como indicador de productividad.",
        "Vectorización con NumPy: Creación de matriz 2D `np.array` para ejecutar cómputo estadístico instantáneo sin bucles for lentos.",
        "Generación Gráfica: Funciones modulares de Matplotlib con guardado automático en archivos `.png`.",
        "Repositorio GitHub Oficial: `https://github.com/Cruz1905/curso-inteligencia-artificial` con historial de commits verificables y documentación en README.md."
    ]
    for ic in items_code:
        pic = tfc.add_paragraph()
        pic.text = f"✔ {ic}\n"
        pic.font.size = Pt(13)
        pic.font.color.rgb = COLOR_TEXTO

    # ==================== SLIDE 7: PRÓXIMOS PASOS ====================
    s7 = prs.slides.add_slide(blank_slide_layout)
    aplicar_fondo(s7)
    agregar_encabezado(s7, "Ruta hacia el Segundo y Tercer Corte", "5. Próximos Pasos (1 Minuto)")

    c_prox = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.8), Inches(11.3), Inches(5.0))
    c_prox.fill.solid()
    c_prox.fill.fore_color.rgb = COLOR_TARJETA
    c_prox.line.color.rgb = COLOR_BORDE

    tbp = s7.shapes.add_textbox(Inches(1.3), Inches(2.0), Inches(10.7), Inches(4.5))
    tfp = tbp.text_frame
    tfp.word_wrap = True

    p = tfp.paragraphs[0]
    p.text = "🚀 Hoja de Ruta para el Modelo de IA"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACENTO

    items_prox = [
        "Segundo Corte (30%): Preprocesamiento de variables categóricas (One-Hot Encoding para técnica y tela).",
        "Entrenamiento de Modelos: Evaluación y comparación con Scikit-Learn de Regresión Lineal Múltiple, Árboles de Decisión y Random Forest Regressor.",
        "Métricas de Validación: Medición de error cuadrático medio (RMSE) y coeficiente de determinación (R²) para asegurar un error menor al 10%.",
        "Tercer Corte (40%): Despliegue de una interfaz visual interactiva con Streamlit donde cualquier taller artesanal de Cartago pueda ingresar las medidas y obtener la cotización instantánea."
    ]
    for ip in items_prox:
        pip = tfp.add_paragraph()
        pip.text = f"➡ {ip}\n"
        pip.font.size = Pt(13)
        pip.font.color.rgb = COLOR_TEXTO

    out_file = "C:/Users/davis/OneDrive/Desktop/curso-inteligencia-artificial/Avance_Proyecto_Bordados_Cartago.pptx"
    prs.save(out_file)
    print(f"Presentacion creada exitosamente en: {out_file}")

if __name__ == "__main__":
    crear_presentacion()
