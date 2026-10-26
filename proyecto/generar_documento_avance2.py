"""
generar_documento_avance2.py
Script generador del documento formal académico en PDF:
'Avance2_Grupo02_BordadosCartago.pdf'
Cumple con la totalidad de los requisitos de la guía del Segundo Corte (COTECNOVA 2026-02).
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# ==============================================================================
# CLASE CANVAS NUMERADA PARA ENCABEZADO Y PIE DE PÁGINA ("Página X de Y")
# ==============================================================================

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # La portada (Página 1) no lleva encabezado ni pie de página
        if self._pageNumber > 1:
            self.saveState()
            
            # Encabezado superior
            self.setFont('Helvetica-Bold', 8)
            self.setFillColor(colors.HexColor('#182B49')) # Azul institucional
            self.drawString(54, 752, 'COTECNOVA · INTELIGENCIA ARTIFICIAL')
            self.setFont('Helvetica', 8)
            self.setFillColor(colors.HexColor('#555555'))
            self.drawRightString(558, 752, 'Avance de Proyecto – Segundo Corte (Período 2026-02)')
            
            # Línea sutil superior
            self.setStrokeColor(colors.HexColor('#107C41')) # Verde esmeralda artesanal
            self.setLineWidth(1.0)
            self.line(54, 746, 558, 746)

            # Pie de página inferior
            self.setStrokeColor(colors.HexColor('#D1D5DB'))
            self.setLineWidth(0.5)
            self.line(54, 45, 558, 45)

            self.setFont('Helvetica', 8)
            self.setFillColor(colors.HexColor('#555555'))
            self.drawString(54, 33, 'Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados de Cartago')
            
            # Numeración de página dinámica
            page_text = f'Página {self._pageNumber} de {page_count}'
            self.setFont('Helvetica-Bold', 8)
            self.setFillColor(colors.HexColor('#182B49'))
            self.drawRightString(558, 33, page_text)
            
            self.restoreState()

# ==============================================================================
# CONSTRUCCIÓN DEL DOCUMENTO PDF
# ==============================================================================

def generar_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_pdf_proyecto = os.path.join(base_dir, 'Avance2_Grupo02_BordadosCartago.pdf')
    ruta_pdf_documentos = r'C:\Users\davis\OneDrive\Documentos\Davison\IA\Avance2_Grupo02_BordadosCartago.pdf'

    # Margen de 0.75 pulgadas (54 puntos)
    doc = SimpleDocTemplate(
        ruta_pdf_proyecto,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    # Paleta de Colores Académica
    C_AZUL_PRINCIPAL = colors.HexColor('#182B49')
    C_VERDE_ACENTO   = colors.HexColor('#107C41')
    C_TEXTO_OSCURO   = colors.HexColor('#222222')
    C_GRIS_CLARO     = colors.HexColor('#F8F9FA')
    C_BORDE_TABLA    = colors.HexColor('#D1D5DB')

    # Estilos de Párrafo
    styles = getSampleStyleSheet()

    title_cover_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=C_AZUL_PRINCIPAL,
        alignment=1, # Centrado
        spaceAfter=15
    )

    subtitle_cover_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=C_VERDE_ACENTO,
        alignment=1,
        spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=C_AZUL_PRINCIPAL,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=C_VERDE_ACENTO,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=C_TEXTO_OSCURO,
        alignment=4, # Justificado
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=C_TEXTO_OSCURO,
        leftIndent=15,
        spaceAfter=4
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#4B5563'),
        alignment=1,
        spaceBefore=4,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1F2937')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=C_TEXTO_OSCURO
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=C_TEXTO_OSCURO,
        alignment=1
    )

    story = []

    # ==========================================================================
    # PÁGINA 1: PORTADA FORMAL ACADÉMICA
    # ==========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("CORPORACIÓN DE ESTUDIOS TECNOLÓGICOS DEL NORTE DEL VALLE<br/><b>COTECNOVA</b>", ParagraphStyle('Univ', alignment=1, fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=C_AZUL_PRINCIPAL)))
    story.append(Paragraph("FACULTAD DE INGENIERÍA · PROGRAMA DE INGENIERÍA DE SISTEMAS", ParagraphStyle('Fac', alignment=1, fontName='Helvetica', fontSize=10, leading=14, textColor=C_VERDE_ACENTO)))
    story.append(Spacer(1, 40))

    story.append(HRFlowable(width="80%", thickness=2.5, color=C_VERDE_ACENTO, spaceAfter=25, spaceBefore=10))
    story.append(Paragraph("SISTEMA INTELIGENTE DE TASACIÓN Y ESTIMACIÓN DE TIEMPOS PARA BORDADOS TRADICIONALES DE CARTAGO", title_cover_style))
    story.append(Paragraph("DOCUMENTO DE ENTREGA – AVANCE DE PROYECTO (SEGUNDO CORTE)<br/><i>Modelado de Datos, Visualización y Perceptrón desde Cero</i>", subtitle_cover_style))
    story.append(HRFlowable(width="80%", thickness=2.5, color=C_VERDE_ACENTO, spaceAfter=35, spaceBefore=10))

    story.append(Spacer(1, 20))
    info_portada = [
        [Paragraph("<b>Asignatura:</b>", body_style), Paragraph("Inteligencia Artificial (Período Académico 2026-02)", body_style)],
        [Paragraph("<b>Docente:</b>", body_style), Paragraph("Ing. Jhon James Cano Sánchez", body_style)],
        [Paragraph("<b>Integrantes (Grupo 02):</b>", body_style), Paragraph("<b>Davison Cruz</b> (Código Estudiantil)<br/><b>Juan Diego Zapata</b> (Código Estudiantil)", body_style)],
        [Paragraph("<b>Línea de Investigación:</b>", body_style), Paragraph("Machine Learning Supervisado aplicado al Sector Artesanal", body_style)],
        [Paragraph("<b>Repositorio Oficial:</b>", body_style), Paragraph("https://github.com/Cruz1905/curso-inteligencia-artificial", body_style)],
        [Paragraph("<b>Fecha de Presentación:</b>", body_style), Paragraph("Domingo, 25 de octubre de 2026", body_style)],
        [Paragraph("<b>Municipio:</b>", body_style), Paragraph("Cartago, Valle del Cauca, Colombia", body_style)]
    ]
    t_portada = Table(info_portada, colWidths=[150, 320])
    t_portada.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
    ]))
    story.append(t_portada)
    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 2: RESUMEN Y AJUSTES DESDE EL AVANCE 1
    # ==========================================================================
    story.append(Paragraph("1. Resumen Ejecutivo del Proyecto", h1_style))
    story.append(Paragraph(
        "El municipio de Cartago, Valle del Cauca, ostenta el reconocimiento cultural de <i>Capital Mundial del Bordado</i>. "
        "Sin embargo, la industria artesanal local opera bajo un modelo de tasación puramente consuetudinario y empírico (\"al ojo\"). "
        "Las bordadoras tradicionales calculan el tiempo de entrega y el precio de venta sin herramientas estandarizadas, lo que "
        "deriva sistemáticamente en la subvaloración del trabajo manual, desequilibrios económicos y retrasos imprevistos en pedidos de alta complejidad.",
        body_style
    ))
    story.append(Paragraph(
        "El presente proyecto desarrolla un sistema fundamentado en Inteligencia Artificial (Machine Learning) orientado a resolver dos necesidades críticas: "
        "1) <b>Estimar con precisión matemática las horas de trabajo manual</b> requeridas para confeccionar una prenda personalizada; y "
        "2) <b>Predecir un precio justo de venta sugerido (COP)</b> que garantice una retribución digna y competitiva. "
        "Para ello, se estructuró un dataset primario de 20 encargos representativos con 9 atributos técnicos (técnica, tela, área en cm², complejidad, "
        "madejas de hilo, horas y precio), capturados directamente en talleres del municipio.",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(Paragraph("2. Ajustes Realizados a Partir del Avance 1", h1_style))
    story.append(Paragraph(
        "Durante la sustentación del primer corte (21 de septiembre de 2026), se recibieron retroalimentaciones orientadas a fortalecer "
        "la rigurosidad metodológica del proyecto. A continuación se detallan las observaciones y las acciones implementadas:",
        body_style
    ))

    ajustes_data = [
        [
            Paragraph("<b>Observación del Docente (Avance 1)</b>", table_header_style),
            Paragraph("<b>Acción Implementada en el Avance 2</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. Rigor en el tipo de problema:</b> Precisar si el proyecto final es clasificación o regresión, evitando ambigüedades en la métrica.", table_cell_style),
            Paragraph("Se delimitó formalmente que el proyecto final es estrictamente de <b>REGRESIÓN</b> (predicción de cantidades continuas en horas y pesos COP). Para la actividad pedagógica de las Clases 8 y 9, se adaptó un hito de clasificación binaria mediante el umbral de la mediana de horas.", table_cell_style)
        ],
        [
            Paragraph("<b>2. Integridad del dataset:</b> Sustentar la limpieza de datos y garantizar que no existan inconsistencias o fuga de información.", table_cell_style),
            Paragraph("Se realizó una auditoría con Pandas verificando 0 nulos y 0 duplicados. Se garantizó formalmente que las variables predictoras del perceptrón no incluyan ni horas ni precio (evitando <i>data leakage</i>).", table_cell_style)
        ],
        [
            Paragraph("<b>3. Ingeniería de características:</b> Incorporar métricas derivadas propias del sector artesanal para aportar valor contextual.", table_cell_style),
            Paragraph("Se crearon dos columnas derivadas: <code>costo_por_cm2</code> ($/cm²) y <code>productividad_cm2_hora</code> (cm²/h), las cuales enriquecen la descripción del rendimiento por técnica.", table_cell_style)
        ]
    ]
    t_ajustes = Table(ajustes_data, colWidths=[220, 284])
    t_ajustes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_AZUL_PRINCIPAL),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDE_TABLA),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_GRIS_CLARO]),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ajustes)
    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 3 y 4: PREPARACIÓN DE DATOS CON PANDAS
    # ==========================================================================
    story.append(Paragraph("3. Preparación y Limpieza de Datos con Pandas", h1_style))
    story.append(Paragraph(
        "En cumplimiento de los lineamientos de la Clase 7, se ejecutó un proceso sistemático de preparación de datos mediante la librería "
        "<b>Pandas</b> en el script <code>src/preparacion_datos_proyecto.py</code>. Este proceso transformó el archivo crudo en dos matrices estructuradas: "
        "<code>data/pedidos_bordados_limpio.csv</code> (dataset enriquecido para análisis exploratorio) y <code>data/pedidos_bordados_preparados_ml.csv</code> "
        "(matriz numérica codificada con One-Hot Encoding lista para algoritmos de Machine Learning).",
        body_style
    ))

    story.append(Paragraph("3.1. Diagnóstico e Inspección Inicial", h2_style))
    story.append(Paragraph(
        "Se procedió con la inspección estructural del dataset original (20 registros y 9 variables). Se verificó la consistencia mediante "
        "las funciones <code>df.info()</code>, <code>df.isnull().sum()</code> y <code>df.duplicated().sum()</code>:",
        body_style
    ))
    story.append(Paragraph("• <b>Valores nulos:</b> Se confirmó la ausencia de valores vacíos (0 nulos en todas las columnas).", bullet_style))
    story.append(Paragraph("• <b>Duplicados:</b> 0 registros repetidos; cada pedido corresponde a una pieza artesanal individualizada.", bullet_style))
    story.append(Paragraph("• <b>Validación de rangos de dominio:</b> Las variables continuas conservan cotas lógicas: el área oscila entre 80 cm² (pañuelos) y 1.200 cm² (manteles de banquete); el insumo de hilo varía de 1 a 14 madejas; el tiempo abarca de 9.5 a 115 horas; y el precio de venta fluctúa entre $85.000 y $850.000 COP.", bullet_style))

    story.append(Paragraph("3.2. Tabla Comparativa de Transformación ('Antes / Después')", h2_style))
    story.append(Paragraph(
        "A continuación se presenta la tabla formal que resume los cambios estructurales operados sobre los datos:",
        body_style
    ))

    antes_despues_data = [
        [Paragraph("<b>Métrica / Atributo</b>", table_header_style), Paragraph("<b>Dataset Original (Crudo)</b>", table_header_style), Paragraph("<b>Dataset Limpio</b>", table_header_style), Paragraph("<b>Dataset para ML (One-Hot)</b>", table_header_style)],
        [Paragraph("Archivo de almacenamiento", table_cell_style), Paragraph("<code>pedidos_bordados.csv</code>", table_cell_center), Paragraph("<code>pedidos_bordados_limpio.csv</code>", table_cell_center), Paragraph("<code>pedidos_bordados_preparados_ml.csv</code>", table_cell_center)],
        [Paragraph("Número de filas (muestras)", table_cell_style), Paragraph("20", table_cell_center), Paragraph("20", table_cell_center), Paragraph("20", table_cell_center)],
        [Paragraph("Número de columnas", table_cell_style), Paragraph("9", table_cell_center), Paragraph("11 (+2 derivados)", table_cell_center), Paragraph("18 (matriz numérica)", table_cell_center)],
        [Paragraph("Valores nulos totales", table_cell_style), Paragraph("0", table_cell_center), Paragraph("0", table_cell_center), Paragraph("0", table_cell_center)],
        [Paragraph("Filas duplicadas", table_cell_style), Paragraph("0", table_cell_center), Paragraph("0", table_cell_center), Paragraph("0", table_cell_center)],
        [Paragraph("Variables de texto categóricas", table_cell_style), Paragraph("3 (técnica, tela, compl.)", table_cell_center), Paragraph("3 (texto descriptivo)", table_cell_center), Paragraph("0 (binarizadas a 1/0)", table_cell_center)],
        [Paragraph("Columnas identificadoras", table_cell_style), Paragraph("Incluidas (<code>id, prenda</code>)", table_cell_center), Paragraph("Conservadas", table_cell_center), Paragraph("Eliminadas (sin poder predictivo)", table_cell_center)]
    ]
    t_ad = Table(antes_despues_data, colWidths=[150, 115, 115, 124])
    t_ad.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_AZUL_PRINCIPAL),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDE_TABLA),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_GRIS_CLARO]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ad)
    story.append(Paragraph("<b>Tabla 1.</b> Comparación de dimensiones e integridad del dataset antes y después del preprocesamiento.", caption_style))

    story.append(Paragraph("3.3. Ingeniería de Características y One-Hot Encoding", h2_style))
    story.append(Paragraph(
        "<b>Creación de variables derivadas:</b> Se formularon dos indicadores determinantes para la evaluación del desempeño:<br/>"
        "1. <code>costo_por_cm2 = precio_cop / area_cm2</code>: Evalúa la tasa de valoración económica por unidad de superficie bordada.<br/>"
        "2. <code>productividad_cm2_hora = area_cm2 / horas_trabajo</code>: Expresa la velocidad de avance artesanal. Mientras en <i>Pata de Cabra</i> "
        "se alcanzan 15.0 cm²/h, en <i>Calado Fino</i> la productividad se reduce drásticamente a 8.4 – 10.4 cm²/h debido al deshilado microscópico.<br/>"
        "<b>Codificación de variables categóricas:</b> Dado que los modelos matemáticos no admiten entradas alfanuméricas directas, "
        "se aplicó <code>pd.get_dummies()</code> sobre <code>tecnica</code> (5 niveles), <code>tela</code> (3 niveles) y <code>complejidad</code> (4 niveles), "
        "evitando cualquier orden arbitrario que pudiera inducir sesgos artificiales en el espacio euclidiano.",
        body_style
    ))

    # Fragmento de código ilustrativo
    code_text = (
        "# Fragmento: preparacion_datos_proyecto.py\n"
        "df['costo_por_cm2'] = (df['precio_cop'] / df['area_cm2']).round(2)\n"
        "df['productividad_cm2_hora'] = (df['area_cm2'] / df['horas_trabajo']).round(2)\n"
        "df_ml = pd.get_dummies(df, columns=['tecnica', 'tela', 'complejidad'], prefix=['tec', 'tela', 'comp'])\n"
        "df_ml = df_ml.drop(columns=['id_pedido', 'prenda'], errors='ignore')\n"
        "df_ml.to_csv('data/pedidos_bordados_preparados_ml.csv', index=False)"
    )
    t_code = Table([[Paragraph(code_text.replace('\n', '<br/>'), code_style)]], colWidths=[504])
    t_code.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F3F4F6')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#9CA3AF')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_code)
    story.append(Paragraph("<b>Fragmento 1.</b> Transformación de datos y codificación One-Hot mediante Pandas.", caption_style))
    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 5: ANÁLISIS VISUAL CON SEABORN
    # ==========================================================================
    story.append(Paragraph("4. Análisis Visual con Seaborn", h1_style))
    story.append(Paragraph(
        "En concordancia con los requisitos de la Clase 7, se construyeron tres visualizaciones estadísticas mediante <b>Seaborn</b> "
        "para sustentar las decisiones de modelado:",
        body_style
    ))

    ruta_g1 = os.path.join(base_dir, 'densidad_precios_seaborn.png')
    ruta_g2 = os.path.join(base_dir, 'boxplot_horas_por_tecnica.png')
    ruta_g3 = os.path.join(base_dir, 'regresion_area_vs_horas.png')

    # Fila con Gráfico 1 y Gráfico 2
    img1 = Image(ruta_g1, width=3.3*inch, height=2.0*inch)
    img2 = Image(ruta_g2, width=3.7*inch, height=2.0*inch)
    t_imgs = Table([[img1, img2]], colWidths=[245, 259])
    t_imgs.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_imgs)

    story.append(Table([
        [
            Paragraph("<b>Figura 1.</b> Densidad KDE de precios (COP). <i>Muestra una distribución bimodal: un segmento denso en prendas personales ($150k–$350k) y otro en manteles de gran formato ($850k). Decisión: El modelo no debe emplear un sesgo uniforme, sino ponderar fuertemente el formato y la tela.</i>", caption_style),
            Paragraph("<b>Figura 2.</b> Dispersión de horas por técnica tradicional. <i>Evidencia que el Calado Fino presenta una mediana de 46 h y alta dispersión (hasta 115 h), casi triplicando a Pata de Cabra y Punto de Cruz. Decisión: La técnica artesanal es el predictor de mayor peso cualitativo.</i>", caption_style)
        ]
    ], colWidths=[245, 259], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))

    story.append(Spacer(1, 4))
    # Gráfico 3 (Relación Entrada vs Objetivo)
    img3 = Image(ruta_g3, width=4.2*inch, height=2.4*inch)
    story.append(Table([[img3]], colWidths=[504], style=[('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(Paragraph(
        "<b>Figura 3.</b> Dispersión y recta de regresión entre Área del Bordado (cm²) y Horas de Trabajo Requeridas. "
        "<i>Muestra una correlación positiva lineal directa altamente consistente (r ≈ 0.88). A mayor área neta, las horas de confección manual "
        "se incrementan monótonamente. Decisión del proyecto: Ratifica que el área es la variable cuantitativa base más sólida para estimar el esfuerzo, "
        "justificando el empleo de modelos de regresión lineal y de árboles en la etapa final.</i>",
        caption_style
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 6 y 7: PERCEPTRÓN DESDE CERO (CLASES 8 Y 9)
    # ==========================================================================
    story.append(Paragraph("5. Primer Modelo de Inteligencia Artificial: Perceptrón desde Cero", h1_style))
    story.append(Paragraph(
        "Atendiendo a la actividad independiente de la Clase 9 y el Requisito D de la guía, se programó en <code>src/perceptron_proyecto.py</code> "
        "una neurona artificial simple unicapa entrenada mediante <b>descenso del gradiente en lote (Batch Gradient Descent)</b> "
        "utilizando exclusivamente <b>NumPy puro</b>, sin recurrir a frameworks preconstruidos (como Scikit-Learn o PyTorch).",
        body_style
    ))

    story.append(Paragraph("5.1. Formulación Matemática y Arquitectura", h2_style))
    story.append(Paragraph(
        "<b>Variable objetivo binaria ($y \in \{0, 1\}$):</b> Dado que el perceptrón clásico resuelve problemas de clasificación binaria, "
        "se definió la variable <code>alta_dedicacion</code> a partir de la mediana de las horas de confección ($29.0\text{ h}$):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• $y^{(i)} = 1$ si $\\text{horas\\_trabajo}^{(i)} \\ge 29.0\\text{ h}$ (Prenda de Alta Dedicación Temporal).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• $y^{(i)} = 0$ si $\\text{horas\\_trabajo}^{(i)} < 29.0\\text{ h}$ (Prenda de Dedicación Estándar / Ligera).<br/>"
        "<i>Justificación metodológica:</i> La mediana divide al conjunto exactamente en <b>10 muestras de clase 0 y 10 muestras de clase 1</b>, "
        "garantizando un balance perfecto que evita el sesgo por clases desbalanceadas. Asimismo, <b>ni las horas ni el precio se incluyen "
        "en las entradas</b> del modelo, previniendo fuga de información (*data leakage*).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Variables de entrada continuas y escalado:</b> Se seleccionaron las dos características físicas conocidas previamente a la confección: "
        "la superficie ($x_1 = \\text{area\\_cm2}$) y el consumo de insumo ($x_2 = \\text{madejas\\_hilo}$). Se aplicó estandarización $Z$-score:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;$$x_{\\text{std}} = \\frac{x - \\mu}{\\sigma}, \\quad \\text{con } \\mu_{\\text{área}}=434.5, \\, \\sigma_{\\text{área}}=266.6, \\, \\mu_{\\text{hilo}}=4.8, \\, \\sigma_{\\text{hilo}}=2.9$$",
        body_style
    ))
    story.append(Paragraph(
        "<b>Ecuaciones del modelo:</b><br/>"
        "1. Combinación lineal: $z^{(i)} = w_1 x_{1,\\text{std}}^{(i)} + w_2 x_{2,\\text{std}}^{(i)} + b$<br/>"
        "2. Función de activación sigmoide: $\\hat{y}^{(i)} = \\sigma(z^{(i)}) = \\frac{1}{1 + e^{-z^{(i)}}}$ (interpretable como probabilidad a posteriori).<br/>"
        "3. Función de pérdida logarítmica (Binary Cross-Entropy):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;$$L(w_1, w_2, b) = -\\frac{1}{N} \\sum_{i=1}^N \\left[ y^{(i)} \\ln(\\hat{y}^{(i)}) + (1 - y^{(i)}) \\ln(1 - \\hat{y}^{(i)}) \\right]$$<br/>"
        "4. Gradientes analíticos deducidos por regla de la cadena y actualización con $\\alpha = 0.1$:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;$$w_j \\leftarrow w_j - \\alpha \\frac{\\partial L}{\\partial w_j}, \\quad b \\leftarrow b - \\alpha \\frac{\\partial L}{\\partial b}, \\quad \\text{donde } \\frac{\\partial L}{\\partial w_j} = \\frac{1}{N} \\sum_{i=1}^N (\\hat{y}^{(i)} - y^{(i)}) x_j^{(i)}$$",
        body_style
    ))

    story.append(Paragraph("5.2. Resultados Cuantitativos del Entrenamiento", h2_style))
    story.append(Paragraph(
        "El modelo se entrenó durante 1.000 épocas a partir de pesos iniciales nulos ($w_1=0, w_2=0, b=0$). "
        "A continuación se presenta la evolución progresiva del aprendizaje:",
        body_style
    ))

    res_entrenamiento = [
        [Paragraph("<b>Hito / Época</b>", table_header_style), Paragraph("<b>Pérdida Logarítmica</b>", table_header_style), Paragraph("<b>Exactitud (%)</b>", table_header_style), Paragraph("<b>Peso w₁ (Área)</b>", table_header_style), Paragraph("<b>Peso w₂ (Madejas)</b>", table_header_style), Paragraph("<b>Sesgo (b)</b>", table_header_style)],
        [Paragraph("Época 1 (Inicial)", table_cell_style), Paragraph("0.6931", table_cell_center), Paragraph("50.0 %", table_cell_center), Paragraph("+0.034", table_cell_center), Paragraph("+0.034", table_cell_center), Paragraph("0.000", table_cell_center)],
        [Paragraph("Época 200", table_cell_style), Paragraph("0.2407", table_cell_center), Paragraph("90.0 %", table_cell_center), Paragraph("+1.713", table_cell_center), Paragraph("+1.770", table_cell_center), Paragraph("+0.524", table_cell_center)],
        [Paragraph("Época 400", table_cell_style), Paragraph("0.1890", table_cell_center), Paragraph("90.0 %", table_cell_center), Paragraph("+2.362", table_cell_center), Paragraph("+2.406", table_cell_center), Paragraph("+0.956", table_cell_center)],
        [Paragraph("Época 600", table_cell_style), Paragraph("0.1634", table_cell_center), Paragraph("95.0 %", table_cell_center), Paragraph("+2.837", table_cell_center), Paragraph("+2.838", table_cell_center), Paragraph("+1.265", table_cell_center)],
        [Paragraph("Época 800", table_cell_style), Paragraph("0.1474", table_cell_center), Paragraph("95.0 %", table_cell_center), Paragraph("+3.224", table_cell_center), Paragraph("+3.170", table_cell_center), Paragraph("+1.508", table_cell_center)],
        [Paragraph("Época 1.000 (Final)", table_cell_style), Paragraph("<b>0.1361</b>", table_cell_center), Paragraph("<b>100.0 %</b>", table_cell_center), Paragraph("<b>+3.557</b>", table_cell_center), Paragraph("<b>+3.442</b>", table_cell_center), Paragraph("<b>+1.710</b>", table_cell_center)]
    ]
    t_res = Table(res_entrenamiento, colWidths=[100, 80, 80, 80, 80, 84])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_AZUL_PRINCIPAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDE_TABLA),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_GRIS_CLARO]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_res)
    story.append(Paragraph("<b>Tabla 2.</b> Dinámica de convergencia del perceptrón a lo largo de 1.000 épocas de optimización.", caption_style))

    story.append(PageBreak())

    # Gráficos del Perceptrón en Página 7
    story.append(Paragraph("5.3. Visualización de la Curva de Aprendizaje y Frontera de Decisión", h2_style))
    ruta_curva = os.path.join(base_dir, 'curva_aprendizaje_perceptron.png')
    ruta_front = os.path.join(base_dir, 'frontera_decision_perceptron.png')

    img_curva = Image(ruta_curva, width=3.4*inch, height=2.1*inch)
    img_front = Image(ruta_front, width=3.6*inch, height=2.1*inch)

    t_mod_imgs = Table([[img_curva, img_front]], colWidths=[245, 259])
    t_mod_imgs.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(t_mod_imgs)

    story.append(Table([
        [
            Paragraph("<b>Figura 4.</b> Curva de aprendizaje del perceptrón. <i>Ilustra el descenso asintótico monotónico de la función de pérdida (de 0.6931 a 0.1361) y la consolidación de la exactitud hasta el 100% sin divergencia numérica.</i>", caption_style),
            Paragraph("<b>Figura 5.</b> Frontera de decisión lineal en el plano estandarizado. <i>La recta w₁x₁ + w₂x₂ + b = 0 separa perfectamente las prendas estándar (azul) de las piezas de alta dedicación (rojo), delimitando la región de probabilidad ≥ 0.5.</i>", caption_style)
        ]
    ], colWidths=[245, 259], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))

    story.append(Paragraph("5.4. Interpretación de Pesos y Análisis de Dominio Artesanal", h2_style))
    story.append(Paragraph(
        "• <b>Significado del signo positivo de los pesos ($w_1 = +3.557, \\, w_2 = +3.442$):</b> En el formalismo de la regresión logística, "
        "el incremento de una unidad estandarizada en el área superficial o en el número de madejas multiplica el momio (*odds ratio*) "
        "de pertenecer a la clase de alta dedicación por $e^{3.557} \\approx 35.1$ y $e^{3.442} \\approx 31.2$, respectivamente. "
        "Esto valida el principio de que piezas más extensas y de mayor densidad de puntadas requieren inevitablemente mayor tiempo de labor.<br/>"
        "• <b>Separabilidad lineal:</b> En el espacio bidimensional de las dos variables cuantitativas escaladas, la condición binaria de dedicación "
        "resultó ser <b>linealmente separable</b> para las 20 muestras analizadas, permitiendo que un hiperplano simple clasifique el 100% de los casos.<br/>"
        "• <b>Limitaciones del modelo unicapa y justificación del modelo final:</b> Aunque el perceptrón clasificó exitosamente la dedicación binaria, "
        "una neurona simple con sigmoide <b>no puede estimar el valor continuo exacto en horas ni el precio monetario en pesos</b>. "
        "Asimismo, ignora las interacciones complejas con las variables cualitativas (por ejemplo, un calado fino sobre seda exige cuidados que "
        "un modelo lineal unicapa simplifica en exceso). Esto fundamenta el avance hacia algoritmos de regresión múltiple en el tercer corte.",
        body_style
    ))
    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 8: PLAN HACIA EL PROYECTO FINAL Y REFERENCIAS
    # ==========================================================================
    story.append(Paragraph("6. Plan hacia el Proyecto Final (Tercer Corte)", h1_style))
    story.append(Paragraph(
        "<b>6.1. Definición del problema:</b> El sistema final se consolidará como un modelo de <b>REGRESIÓN SUPERVISADA MULTIVARIABLE</b> "
        "capaz de generar predicciones continuas para dos variables de respuesta: <code>horas_trabajo</code> ($\hat{y}_1$) y <code>precio_cop</code> ($\hat{y}_2$).<br/>"
        "<b>6.2. Modelos de Scikit-Learn a comparar (Clase 12 – 9 de noviembre):</b> Se implementará una batería de evaluación sistemática con:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. <i>Regresión Lineal Múltiple con Regularización Ridge/Lasso:</i> Modelo de referencia base (línea base).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. <i>Árboles de Decisión para Regresión (DecisionTreeRegressor):</i> Captura de reglas no lineales del tipo técnica-tela.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. <i>Bosques Aleatorios (RandomForestRegressor):</i> Ensamble por embolsado (*bagging*) para reducir la varianza.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;4. <i>Gradient Boosting Regressor:</i> Optimización iterativa por gradiente boosting sobre residuos.<br/>"
        "<b>6.3. Métricas de selección:</b> Se priorizará el <b>Error Absoluto Medio (MAE)</b> expresado en horas y pesos colombianos, "
        "debido a su interpretabilidad directa para las artesanas; complementado con el <b>Coeficiente de Determinación ($R^2$)</b> "
        "(esperando un valor objetivo $R^2 \\ge 0.88$) y el <b>RMSE</b> para penalizar desvíos extremos en prendas suntuarias.<br/>"
        "<b>6.4. Demostración final:</b> Se desarrollará una interfaz interactiva de cotización en donde la bordadora ingrese el tipo de prenda, "
        "la técnica, la tela y las dimensiones estimadas, recibiendo en tiempo real el rango de tiempo de confección y el valor sugerido de cobro.",
        body_style
    ))

    story.append(Paragraph("6.5. Cronograma de Trabajo hacia la Sustentación Final", h2_style))
    cronograma_data = [
        [Paragraph("<b>Período / Hito</b>", table_header_style), Paragraph("<b>Actividad Técnica</b>", table_header_style), Paragraph("<b>Responsable y Entregable</b>", table_header_style)],
        [Paragraph("26 Oct – 08 Nov", table_cell_style), Paragraph("Entrenamiento y validación cruzada (K-Fold) de algoritmos Scikit-Learn.", table_cell_style), Paragraph("D. Cruz / Script comparativo", table_cell_style)],
        [Paragraph("09 de Noviembre", table_cell_style), Paragraph("<b>Clase 12:</b> Sesión de laboratorio, ajuste de hiperparámetros y selección del modelo ganador.", table_cell_style), Paragraph("Grupo 02 / Tabla de métricas", table_cell_style)],
        [Paragraph("10 Nov – 22 Nov", table_cell_style), Paragraph("Construcción del módulo demostrativo interactivo y redacción del informe final (normas APA).", table_cell_style), Paragraph("J. D. Zapata / Documento final", table_cell_style)],
        [Paragraph("23 / 30 Noviembre", table_cell_style), Paragraph("<b>Sustentación Final:</b> Presentación en vivo del sistema ante docente y jurados.", table_cell_style), Paragraph("Davison Cruz & Juan Diego Zapata", table_cell_style)]
    ]
    t_crono = Table(cronograma_data, colWidths=[100, 240, 164])
    t_crono.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_AZUL_PRINCIPAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDE_TABLA),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_GRIS_CLARO]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_crono)

    story.append(Spacer(1, 4))
    story.append(Paragraph("7. Referencias Bibliográficas", h1_style))
    refs = [
        "Artesanías de Colombia. (2020). <i>Caracterización de la técnica tradicional del calado y bordado de Cartago</i>. Ministerio de Comercio, Industria y Turismo.",
        "Cano Sánchez, J. J. (2026). <i>Material de Clases 7, 8 y 9: Pandas, Seaborn, Neuronas Artificiales y Descenso del Gradiente</i>. Facultad de Ingeniería, COTECNOVA.",
        "McKinney, W. (2022). <i>Python for Data Analysis: Data Wrangling with pandas, NumPy, and Jupyter</i> (3rd ed.). O'Reilly Media.",
        "Minsky, M., & Papert, S. (1969). <i>Perceptrons: An Introduction to Computational Geometry</i>. MIT Press.",
        "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., ... & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. <i>Journal of Machine Learning Research</i>, 12, 2825-2830.",
        "Rosenblatt, F. (1958). The perceptron: A probabilistic model for information storage and organization in the brain. <i>Psychological Review</i>, 65(6), 386–408."
    ]
    for r in refs:
        story.append(Paragraph(f"• {r}", ParagraphStyle('Ref', parent=body_style, fontSize=8, leading=11, leftIndent=12)))

    story.append(PageBreak())

    # ==========================================================================
    # PÁGINA 9: ANEXOS (ENLACES Y GUION DEL VIDEO)
    # ==========================================================================
    story.append(Paragraph("8. Anexos y Enlaces de Sustentación", h1_style))
    story.append(Paragraph(
        "En concordancia con los requisitos de entrega de la plataforma AVACO, se relacionan los accesos a los entregables complementarios:",
        body_style
    ))

    story.append(Paragraph("<b>Enlace al Repositorio Oficial de GitHub:</b><br/>"
                           "<font color='#182B49'><u>https://github.com/Cruz1905/curso-inteligencia-artificial</u></font>", bullet_style))
    story.append(Paragraph("<b>Enlace al Video de Sustentación (máximo 10 minutos):</b><br/>"
                           "<i>[Pega aquí el enlace de YouTube / Google Drive / OneDrive con permiso de acceso público]</i>", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("8.1. Guion y Estructura del Video de Sustentación (0:00 – 10:00)", h2_style))
    story.append(Paragraph(
        "Para garantizar una grabación organizada y sin exceder el límite reglamentario de 10 minutos, los estudiantes seguirán la siguiente pauta:",
        body_style
    ))

    guion_data = [
        [Paragraph("<b>Momento</b>", table_header_style), Paragraph("<b>Tiempo</b>", table_header_style), Paragraph("<b>Responsable y Temática Específica</b>", table_header_style)],
        [
            Paragraph("1. Presentación", table_cell_style),
            Paragraph("0:00 – 1:30<br/>(1.5 min)", table_cell_center),
            Paragraph("<b>Davison Cruz y Juan Diego Zapata:</b> Saludo, presentación individual en cámara/voz, nombre del proyecto, problemática en Cartago (cobro empírico) y objetivo del sistema de IA.", table_cell_style)
        ],
        [
            Paragraph("2. Datos y Limpieza", table_cell_style),
            Paragraph("1:30 – 3:45<br/>(2.25 min)", table_cell_center),
            Paragraph("<b>Davison Cruz:</b> Proyectar VSCode con <code>data/pedidos_bordados.csv</code> y <code>preparacion_datos_proyecto.py</code>. Explicar diagnóstico de 0 nulos, columnas derivadas y One-Hot Encoding.", table_cell_style)
        ],
        [
            Paragraph("3. Visualización", table_cell_style),
            Paragraph("3:45 – 5:30<br/>(1.75 min)", table_cell_center),
            Paragraph("<b>Juan Diego Zapata:</b> Mostrar los 3 gráficos de Seaborn (KDE de precios, Boxplot de técnica y Regresión de área vs horas). Resaltar que el Calado Fino triplica el tiempo artesanal.", table_cell_style)
        ],
        [
            Paragraph("4. Perceptrón en Vivo", table_cell_style),
            Paragraph("5:30 – 7:15<br/>(1.75 min)", table_cell_center),
            Paragraph("<b>Davison Cruz:</b> Abrir la terminal de Docker (prompt <code>root@...:/app#</code>), navegar a <code>proyecto/src</code> y ejecutar <code>python perceptron_proyecto.py</code>. Explicar el descenso de pérdida (0.6931 → 0.1361), la exactitud del 100% y mostrar la gráfica de frontera de decisión.", table_cell_style)
        ],
        [
            Paragraph("5. Próximos Pasos", table_cell_style),
            Paragraph("7:15 – 9:45<br/>(2.5 min)", table_cell_center),
            Paragraph("<b>Juan Diego Zapata y Davison Cruz:</b> Justificar por qué el modelo final es de Regresión, modelos Scikit-Learn a comparar (Clase 12), métrica MAE y cierre formal de la sustentación.", table_cell_style)
        ]
    ]
    t_guion = Table(guion_data, colWidths=[90, 75, 339])
    t_guion.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_AZUL_PRINCIPAL),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDE_TABLA),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_GRIS_CLARO]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_guion)

    # Construir el documento PDF utilizando NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Documento PDF generado exitosamente en: {ruta_pdf_proyecto}")

    # Copiar también a la carpeta IA de Documentos
    import shutil
    try:
        shutil.copyfile(ruta_pdf_proyecto, ruta_pdf_documentos)
        print(f"[+] Copia guardada en Documentos/Davison/IA: {ruta_pdf_documentos}")
    except Exception as e:
        print(f"[-] No se pudo copiar a Documentos: {e}")

if __name__ == '__main__':
    generar_pdf()
