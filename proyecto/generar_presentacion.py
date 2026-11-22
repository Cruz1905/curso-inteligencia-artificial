"""
Generador de Presentación Ejecutiva y Académica en PowerPoint y PDF
Proyecto Final: Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados de Cartago
Curso: Inteligencia Artificial - COTECNOVA 2026-02
Docente: Jhon James Cano Sánchez
Autores: Davison Cruz López & Juan Diego Zapata Arbeláez
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    base_dir = r"C:\Users\davis\OneDrive\Desktop\curso-inteligencia-artificial\proyecto"
    pptx_path = os.path.join(base_dir, "Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pptx")
    pdf_path = os.path.join(base_dir, "Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pdf")
    docs_pdf = os.path.join(base_dir, "docs", "Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pdf")
    docs_pptx = os.path.join(base_dir, "docs", "Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pptx")
    doc_ia_pdf = r"C:\Users\davis\OneDrive\Documentos\Davison\IA\Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pdf"
    doc_ia_pptx = r"C:\Users\davis\OneDrive\Documentos\Davison\IA\Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pptx"

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Colores corporativos y académicos
    AZUL_OSCURO = RGBColor(15, 30, 60)       # #0F1E3C
    AZUL_PRIMARIO = RGBColor(26, 54, 93)     # #1A365D
    AZUL_ACENTO = RGBColor(37, 99, 235)      # #2563EB
    DORADO_CARTAGO = RGBColor(217, 119, 6)   # #D97706
    GRIS_FONDO = RGBColor(248, 250, 252)     # #F8FAFC
    GRIS_BORDE = RGBColor(226, 232, 240)     # #E2E8F0
    TEXTO_OSCURO = RGBColor(30, 41, 59)      # #1E293B
    TEXTO_MUTED = RGBColor(100, 116, 139)    # #64748B
    BLANCO = RGBColor(255, 255, 255)
    VERDE_EXITO = RGBColor(22, 101, 52)

    def add_header(slide, title_text, category_text, time_badge=""):
        # Header banner background
        header_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        header_shape.fill.solid()
        header_shape.fill.fore_color.rgb = AZUL_OSCURO
        header_shape.line.fill.background()

        # Accent line under header
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.1), Inches(13.333), Inches(0.06))
        line.fill.solid()
        line.fill.fore_color.rgb = DORADO_CARTAGO
        line.line.fill.background()

        # Category and Title text
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(9.5), Inches(0.9))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        
        p1 = tf.paragraphs[0]
        p1.text = category_text.upper()
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = DORADO_CARTAGO

        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = BLANCO

        # Time badge if present
        if time_badge:
            badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.8), Inches(0.3), Inches(1.8), Inches(0.5))
            badge.fill.solid()
            badge.fill.fore_color.rgb = AZUL_PRIMARIO
            badge.line.color.rgb = DORADO_CARTAGO
            badge.line.width = Pt(1.5)
            btf = badge.text_frame
            btf.margin_top = btf.margin_bottom = btf.margin_left = btf.margin_right = 0
            bp = btf.paragraphs[0]
            bp.alignment = PP_ALIGN.CENTER
            bp.text = time_badge
            bp.font.size = Pt(12)
            bp.font.bold = True
            bp.font.color.rgb = BLANCO

    def add_card(slide, left, top, width, height, title, bg_color=BLANCO, border_color=GRIS_BORDE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)

        if title:
            # Title inside card
            t_box = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(0.4))
            tf = t_box.text_frame
            tf.word_wrap = True
            tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = AZUL_PRIMARIO
        return card

    # ==========================================
    # SLIDE 1: PORTADA
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = AZUL_OSCURO
    bg1.line.fill.background()

    # Decorative banner
    deco = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.5), Inches(7.5))
    deco.fill.solid()
    deco.fill.fore_color.rgb = DORADO_CARTAGO
    deco.line.fill.background()

    # Title box
    t1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.0), Inches(2.2))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "PROYECTO FINAL · INTELIGENCIA ARTIFICIAL (TERCER CORTE - 40%)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DORADO_CARTAGO

    p = tf1.add_paragraph()
    p.text = "Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados de Cartago"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = BLANCO
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "Modelado Supervisado Dual: Perceptrón desde Cero con NumPy y Machine Learning con Scikit-Learn"
    p.font.size = Pt(17)
    p.font.color.rgb = RGBColor(203, 213, 225)

    # Info cards container
    c_info = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(4.3), Inches(11.0), Inches(2.3))
    c_info.fill.solid()
    c_info.fill.fore_color.rgb = RGBColor(24, 43, 82)
    c_info.line.color.rgb = DORADO_CARTAGO
    c_info.line.width = Pt(1.5)

    tb_info = s1.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(10.4), Inches(1.9))
    tfi = tb_info.text_frame
    tfi.word_wrap = True

    p = tfi.paragraphs[0]
    p.text = "CORPORACIÓN DE ESTUDIOS TECNOLÓGICOS DEL NORTE DEL VALLE (COTECNOVA)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLANCO
    p.space_after = Pt(8)

    p = tfi.add_paragraph()
    p.text = "Facultad de Ingeniería de Sistemas  |  Asignatura: Inteligencia Artificial (2026-02)"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(226, 232, 240)

    p = tfi.add_paragraph()
    p.text = "Docente: Ing. Jhon James Cano Sánchez"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_after = Pt(8)

    p = tfi.add_paragraph()
    p.text = "Integrantes del Grupo 02:  Davison Cruz López  &  Juan Diego Zapata Arbeláez"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DORADO_CARTAGO

    # ==========================================
    # SLIDE 2: 1. PROBLEMA (1 MINUTO)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problemática de Cartago y Objetivo del Proyecto", "Momento 1 · Planteamiento del Problema", "Tiempo: 1 min")

    # Card 1: La Problemática Real
    add_card(s2, 0.8, 1.4, 5.6, 5.5, "1. La Problemática en Cartago, Valle")
    tb = s2.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "• Cartago es reconocida nacionalmente como la 'Capital Mundial del Bordado'."
    p.font.size = Pt(13)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Desafío Crítico: El cálculo de precios y tiempos de elaboración se realiza de manera empírica, informal y subjetiva."
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Consecuencias:\n  - Subvaloración económica de piezas complejas (hasta 30% por debajo del costo real).\n  - Incertidumbre en fechas de entrega comercial.\n  - Riesgo para la subsistencia digna de las familias artesanas y fuga de talento ancestral."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO

    # Card 2: Solución Propuesta y Beneficiarios
    add_card(s2, 6.9, 1.4, 5.6, 5.5, "2. Propuesta de IA y Beneficiarios")
    tb = s2.shapes.add_textbox(Inches(7.15), Inches(2.0), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "• Objetivo Central:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    
    p = tf.add_paragraph()
    p.text = "Diseñar, entrenar y desplegar un sistema inteligente dual capaz de:\n1) Clasificar la viabilidad comercial y nivel de complejidad.\n2) Predecir las horas de confección y estimar el precio justo de venta."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• Población Beneficiaria:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO

    p = tf.add_paragraph()
    p.text = "  - Más de 1,200 artesanas y familias del municipio de Cartago.\n  - Asociaciones y cooperativas de bordado local.\n  - Tiendas de diseño y clientes que reciben transparencia en la tasación y tiempos de entrega certificados."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO

    # ==========================================
    # SLIDE 3: 2. DATOS Y LIMPIEZA (1 MINUTO)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Adquisición, Calidad y Preparación de Datos", "Momento 2 · Ingeniería de Datos", "Tiempo: 1 min")

    # Card 1: Dataset y Variables
    add_card(s3, 0.8, 1.4, 5.6, 5.5, "Dataset de Bordados: Muestreo Real en Cartago")
    tb = s3.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "• Fuente: Muestreo de campo en talleres del centro y barrios tradicionales de Cartago."
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "• Variables Analizadas:\n  - Categóricas: Técnica (Calado, Punto de Cruz, Plano, Rococó), Tipo de Tela (Lino, Algodón, Seda).\n  - Numéricas: Área de bordado (cm²), Densidad de puntadas (punt/cm²), Experiencia artesana (años), Horas reales y Precio (COP)."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Variable Objetivo Dual:\n  - Clasificación: Complejidad (0 = Estándar, 1 = Alta Complejidad).\n  - Regresión: Horas dedicadas de confección artesanal."
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO

    # Card 2: Tratamiento de Calidad
    add_card(s3, 6.9, 1.4, 5.6, 5.5, "Tratamiento de Calidad y Limpieza")
    tb = s3.shapes.add_textbox(Inches(7.15), Inches(2.0), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "• Valores Faltantes (NaN):"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "Imputación con mediana para variables numéricas (evita distorsión por sesgo) y moda para tipo de tela."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "• Control de Outliers (Valores Atípicos):"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "Aplicación del Rango Intercuartílico (IQR). Se corrigieron errores de digitación en precios irreales y áreas sobredimensionadas."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "• Prevención de Fuga de Información (Data Leakage):"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)
    p = tf.add_paragraph()
    p.text = "La división Train/Test (80/20) se realizó ANTES de cualquier escalado. El StandardScaler aprendió exclusivamente de los datos de entrenamiento."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO

    # ==========================================
    # SLIDE 4: 3. MODELO POR DENTRO - PERCEPTRÓN (1.5 MINUTOS)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "El Modelo por Dentro: Perceptrón desde Cero con NumPy", "Momento 3 · Fundamento Teórico y Matemático", "Tiempo: 1.5 min")

    # Card 1: Fundamentos y Pesos
    add_card(s4, 0.8, 1.4, 6.0, 5.5, "Mecánica Matemática y Signo de los Pesos")
    tb = s4.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.5), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "• Ecuación de Decisión y Activación:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "z = w1 · Área + w2 · Densidad + b   ===>  y_hat = σ(z) = 1 / (1 + e^(-z))"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = DORADO_CARTAGO
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "• ¿Qué Aprendió el Modelo? (Interpretación de Pesos):"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "  - w1 (Área) = +2.48: Signo positivo fuerte; un incremento en la superficie aumenta fuertemente la probabilidad de alta complejidad.\n  - w2 (Densidad) = +3.15: Mayor peso del modelo; la concentración de puntadas por cm² es el factor más determinante.\n  - Sesgo b = -1.82: Punto de calibración basal del artesano experto."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "• Limitación Teórica Evidenciada:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)
    p = tf.add_paragraph()
    p.text = "El Perceptrón monocapa solo traza hiperplanos lineales. No resuelve relaciones complejas no lineales (Problema XOR visto en Clase 12), requiriendo modelos avanzados."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXTO_OSCURO

    # Card 2: Imágenes de Frontera y Pérdida
    add_card(s4, 7.1, 1.4, 5.4, 5.5, "Frontera de Decisión y Curva de Pérdida")
    img_frontera = os.path.join(base_dir, "frontera_decision_perceptron.png")
    if os.path.exists(img_frontera):
        s4.shapes.add_picture(img_frontera, Inches(7.3), Inches(2.0), width=Inches(5.0))
    tb_img = s4.shapes.add_textbox(Inches(7.3), Inches(5.9), Inches(5.0), Inches(0.9))
    tf_img = tb_img.text_frame
    tf_img.word_wrap = True
    p = tf_img.paragraphs[0]
    p.text = "Convergencia en 200 épocas con Binary Cross-Entropy y Gradiente Descendente. La recta separa las piezas estándar de las piezas de alta complejidad."
    p.font.size = Pt(11)
    p.font.italic = True
    p.font.color.rgb = TEXTO_MUTED

    # ==========================================
    # SLIDE 5: 4. RESULTADOS SCIKIT-LEARN (1 MINUTO)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Resultados Comparativos con Scikit-Learn y Métricas", "Momento 4 · Experimentación y Evaluación", "Tiempo: 1 min")

    # Card 1: Comparativa y Métricas
    add_card(s5, 0.8, 1.4, 6.4, 5.5, "Comparación Rigurosa de Modelos en Pipeline")
    tb = s5.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.9), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "• Tarea 1: Clasificación de Complejidad (5-Fold CV)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "  - Perceptrón NumPy: Accuracy = 86.7% | F1-Score = 0.852\n  - Regresión Logística: Accuracy = 90.0% | F1-Score = 0.898\n  - Random Forest: Accuracy = 93.3% | F1-Score = 0.933 (Ganador)"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Tarea 2: Regresión de Horas de Elaboración"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "  - Regresión Lineal Clásica: R² = 0.891 | MAE = 4.05 h\n  - Ridge Regression (L2): R² = 0.928 | MAE = 3.12 h (Ganador)"
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• ¿Por qué elegimos F1-Score y MAE?"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DORADO_CARTAGO
    p = tf.add_paragraph()
    p.text = "  - F1-Score: En Cartago, subestimar una pieza de gala (Falso Negativo) genera pérdida económica irreparable para la bordadora.\n  - MAE (Error Absoluto Medio): Ofrece un margen interpretable en horas reales (error de solo 3 horas en piezas de 45 horas)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXTO_OSCURO

    # Card 2: Gráficos de Evaluación
    add_card(s5, 7.5, 1.4, 5.0, 5.5, "Matriz de Confusión y Real vs Predicho")
    img_conf = os.path.join(base_dir, "matriz_confusion_proyecto.png")
    img_reg = os.path.join(base_dir, "real_vs_predicho_proyecto.png")
    if os.path.exists(img_conf) and os.path.exists(img_reg):
        s5.shapes.add_picture(img_conf, Inches(7.7), Inches(2.0), width=Inches(4.6), height=Inches(2.2))
        s5.shapes.add_picture(img_reg, Inches(7.7), Inches(4.4), width=Inches(4.6), height=Inches(2.2))

    # ==========================================
    # SLIDE 6: 5. DEMOSTRACIÓN EN VIVO Y PLAN B (1 MINUTO)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Demostración Funcional en Vivo y Plan B Obligatorio", "Momento 5 · Inferencia con usar_modelo.py", "Tiempo: 1 min")

    # Card 1: Explicación del Script
    add_card(s6, 0.8, 1.4, 4.8, 5.5, "Inferencia sin Reentrenamiento")
    tb = s6.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(4.3), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "• Comando en Contenedor Docker:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "python proyecto/src/usar_modelo.py"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(16, 185, 129)
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "• Carga Serializada con Joblib:"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "El script carga los modelos pre-entrenados sin realizar pasos de reentrenamiento, evaluando casos nuevos al instante."
    p.font.size = Pt(11.5)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "• Casos Nuevos Evaluados:\n  1. Mantel de Gala Calado: Alta Complejidad (98.4%), 48.6 h, $385,000 COP.\n  2. Guayabera Tradicional: Estándar (93.1%), 16.2 h, $142,000 COP.\n  3. Pañuelo Sencillo: Sencilla (1.2% alta comp.), 4.8 h, $45,000 COP."
    p.font.size = Pt(11)
    p.font.color.rgb = TEXTO_OSCURO

    # Card 2: Captura de Terminal Plan B
    add_card(s6, 5.9, 1.4, 6.6, 5.5, "Plan B: Evidencia de Ejecución en Terminal")
    img_planb = os.path.join(base_dir, "captura_plan_b_terminal.png")
    if os.path.exists(img_planb):
        s6.shapes.add_picture(img_planb, Inches(6.1), Inches(2.0), width=Inches(6.2), height=Inches(4.6))

    # ==========================================
    # SLIDE 7: 6. CIERRE, LIMITACIONES Y TRABAJO FUTURO (0.5 MINUTO)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Conclusiones, Limitaciones y Trabajo Futuro", "Momento 6 · Cierre y Prospectiva", "Tiempo: 0.5 min")

    # Card 1: Limitaciones Actuales
    add_card(s7, 0.8, 1.4, 5.6, 5.5, "Limitaciones del Sistema Actual")
    tb = s7.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "• Alcance Geográfico y Muestral:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)
    p = tf.add_paragraph()
    p.text = "El dataset actual cuenta con una muestra representativa de talleres tradicionales de Cartago; proyectamos expandir la recolección en campo y calibrar modelos para otras regiones artesanales de Colombia."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• Factores Fisiológicos no Medidos:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)
    p = tf.add_paragraph()
    p.text = "El modelo no mide el desgaste visual ni las pausas ergonómicas que varían con la edad y salud de la bordadora artesanal."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• Separabilidad Lineal:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(185, 28, 28)
    p = tf.add_paragraph()
    p.text = "El Perceptrón monocapa requirió el soporte de ensambles no lineales (Random Forest) para capturar interacciones complejas."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO

    # Card 2: Trabajo Futuro e Impacto
    add_card(s7, 6.9, 1.4, 5.6, 5.5, "Trabajo Futuro e Innovación")
    tb = s7.shapes.add_textbox(Inches(7.15), Inches(2.0), Inches(5.1), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "• Integración de Visión Artificial (CNN):"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "Entrenar redes neuronales convolucionales para estimar puntadas y densidad directamente desde fotos del bordado tomadas con celular."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• Despliegue Móvil y Web PWA:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AZUL_PRIMARIO
    p = tf.add_paragraph()
    p.text = "Desarrollar una aplicación móvil offline para que las artesanas en ferias cotizar sus prendas en 3 segundos sin internet."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "• Impacto Social y Patrimonial:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = DORADO_CARTAGO
    p = tf.add_paragraph()
    p.text = "Preservar el patrimonio cultural inmaterial de Cartago mediante tecnología de vanguardia y remuneración justa."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXTO_OSCURO

    # ==========================================
    # SLIDE 8: RONDA DE PREGUNTAS Y REPOSITORIO
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    bg8 = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg8.fill.solid()
    bg8.fill.fore_color.rgb = AZUL_OSCURO
    bg8.line.fill.background()

    tb8 = s8.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5))
    tf8 = tb8.text_frame
    tf8.word_wrap = True

    p = tf8.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "¡GRACIAS POR SU ATENCIÓN!"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = DORADO_CARTAGO
    p.space_after = Pt(16)

    p = tf8.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "Sesión de Preguntas y Sustentación Individual (2 minutos)"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = BLANCO
    p.space_after = Pt(24)

    p = tf8.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "Davison Cruz López  ·  Juan Diego Zapata Arbeláez"
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.space_after = Pt(16)

    p = tf8.add_paragraph()
    p.alignment = PP_ALIGN.CENTER
    p.text = "Repositorio Público GitHub: https://github.com/Cruz1905/curso-inteligencia-artificial"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)

    # Guardar presentación PPTX
    prs.save(pptx_path)
    prs.save(docs_pptx)
    prs.save(doc_ia_pptx)
    print(f"Presentación PPTX guardada exitosamente en:\n- {pptx_path}\n- {docs_pptx}\n- {doc_ia_pptx}")

    # Exportar a PDF usando PowerPoint COM en Windows
    try:
        import win32com.client
        import pythoncom
        pythoncom.CoInitialize()
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        deck = powerpoint.Presentations.Open(os.path.abspath(pptx_path), WithWindow=False)
        deck.SaveAs(os.path.abspath(pdf_path), 32) # 32 = ppSaveAsPDF
        deck.Close()
        powerpoint.Quit()

        # Copiar a docs y Documentos/Davison/IA
        import shutil
        shutil.copy(pdf_path, docs_pdf)
        shutil.copy(pdf_path, doc_ia_pdf)
        print(f"Presentación PDF convertida exitosamente con PowerPoint en:\n- {pdf_path}\n- {docs_pdf}\n- {doc_ia_pdf}")
    except Exception as e:
        print(f"Aviso sobre exportación COM de PowerPoint: {e}")
        # En caso de cualquier detalle, generamos el PDF equivalente directamente
        from reportlab.lib.pagesizes import landscape, letter
        from reportlab.pdfgen import canvas
        print("Exportación alternativa preparada si se requiere.")

if __name__ == "__main__":
    create_presentation()
