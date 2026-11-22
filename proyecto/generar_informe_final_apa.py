"""
generar_informe_final_apa.py
Generador del Informe Final del Proyecto de Inteligencia Artificial (Tercer Corte - 40%)
Cumple rigurosamente con los lineamientos oficiales de COTECNOVA (2026-02) y la 7.ª edición de Normas APA:
- Formato carta con márgenes de 2.54 cm (1 pulgada / 72 pt) en los cuatro lados.
- Tipografía Times New Roman (Times-Roman) 12 pt con interlineado doble (leading de 24 pt).
- Texto alineado a la izquierda (sin justificar) con sangría de 1.27 cm (0.5 in / 36 pt) en la primera línea.
- Numeración en la esquina superior derecha desde la portada.
- Jerarquía de títulos APA (Nivel 1, Nivel 2 y Nivel 3).
- Tablas APA oficiales (sin líneas verticales, solo bordes superior, inferior y subcabecera).
- Figuras con número en negrita, título en cursiva y nota al pie.
- Extensión reglamentaria entre 12 y 20 páginas de contenido.
- Apéndices con enlace a GitHub y Declaración de uso de Inteligencia Artificial.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# ==============================================================================
# CANVAS PERSONALIZADO PARA NUMERACIÓN EN ESQUINA SUPERIOR DERECHA (APA 7)
# ==============================================================================
class APANumberedCanvas(canvas.Canvas):
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
            self.draw_page_decorations()
            super().showPage()
        super().save()

    def draw_page_decorations(self):
        self.saveState()
        # Número de página en la esquina superior derecha (a 1 pulgada del borde superior y derecho)
        self.setFont('Times-Roman', 12)
        self.setFillColor(colors.black)
        # 612 x 792 pt (Letter). Margen derecho a 72 pt (x = 540)
        self.drawRightString(540, 742, str(self._pageNumber))
        self.restoreState()

# ==============================================================================
# CONSTRUCTOR PRINCIPAL DEL INFORME
# ==============================================================================
def construir_informe_apa():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_salida = os.path.join(base_dir, "Informe_Final_Grupo02_BordadosCartago.pdf")
    ruta_docs = os.path.join(base_dir, "docs", "Informe_Final_Grupo02_BordadosCartago.pdf")
    os.makedirs(os.path.dirname(ruta_docs), exist_ok=True)

    # Márgenes estrictos de 1 pulgada (72 pt / 2.54 cm)
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=letter,
        leftMargin=72,
        rightMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Estilos según APA 7 (Times-Roman 12 pt, interlineado doble = 24 pt)
    styles = getSampleStyleSheet()

    # Párrafo estándar APA 7: alineado a la izquierda, interlineado doble, sangría de 36 pt
    p_body = ParagraphStyle(
        'APABody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=24,
        textColor=colors.black,
        alignment=0, # Izquierda (TA_LEFT)
        firstLineIndent=36, # 1.27 cm
        spaceBefore=0,
        spaceAfter=0
    )

    # Párrafo sin sangría (para resumen, notas y títulos iniciales)
    p_body_no_indent = ParagraphStyle(
        'APABodyNoIndent',
        parent=p_body,
        firstLineIndent=0
    )

    # Párrafo para la Portada Estudiantil (centrado, interlineado doble)
    p_cover = ParagraphStyle(
        'APACover',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=24,
        textColor=colors.black,
        alignment=1, # Centrado
        spaceBefore=0,
        spaceAfter=0
    )

    p_cover_bold = ParagraphStyle(
        'APACoverBold',
        parent=p_cover,
        fontName='Times-Bold'
    )

    # Títulos Nivel 1 (Centrado, Negrita, Doble espacio)
    p_h1 = ParagraphStyle(
        'APAH1',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=24,
        textColor=colors.black,
        alignment=1, # Centrado
        spaceBefore=12,
        spaceAfter=0,
        keepWithNext=True
    )

    # Títulos Nivel 2 (Alineado izquierda, Negrita, Doble espacio)
    p_h2 = ParagraphStyle(
        'APAH2',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=24,
        textColor=colors.black,
        alignment=0,
        spaceBefore=12,
        spaceAfter=0,
        keepWithNext=True
    )

    # Títulos Nivel 3 (Alineado izquierda, Negrita y Cursiva)
    p_h3 = ParagraphStyle(
        'APAH3',
        parent=styles['Normal'],
        fontName='Times-BoldItalic',
        fontSize=12,
        leading=24,
        textColor=colors.black,
        alignment=0,
        spaceBefore=12,
        spaceAfter=0,
        keepWithNext=True
    )

    # Estilos de Tablas y Figuras APA
    p_table_num = ParagraphStyle(
        'APATableNum',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=0,
        spaceBefore=12,
        spaceAfter=2,
        keepWithNext=True
    )

    p_table_title = ParagraphStyle(
        'APATableTitle',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=12,
        leading=16,
        alignment=0,
        spaceBefore=0,
        spaceAfter=6,
        keepWithNext=True
    )

    p_table_cell = ParagraphStyle(
        'APATableCell',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=0
    )

    p_table_cell_center = ParagraphStyle(
        'APATableCellCenter',
        parent=p_table_cell,
        alignment=1
    )

    p_table_cell_bold = ParagraphStyle(
        'APATableCellBold',
        parent=p_table_cell,
        fontName='Times-Bold'
    )

    p_note = ParagraphStyle(
        'APANote',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        alignment=0,
        spaceBefore=4,
        spaceAfter=12
    )

    # Referencias con sangría francesa (1.27 cm / 36 pt)
    p_ref = ParagraphStyle(
        'APAReference',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=24,
        alignment=0,
        leftIndent=36,
        firstLineIndent=-36,
        spaceBefore=0,
        spaceAfter=0
    )

    historia = []

    # ==========================================================================
    # PÁGINA 1: PORTADA DE TRABAJO ESTUDIANTIL APA 7 (Sección 3.3)
    # ==========================================================================
    historia.append(Spacer(1, 100))
    historia.append(Paragraph("<b>Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago</b>", p_cover_bold))
    historia.append(Spacer(1, 48))
    historia.append(Paragraph("Davison Cruz López y Juan Diego Zapata Arbeláez", p_cover))
    historia.append(Spacer(1, 48))
    historia.append(Paragraph("Ingeniería de Sistemas, Corporación de Estudios Tecnológicos del Norte del Valle", p_cover))
    historia.append(Paragraph("Inteligencia Artificial", p_cover))
    historia.append(Paragraph("Jhon James Cano Sánchez", p_cover))
    historia.append(Paragraph("22 de noviembre de 2026", p_cover))
    historia.append(PageBreak())

    # ==========================================================================
    # PÁGINA 2: RESUMEN Y PALABRAS CLAVE (Sección 3.1)
    # ==========================================================================
    historia.append(Paragraph("<b>Resumen</b>", p_h1))
    historia.append(Spacer(1, 12))
    resumen_texto = (
        "En el municipio de Cartago, Valle del Cauca, la tasación de prendas y lencería artesanal "
        "bordada se realiza predominantemente mediante estimaciones empíricas desprovistas de soporte "
        "matemático, lo cual genera recurrentes desfases presupuestales y subvaloración del trabajo manual. "
        "El presente proyecto describe el diseño, entrenamiento y evaluación de un sistema de inteligencia "
        "artificial orientado a la predicción cuantitativa del tiempo de confección en horas y a la clasificación "
        "del nivel de dedicación laboral a partir de variables cuantitativas de insumos y dimensiones geométricas. "
        "A partir de una muestra representativa de 20 pedidos locales con 9 características, se efectuó una "
        "depuración con Pandas y se implementó inicialmente un perceptrón simple desde cero con NumPy "
        "empleando activación sigmoide y descenso del gradiente. Posteriormente, se estructuró un flujo "
        "industrial en Scikit-Learn mediante Pipelines y validación cruzada para comparar arquitecturas "
        "de clasificación (Regresión Logística, K-Nearest Neighbors, Árboles de Decisión y Redes Neuronales MLP) "
        "y de regresión múltiple. Como resultado principal, el clasificador logístico obtuvo un F1-Score de 1.0 "
        "en datos de prueba no vistos, mientras que la regresión Ridge alcanzó un coeficiente de determinación "
        "R² de 0.928 y un error absoluto medio (MAE) de apenas 3.58 horas. Se concluye que el modelo lineal "
        "regularizado generaliza adecuadamente la dinámica productiva local, permitiendo estandarizar la "
        "cotización justa del bordado tradicional."
    )
    historia.append(Paragraph(resumen_texto, p_body_no_indent))
    historia.append(Spacer(1, 18))
    historia.append(Paragraph("<i>Palabras clave:</i> aprendizaje automático, bordados de Cartago, perceptrón, regresión Ridge, Scikit-Learn.", p_body_no_indent))
    historia.append(PageBreak())

    # ==========================================================================
    # PÁGINA 3: INTRODUCCIÓN (Sección 3.1)
    # ==========================================================================
    historia.append(Paragraph("<b>Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago</b>", p_h1))
    historia.append(Spacer(1, 12))
    
    p1 = (
        "El municipio de Cartago, situado en el norte del departamento del Valle del Cauca, es "
        "reconocido a nivel nacional e internacional como la Capital Mundial del Bordado. Durante "
        "décadas, esta manifestación artesanal ha constituido uno de los principales motores de identidad "
        "cultural, cohesión comunitaria y sustento socioeconómico para cientos de familias de la región, "
        "especialmente para mujeres cabeza de hogar organizadas en pequeños talleres y unidades productivas "
        "domésticas. Las técnicas tradicionales cartagüeñas, entre las que destacan el calado fino, el rococó, "
        "el punto de sombra, la pata de cabra y el punto de cruz, demandan un elevado grado de precisión "
        "motriz, minuciosidad y extensas jornadas de trabajo manual sobre textiles finos como el lino, el algodón y la seda."
    )
    historia.append(Paragraph(p1, p_body))

    p2 = (
        "A pesar de su invaluable riqueza patrimonial, el sector enfrenta una seria vulnerabilidad en sus "
        "procesos de comercialización y costeo operativo. Históricamente, la tasación de las piezas artesanales "
        "—es decir, la estimación del tiempo que requerirá la confección y la consecuente fijación del precio de venta— "
        "se efectúa de manera puramente subjetiva e intuitiva, basándose en la experiencia informal de la bordadora. "
        "Esta ausencia de criterios estandarizados e instrumentos técnicos conlleva a distorsiones comerciales "
        "sistemáticas: en encargos de alta complejidad geométrica o dimensional, las artesanas suelen subestimar "
        "las horas requeridas, fijando tarifas que ni siquiera cubren el costo de oportunidad de su tiempo, lo cual "
        "deriva en precarización económica, incumplimiento de plazos con clientes y pérdidas de rentabilidad."
    )
    historia.append(Paragraph(p2, p_body))

    p3 = (
        "Frente a este escenario, la aplicación de técnicas contemporáneas de inteligencia artificial y "
        "aprendizaje supervisado ofrece una oportunidad estratégica de modernización y dignificación del oficio. "
        "Al formalizar la relación existente entre las especificaciones objetivas de un encargo (superficie neta a bordar, "
        "consumo de madejas de hilo, técnica y tipo de textil) y las variables de respuesta (horas reales de trabajo "
        "y categorización de complejidad), es factible formular modelos matemáticos capaces de predecir con exactitud "
        "el esfuerzo productivo antes de iniciar la aguja. De este modo, la pregunta central de investigación que "
        "orienta este trabajo es: ¿En qué medida un sistema de aprendizaje automático fundamentado en el ciclo "
        "completo de Machine Learning puede predecir con precisión matemática el tiempo de confección manual y clasificar "
        "la complejidad de pedidos de bordado tradicional en Cartago?"
    )
    historia.append(Paragraph(p3, p_body))

    p4 = (
        "El presente informe documenta de manera integral el desarrollo, implementación y validación empírica "
        "del sistema propuesto. Se aborda la totalidad del ciclo metodológico exigido por la asignatura: desde la "
        "construcción y depuración del conjunto de datos representativo mediante la biblioteca Pandas, pasando por el "
        "desarrollo conceptual y algorítmico de un perceptrón simple construido línea por línea en NumPy puro, hasta la "
        "adopción de la suite industrial Scikit-Learn con esquemas de partición rigurosa, Pipelines de estandarización, "
        "validación cruzada y serialización del modelo en un archivo para inferencia en tiempo real dentro de un contenedor Docker."
    )
    historia.append(Paragraph(p4, p_body))

    # ==========================================================================
    # PÁGINA 4-5: OBJETIVOS
    # ==========================================================================
    historia.append(Paragraph("<b>Objetivos</b>", p_h1))
    historia.append(Spacer(1, 12))

    historia.append(Paragraph("<b>Objetivo General</b>", p_h2))
    obj_gen = (
        "Desarrollar, entrenar y evaluar un sistema de inteligencia artificial fundamentado en modelos de "
        "clasificación y regresión supervisada, capaz de estimar las horas de labor artesanal y categorizar la "
        "complejidad de pedidos de bordado tradicional en Cartago, Valle del Cauca, mediante el uso integrado de "
        "NumPy, Pandas y Scikit-Learn dentro de un entorno contenerizado reproducible."
    )
    historia.append(Paragraph(obj_gen, p_body))

    historia.append(Paragraph("<b>Objetivos Específicos</b>", p_h2))
    obj_esp1 = (
        "1. Estructurar y depurar un conjunto de datos representativo de 20 piezas artesanales de talleres locales "
        "de Cartago mediante Pandas, aplicando ingeniería de características para derivar métricas de productividad "
        "y codificación numérica de variables categóricas."
    )
    historia.append(Paragraph(obj_esp1, p_body))

    obj_esp2 = (
        "2. Construir e implementar desde cero con NumPy un modelo de perceptrón con función de activación sigmoide "
        "y optimización por descenso del gradiente, interpretando analíticamente los pesos sinápticos aprendidos y su "
        "correspondiente frontera de decisión lineal."
    )
    historia.append(Paragraph(obj_esp2, p_body))

    obj_esp3 = (
        "3. Entrenar y comparar múltiples algoritmos de clasificación y regresión en Scikit-Learn utilizando Pipelines "
        "con escalado estándar, partición estratificada de entrenamiento y prueba, y validación cruzada en 5 pliegues, "
        "seleccionando los mejores estimadores según métricas F1-Score y R²."
    )
    historia.append(Paragraph(obj_esp3, p_body))

    obj_esp4 = (
        "4. Persistir los modelos optimizados mediante la librería Joblib y construir un script de inferencia en tiempo "
        "real que permita tasar nuevos encargos de bordado de forma instantánea, garantizando la reproducibilidad técnica "
        "mediante Docker Compose."
    )
    historia.append(Paragraph(obj_esp4, p_body))

    # ==========================================================================
    # PÁGINAS 5-7: MARCO TEÓRICO (Sección 3.1)
    # ==========================================================================
    historia.append(Paragraph("<b>Marco Teórico</b>", p_h1))
    historia.append(Spacer(1, 12))

    t1 = (
        "El aprendizaje automático o Machine Learning constituye un subcampo fundamental de la inteligencia "
        "artificial enfocado en la concepción de algoritmos capaces de extraer patrones representativos a partir de "
        "la experiencia empírica sin requerir programación explícita de reglas lógicas (Russell & Norvig, 2020). "
        "Dentro del paradigma del aprendizaje supervisado, cada observación del conjunto de datos se compone de un "
        "vector de características de entrada X y una etiqueta objetivo y observada en el mundo real. Dependiendo de "
        "la naturaleza matemática de dicha etiqueta, el problema se clasifica como una tarea de clasificación binaria "
        "o multiclase cuando y toma valores discretos, o como una tarea de regresión cuando la variable dependiente "
        "es continua (Müller & Guido, 2016)."
    )
    historia.append(Paragraph(t1, p_body))

    historia.append(Paragraph("<b>El Perceptrón y la Neurona Artificial</b>", p_h2))
    t2 = (
        "La génesis computacional del conexionismo moderno se remonta al modelo fundacional del perceptrón simple "
        "introducido por Rosenblatt (1958). Conceptualmente, una neurona artificial opera recibiendo un conjunto de "
        "entradas ponderadas por pesos sinápticos que representan la importancia relativa de cada factor en la decisión "
        "final. Matemáticamente, el potencial de activación z se define como la combinación lineal de las entradas "
        "más un término de sesgo o bias b: z = w1 x1 + w2 x2 + ... + wn xn + b = X w + b. "
        "En el contexto de este proyecto, x1 simboliza el área superficial en centímetros cuadrados bordados, mientras "
        "que x2 representa las madejas de hilo empleadas. Como señalan Goodfellow et al. (2016), el sesgo b desempeña "
        "un papel imprescindible al permitir desplazar el hiperplano de corte respecto al origen de coordenadas, dotando "
        "al estimador de la flexibilidad geométrica requerida para ajustarse al umbral de clasificación."
    )
    historia.append(Paragraph(t2, p_body))

    t3 = (
        "Para transformar la combinación lineal continua z en una interpretación de probabilidad acotada entre 0 y 1, "
        "se introduce la función de activación sigmoide logística: sigma(z) = 1 / (1 + e^-z). "
        "A diferencia de las funciones de escalón unitario primitivas, la sigmoide es estrictamente suave, diferenciable "
        "y presenta una derivada analítica sumamente conveniente: sigma'(z) = sigma(z) * (1 - sigma(z)). "
        "Esta propiedad matemática resulta decisiva para aplicar métodos de optimización basados en cálculo diferencial, "
        "toda vez que permite calcular gradientes exactos de la función de costo con respecto a los pesos sinápticos."
    )
    historia.append(Paragraph(t3, p_body))

    historia.append(Paragraph("<b>Función de Pérdida Logarítmica y Descenso del Gradiente</b>", p_h2))
    t4 = (
        "La evaluación cuantitativa del error cometido por la neurona se rige por la función de pérdida logarítmica, "
        "conocida en la literatura científica como entropía cruzada binaria o Binary Cross-Entropy Loss (Géron, 2022). "
        "Para un conjunto de N muestras de entrenamiento, la función de pérdida L(w, b) se formula formalmente como: "
        "L = -1/N * sum(y * ln(y_hat) + (1 - y) * ln(1 - y_hat)), donde y denota la etiqueta binaria real (0 o 1) y "
        "y_hat representa la probabilidad predicha sigma(z). Esta función penaliza de manera asintótica las predicciones "
        "erróneas de alta confianza (por ejemplo, predecir una probabilidad de 0.01 cuando la clase real es 1)."
    )
    historia.append(Paragraph(t4, p_body))

    t5 = (
        "La actualización iterativa de los parámetros del modelo se ejecuta mediante el algoritmo de descenso del "
        "gradiente en lote (Batch Gradient Descent). En cada época de entrenamiento t, se computan los gradientes "
        "analíticos del costo respecto a cada peso y sesgo: dL/dw = 1/N * X^T (y_hat - y) y dL/db = 1/N * sum(y_hat - y). "
        "Posteriormente, los pesos se ajustan en sentido opuesto a la máxima pendiente a través de una tasa de "
        "aprendizaje alfa: w^(t+1) = w^(t) - alfa * dL/dw y b^(t+1) = b^(t) - alfa * dL/db. "
        "Si alfa es demasiado pequeña, la convergencia es lenta; si es desmedidamente grande, el algoritmo puede oscilar "
        "y divergir numéricamente (Géron, 2022)."
    )
    historia.append(Paragraph(t5, p_body))

    historia.append(Paragraph("<b>Limitaciones del Perceptrón Monocapa y el Problema XOR</b>", p_h2))
    t6 = (
        "Una de las conclusiones teóricas más relevantes abordadas en la asignatura es la demostrada por Minsky y Papert "
        "en 1969 respecto a la incapacidad fundamental del perceptrón simple para resolver problemas que no sean linealmente "
        "separables, como la compuerta lógica XOR. Dado que una neurona individual genera una frontera de decisión estrictamente "
        "rectilínea en R², cualquier distribución espacial donde las clases alternen diagonalmente resulta inalcanzable. "
        "Para superar esta limitación estructural, es necesario transitar hacia el Perceptrón Multicapa (MLP), el cual incorpora "
        "una o más capas ocultas dotadas de funciones de activación no lineales (como tangente hiperbólica o ReLU), "
        "permitiendo al modelo curvar el espacio geométrico y modelar relaciones no lineales complejas (Goodfellow et al., 2016)."
    )
    historia.append(Paragraph(t6, p_body))

    historia.append(Paragraph("<b>Scikit-Learn, Pipelines y Prevención de Fuga de Información</b>", p_h2))
    t7 = (
        "Scikit-Learn es la biblioteca de código abierto líder en el ecosistema científico de Python para minería de "
        "datos y Machine Learning (Pedregosa et al., 2011). Uno de sus pilares metodológicos es el concepto de Pipeline, "
        "el cual encadena secuencialmente transformadores de datos (como StandardScaler) con un estimador final. "
        "El uso de Pipelines resulta mandatario en la práctica profesional para erradicar la fuga de datos o data leakage: "
        "un error metodológico frecuente en el que parámetros estadísticos del conjunto de prueba (como la media o la "
        "desviación estándar) se filtran inadvertidamente en la etapa de entrenamiento, inflando de manera artificial "
        "las métricas de exactitud y comprometiendo la generalización futura del sistema (Müller & Guido, 2016)."
    )
    historia.append(Paragraph(t7, p_body))

    historia.append(Paragraph("<b>Modelos de Regresión y Métricas de Rendimiento</b>", p_h2))
    t8 = (
        "En la estimación cuantitativa de variables continuas como las horas de trabajo manual, la Regresión Lineal Múltiple "
        "modela la respuesta esperada mediante una combinación lineal ponderada de las variables independientes. No obstante, "
        "cuando las variables explicativas presentan correlaciones moderadas o el conjunto de datos es compacto, los métodos "
        "de mínimos cuadrados ordinarios pueden volverse inestables y propensos al sobreajuste. Para mitigar esta fragilidad, "
        "se recurre a la Regresión Ridge (regularización L2), la cual introduce una penalización proporcional a la norma "
        "euclidiana de los coeficientes: Costo = MSE + alpha * sum(w_j^2). "
        "Esta restricción contrae los pesos hacia cero sin eliminarlos, logrando un balance óptimo entre sesgo y varianza "
        "que mejora la capacidad de predicción con observaciones no vistas (Géron, 2022)."
    )
    historia.append(Paragraph(t8, p_body))

    t9 = (
        "Para evaluar la calidad técnica de los modelos, la literatura recomienda métricas complementarias: "
        "en clasificación, la Exactitud (Accuracy), la Precisión (proporción de positivos reales entre los predichos), "
        "el Recall o Sensibilidad (proporción de casos positivos reales capturados) y el F1-Score, que representa la "
        "media armónica entre precisión y recall. En regresión, se cuantifica el Error Absoluto Medio (MAE), la Raíz "
        "del Error Cuadrático Medio (RMSE) y el Coeficiente de Determinación R², el cual mide la proporción de la "
        "varianza de la variable dependiente explicada por el modelo (Pedregosa et al., 2011)."
    )
    historia.append(Paragraph(t9, p_body))

    # ==========================================================================
    # PÁGINAS 8-10: METODOLOGÍA (Sección 3.1)
    # ==========================================================================
    historia.append(Paragraph("<b>Metodología</b>", p_h1))
    historia.append(Spacer(1, 12))

    m1 = (
        "La metodología implementada en este proyecto se organizó rigurosamente a lo largo de las fases formativas "
        "del semestre académico 2026-02, garantizando la trazabilidad integral del ciclo de vida de la ciencia de datos: "
        "adquisición y muestreo empírico de la información, análisis exploratorio y depuración con Pandas, modelado manual "
        "con NumPy, comparación sistemática con Scikit-Learn y persistencia industrial para despliegue contenerizado."
    )
    historia.append(Paragraph(m1, p_body))

    historia.append(Paragraph("<b>Adquisición y Diccionario de Datos</b>", p_h2))
    m2 = (
        "Dada la carencia de repositorios públicos estandarizados sobre el sector artesanal de Cartago, el equipo de trabajo "
        "recolectó de manera directa una muestra estructurada de 20 encargos reales representativos en talleres locales y "
        "talleres familiares. El dataset resultante se almacenó en el archivo data/pedidos_bordados.csv e integra 9 atributos "
        "técnicos que describen las propiedades físicas y operativas de cada pieza:"
    )
    historia.append(Paragraph(m2, p_body))

    # Lista de variables del diccionario
    dict_vars = [
        "• id_pedido: Identificador alfanumérico correlativo del encargo artesanal.",
        "• prenda: Tipología del artículo confeccionado (Guayabera, Blusa, Mantel, Vestido, Tapete, Pañuelo, etc.).",
        "• tecnica: Técnica manual de bordado aplicada (Calado Fino, Punto de Sombra, Rococó, Punto de Cruz, Pata de Cabra).",
        "• tela: Fibra textil de soporte utilizada como base (Lino, Algodón, Seda).",
        "• area_cm2: Superficie neta calculada de la región bordada expresada en centímetros cuadrados (cm²).",
        "• complejidad: Nivel cualitativo de exigencia técnica reportado por la modista (Baja, Media, Alta, Muy Alta).",
        "• madejas_hilo: Cantidad exacta de madejas de hilo de seda o algodón mercerizado consumidas en la pieza.",
        "• horas_trabajo: Variable continua que registra el tiempo real invertido en la confección manual (horas).",
        "• precio_cop: Tarifa económica final en pesos colombianos (COP) facturada al cliente por la prenda."
    ]
    for dv in dict_vars:
        historia.append(Paragraph(dv, p_body_no_indent))

    historia.append(Paragraph("<b>Preparación e Ingeniería de Características con Pandas</b>", p_h2))
    m3 = (
        "Durante la etapa de depuración (Clases 7 y 8), se confirmó la integridad de las 20 observaciones, constatándose "
        "la ausencia total de valores nulos o registros duplicados. Con el propósito de enriquecer la capacidad analítica "
        "del dataset, se formularon dos nuevas variables derivadas con estricto fundamento en la economía de la producción: "
        "el costo por centímetro cuadrado (costo_por_cm2 = precio_cop / area_cm2) y la tasa de productividad artesanal "
        "(productividad_cm2_hora = area_cm2 / horas_trabajo). Asimismo, para habilitar el procesamiento por parte de "
        "algoritmos de Machine Learning, las variables cualitativas tecnica, tela y complejidad se codificaron numéricamente "
        "mediante variables indicadoras (One-Hot Encoding con pd.get_dummies), generando una matriz final de 18 columnas."
    )
    historia.append(Paragraph(m3, p_body))

    historia.append(Paragraph("<b>Implementación del Perceptrón desde Cero (Avance 2)</b>", p_h2))
    m4 = (
        "En la fase intermedia del curso, se programó en el script src/perceptron_proyecto.py una neurona artificial monocapa "
        "sin dependencias de librerías externas de aprendizaje. Para formular la tarea de clasificación binaria, se determinó "
        "como variable objetivo la Alta Dedicación Horaria (alta_dedicacion = 1 si horas_trabajo >= 29.0 h, y 0 en caso contrario), "
        "donde 29.0 horas corresponde a la mediana observada del conjunto de datos, asegurando un balance idóneo de clases (10 contra 10). "
        "Se seleccionaron como entradas predictoras el área superficial del bordado (x1) y el insumo de madejas (x2). "
        "Ambas variables se estandarizaron internamente mediante z = (x - mu) / sigma (mu_area = 434.5 cm², sigma_area = 266.6 cm²; "
        "mu_madejas = 4.8, sigma_madejas = 2.9). El modelo fue entrenado durante 1000 épocas con tasa de aprendizaje alfa = 0.1, "
        "minimizando la pérdida logarítmica mediante descenso del gradiente analítico."
    )
    historia.append(Paragraph(m4, p_body))

    historia.append(Paragraph("<b>Modelado Avanzado con Scikit-Learn y Validación Cruzada (Clase 12)</b>", p_h2))
    m5 = (
        "En consonancia con los lineamientos de la Clase 12, se estructuró el script src/modelo_proyecto.py para migrar hacia "
        "un entorno industrial estandarizado. Se ejecutó una partición rigurosa de los datos reservando el 80% (16 pedidos) para "
        "entrenamiento y el 20% restante (4 pedidos) para prueba independiente no vista, utilizando random_state=42 y estratificación "
        "por clases (stratify=y). Para evitar data leakage, cada arquitectura se encapsuló en un Pipeline que integra StandardScaler() "
        "junto con el modelo respectivo. En clasificación, se compararon Regresión Logística, KNN (k=3), Árbol de Decisión (max_depth=3) "
        "y Red Neuronal MLPClassifier (8, 4 neuronas ocultas), evaluando métricas con validación cruzada en 5 pliegues (k=5). "
        "En regresión, se confrontaron la Regresión Lineal Clásica, Ridge Regression (alpha=1.0), KNN Regressor y Árboles de Regresión, "
        "optimizando la minimización del MAE y la maximización del R²."
    )
    historia.append(Paragraph(m5, p_body))

    historia.append(Paragraph("<b>Entorno de Ejecución Contenerizado con Docker</b>", p_h2))
    m6 = (
        "Para certificar la reproducibilidad absoluta de los experimentos en cualquier plataforma informática, se diseñó un "
        "contenedor Docker fundamentado en la imagen base oficial python:3.12-slim. Mediante el archivo docker-compose.yml, se "
        "orquesta el servicio bajo el nombre de contenedor ia_python, montando el directorio local del proyecto como un volumen "
        "de trabajo interactivo e instalando las dependencias científicas requeridas (numpy, pandas, matplotlib, seaborn, scikit-learn y joblib)."
    )
    historia.append(Paragraph(m6, p_body))

    # ==========================================================================
    # PÁGINAS 11-13: RESULTADOS (Sección 3.1)
    # ==========================================================================
    historia.append(Paragraph("<b>Resultados</b>", p_h1))
    historia.append(Spacer(1, 12))

    r1 = (
        "Los experimentos computacionales suministraron evidencia cuantitativa concluyente respecto al comportamiento "
        "de las variables y el desempeño de los modelos de inteligencia artificial implementados."
    )
    historia.append(Paragraph(r1, p_body))

    # Tabla 1: Estadísticas descriptivas
    historia.append(Paragraph("<b>Tabla 1</b>", p_table_num))
    historia.append(Paragraph("<i>Estadísticas Descriptivas de las Variables Principales de los Bordados de Cartago</i>", p_table_title))
    
    tabla_1_datos = [
        [Paragraph("<b>Variable</b>", p_table_cell_bold), Paragraph("<b>Media</b>", p_table_cell_bold), Paragraph("<b>Mediana</b>", p_table_cell_bold), Paragraph("<b>Desv. Est.</b>", p_table_cell_bold), Paragraph("<b>Mínimo</b>", p_table_cell_bold), Paragraph("<b>Máximo</b>", p_table_cell_bold)],
        [Paragraph("Área bordada (cm²)", p_table_cell), Paragraph("434.50", p_table_cell_center), Paragraph("365.00", p_table_cell_center), Paragraph("273.53", p_table_cell_center), Paragraph("80.00", p_table_cell_center), Paragraph("1200.00", p_table_cell_center)],
        [Paragraph("Insumo de madejas", p_table_cell), Paragraph("4.75", p_table_cell_center), Paragraph("4.00", p_table_cell_center), Paragraph("3.02", p_table_cell_center), Paragraph("1.00", p_table_cell_center), Paragraph("14.00", p_table_cell_center)],
        [Paragraph("Horas de confección (h)", p_table_cell), Paragraph("37.30", p_table_cell_center), Paragraph("29.00", p_table_cell_center), Paragraph("24.43", p_table_cell_center), Paragraph("9.50", p_table_cell_center), Paragraph("115.00", p_table_cell_center)],
        [Paragraph("Precio cobrado (COP)", p_table_cell), Paragraph("$287,500", p_table_cell_center), Paragraph("$230,000", p_table_cell_center), Paragraph("$181,490", p_table_cell_center), Paragraph("$85,000", p_table_cell_center), Paragraph("$850,000", p_table_cell_center)],
    ]
    t1_elem = Table(tabla_1_datos, colWidths=[150, 60, 60, 65, 60, 65])
    t1_elem.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    historia.append(t1_elem)
    historia.append(Paragraph("<i>Nota.</i> Datos extraídos de la muestra de 20 pedidos representativos recolectados en talleres de Cartago (N = 20).", p_note))

    # Resultados del perceptrón hecho a mano
    historia.append(Paragraph("<b>Desempeño del Perceptrón desde Cero (NumPy Puro)</b>", p_h2))
    r2 = (
        "Durante el entrenamiento de 1000 épocas, el perceptrón implementado línea por línea demostró una convergencia "
        "monotónica estable. La función de pérdida logarítmica descendió desde un valor inicial de 0.6931 (azar teórico) "
        "hasta un valor final de 0.1361, logrando una exactitud de entrenamiento del 100.0% (20 aciertos sobre 20 muestras). "
        "Los parámetros sinápticos finales aprendidos fueron: w1 (Área) = +3.5566, w2 (Madejas) = +3.4419 y sesgo b = +1.7104. "
        "El signo positivo de ambos coeficientes corrobora matemáticamente la intuición de las maestras artesanas: tanto la "
        "superficie neta como la densidad de material ejercen una presión incremental directa sobre la probabilidad de que "
        "la pieza sobrepase el umbral de las 29 horas de manufactura."
    )
    historia.append(Paragraph(r2, p_body))

    # Figura 1: Curva y Frontera del Perceptrón
    ruta_curva = os.path.join(base_dir, "curva_aprendizaje_perceptron.png")
    if os.path.exists(ruta_curva):
        historia.append(Paragraph("<b>Figura 1</b>", p_table_num))
        historia.append(Paragraph("<i>Curva de Aprendizaje del Perceptrón con Descenso del Gradiente</i>", p_table_title))
        historia.append(Image(ruta_curva, width=5.5*inch, height=2.8*inch))
        historia.append(Paragraph("<i>Nota.</i> Evolución de la pérdida logarítmica y exactitud a lo largo de 1000 épocas con tasa de aprendizaje alfa = 0.1. Elaboración propia con Matplotlib.", p_note))

    # Resultados de Clasificación en Scikit-Learn
    historia.append(Paragraph("<b>Comparación de Modelos de Clasificación en Scikit-Learn (Clase 12)</b>", p_h2))
    r3 = (
        "La evaluación rigurosa con partición estratificada independiente (80% entrenamiento, 20% prueba no vista) "
        "reveló un excelente comportamiento general de los estimadores lineales y basados en vecindad. "
        "La Tabla 2 sintetiza las métricas obtenidas sobre los 4 pedidos de prueba reservados."
    )
    historia.append(Paragraph(r3, p_body))

    # Tabla 2: Clasificación Scikit-Learn
    historia.append(Paragraph("<b>Tabla 2</b>", p_table_num))
    historia.append(Paragraph("<i>Comparación de Modelos de Clasificación en Conjunto de Prueba y Validación Cruzada</i>", p_table_title))
    
    tabla_2_datos = [
        [Paragraph("<b>Modelo Evaluado</b>", p_table_cell_bold), Paragraph("<b>Exactitud</b>", p_table_cell_bold), Paragraph("<b>Precisión</b>", p_table_cell_bold), Paragraph("<b>Recall</b>", p_table_cell_bold), Paragraph("<b>F1-Score</b>", p_table_cell_bold), Paragraph("<b>Val. Cruzada (k=5)</b>", p_table_cell_bold)],
        [Paragraph("Regresión Logística", p_table_cell), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("0.900", p_table_cell_center)],
        [Paragraph("KNN (k = 3 vecinos)", p_table_cell), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("0.950", p_table_cell_center)],
        [Paragraph("Árbol de Decisión (d = 3)", p_table_cell), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center)],
        [Paragraph("Red Neuronal (MLP)", p_table_cell), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("1.000", p_table_cell_center), Paragraph("0.900", p_table_cell_center)],
    ]
    t2_elem = Table(tabla_2_datos, colWidths=[150, 60, 60, 60, 60, 70])
    t2_elem.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    historia.append(t2_elem)
    historia.append(Paragraph("<i>Nota.</i> Métricas calculadas sobre los 4 lotes de prueba independientes (N_test = 4). Validación cruzada evaluada sobre la totalidad de los datos con k = 5 pliegues.", p_note))

    # Figura 2: Matriz de confusión
    ruta_cm = os.path.join(base_dir, "matriz_confusion_proyecto.png")
    if os.path.exists(ruta_cm):
        historia.append(Paragraph("<b>Figura 2</b>", p_table_num))
        historia.append(Paragraph("<i>Matriz de Confusión del Modelo de Regresión Logística en Datos de Prueba</i>", p_table_title))
        historia.append(Image(ruta_cm, width=4.5*inch, height=3.5*inch))
        historia.append(Paragraph("<i>Nota.</i> Clasificación binaria en prueba: 2 verdaderos negativos y 2 verdaderos positivos, sin falsas alarmas ni omisiones. Elaboración propia con Seaborn.", p_note))

    # Resultados de Regresión en Scikit-Learn
    historia.append(Paragraph("<b>Comparación de Modelos de Regresión Continua (Estimación de Horas)</b>", p_h2))
    r4 = (
        "El objetivo central del sistema radica en cuantificar con exactitud el valor continuo de horas requeridas. "
        "La Tabla 3 contrasta las arquitecturas de regresión múltiple evaluadas."
    )
    historia.append(Paragraph(r4, p_body))

    # Tabla 3: Regresión Scikit-Learn
    historia.append(Paragraph("<b>Tabla 3</b>", p_table_num))
    historia.append(Paragraph("<i>Desempeño de los Modelos de Regresión en la Estimación de Horas de Trabajo</i>", p_table_title))
    
    tabla_3_datos = [
        [Paragraph("<b>Modelo de Regresión</b>", p_table_cell_bold), Paragraph("<b>MAE (horas)</b>", p_table_cell_bold), Paragraph("<b>RMSE (horas)</b>", p_table_cell_bold), Paragraph("<b>R² Score</b>", p_table_cell_bold), Paragraph("<b>Aporte Conceptual</b>", p_table_cell_bold)],
        [Paragraph("Regresión Lineal Múltiple", p_table_cell), Paragraph("4.386", p_table_cell_center), Paragraph("5.370", p_table_cell_center), Paragraph("0.914", p_table_cell_center), Paragraph("Línea base paramétrica", p_table_cell)],
        [Paragraph("<b>Ridge Regression (alfa = 1.0)</b>", p_table_cell), Paragraph("<b>3.584</b>", p_table_cell_center), Paragraph("<b>4.919</b>", p_table_cell_center), Paragraph("<b>0.928</b>", p_table_cell_center), Paragraph("<b>Regularización L2 (Ganador)</b>", p_table_cell)],
        [Paragraph("KNN Regressor (k = 3)", p_table_cell), Paragraph("5.667", p_table_cell_center), Paragraph("7.528", p_table_cell_center), Paragraph("0.831", p_table_cell_center), Paragraph("No paramétrico por proximidad", p_table_cell)],
        [Paragraph("Árbol de Regresión (d = 3)", p_table_cell), Paragraph("7.500", p_table_cell_center), Paragraph("8.712", p_table_cell_center), Paragraph("0.773", p_table_cell_center), Paragraph("Reglas de partición ortogonales", p_table_cell)],
    ]
    t3_elem = Table(tabla_3_datos, colWidths=[140, 65, 65, 60, 130])
    t3_elem.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    historia.append(t3_elem)
    historia.append(Paragraph("<i>Nota.</i> El modelo Ridge Regression superó a las demás arquitecturas alcanzando el mayor R² (0.928) y el menor MAE (3.58 horas). Elaboración propia con Scikit-Learn.", p_note))

    # Figura 3: Real vs Predicho
    ruta_reg_plot = os.path.join(base_dir, "real_vs_predicho_proyecto.png")
    if os.path.exists(ruta_reg_plot):
        historia.append(Paragraph("<b>Figura 3</b>", p_table_num))
        historia.append(Paragraph("<i>Dispersión de Horas Reales vs Horas Estimadas por la Regresión Ridge</i>", p_table_title))
        historia.append(Image(ruta_reg_plot, width=5.0*inch, height=3.8*inch))
        historia.append(Paragraph("<i>Nota.</i> La línea discontinua roja señala la predicción perfecta. La alineación estrecha de los puntos evidencia la consistencia del estimador regularizado. Elaboración propia con Matplotlib.", p_note))

    # Inferencia en tiempo real (usar_modelo.py)
    historia.append(Paragraph("<b>Demostración de Inferencia en Tiempo Real (usar_modelo.py)</b>", p_h2))
    r5 = (
        "Para validar la utilidad del sistema en un entorno de producción, se ejecutó el script de inferencia "
        "cargando los modelos serializados en disco (modelo_clasificacion_bordados.joblib y modelo_regresion_bordados.joblib) "
        "sin requerir reentrenar. Se sometieron a tasación tres casos representativos diseñados conjuntamente con modistas locales:"
    )
    historia.append(Paragraph(r5, p_body))

    # Tabla 4: Inferencia en tiempo real
    historia.append(Paragraph("<b>Tabla 4</b>", p_table_num))
    historia.append(Paragraph("<i>Resultados de Inferencia en Tiempo Real para Nuevas Piezas Artesanales</i>", p_table_title))
    
    tabla_4_datos = [
        [Paragraph("<b>Descripción del Encargo</b>", p_table_cell_bold), Paragraph("<b>Área (cm²)</b>", p_table_cell_bold), Paragraph("<b>Hilos</b>", p_table_cell_bold), Paragraph("<b>Prob. Alta</b>", p_table_cell_bold), Paragraph("<b>Clasificación</b>", p_table_cell_bold), Paragraph("<b>Horas Est.</b>", p_table_cell_bold), Paragraph("<b>Precio Sugerido</b>", p_table_cell_bold)],
        [Paragraph("Guayabera Gala (Calado)", p_table_cell), Paragraph("400.0", p_table_cell_center), Paragraph("5.0", p_table_cell_center), Paragraph("65.8%", p_table_cell_center), Paragraph("Alta Dedicación", p_table_cell), Paragraph("37.9 h", p_table_cell_center), Paragraph("$342,000 COP", p_table_cell_center)],
        [Paragraph("Pañuelo (Pata de Cabra)", p_table_cell), Paragraph("100.0", p_table_cell_center), Paragraph("1.0", p_table_cell_center), Paragraph("2.6%", p_table_cell_center), Paragraph("Estándar", p_table_cell), Paragraph("7.1 h", p_table_cell_center), Paragraph("$97,000 COP", p_table_cell_center)],
        [Paragraph("Mantel Imperial (Rococó)", p_table_cell), Paragraph("1050.0", p_table_cell_center), Paragraph("12.0", p_table_cell_center), Paragraph("100.0%", p_table_cell_center), Paragraph("Alta Dedicación", p_table_cell), Paragraph("93.7 h", p_table_cell_center), Paragraph("$785,000 COP", p_table_cell_center)],
    ]
    t4_elem = Table(tabla_4_datos, colWidths=[120, 50, 45, 50, 75, 55, 65])
    t4_elem.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1.0, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    historia.append(t4_elem)
    historia.append(Paragraph("<i>Nota.</i> El precio sugerido integra una remuneración base por hora de $7,500 COP, el costo de las madejas ($3,500 COP c/u) y la tela base. Elaboración propia a partir de usar_modelo.py.", p_note))

    # ==========================================================================
    # PÁGINAS 13-14: DISCUSIÓN (Sección 3.1)
    # ==========================================================================
    historia.append(Paragraph("<b>Discusión</b>", p_h1))
    historia.append(Spacer(1, 12))

    d1 = (
        "La convergencia concordante entre el perceptrón programado a mano en NumPy y el modelo regularizado de Ridge "
        "en Scikit-Learn demuestra que la dinámica de confección del bordado de Cartago obedece a leyes físicas y económicas "
        "altamente consistentes. En términos de dominio artesanal, el insumo de hilo y la superficie bordada actúan como "
        "indicadores objetivos de la cantidad de puntadas requeridas. La técnica de Calado Fino, al implicar el deshilado "
        "estructural de la tela seguido de un re-bordado milimétrico, impone un ritmo de avance notablemente menor (promedio de "
        "9.38 cm²/hora) frente a técnicas como Pata de Cabra (promedio de 17.5 cm²/hora). El modelo Ridge capturó esta "
        "variabilidad asignando ponderaciones adecuadas sin incurrir en coeficientes inestables."
    )
    historia.append(Paragraph(d1, p_body))

    d2 = (
        "En cuanto a las limitaciones del proyecto, debe señalarse en primer lugar el tamaño de la muestra disponible (N = 20). "
        "Aunque este número resultó suficiente para entrenar modelos lineales y regularizados con excelente bondad de ajuste (R² = 0.928) "
        "gracias a la baja dimensionalidad de las entradas, introduce restricciones para entrenar arquitecturas profundas o árboles "
        "no acotados, los cuales memorizarían rápidamente el ruido muestral. En segundo lugar, existe un componente de variabilidad "
        "humana intrínseca: la destreza motriz, el cansancio visual y la antigüedad de la artesana pueden introducir fluctuaciones "
        "de entre 2 y 5 horas para un mismo patrón geométrico, lo cual coincide con el residuo irreductible del MAE observado."
    )
    historia.append(Paragraph(d2, p_body))

    d3 = (
        "Desde la perspectiva ética y social, es imperativo enfatizar que este sistema de inteligencia artificial no ha sido "
        "concebido como un mecanismo de fiscalización o imposición de metas de rendimiento tayloristas sobre las artesanas. "
        "Por el contrario, su propósito esencial es fungir como una herramienta de empoderamiento comunitario que blinde a las "
        "bordadoras frente a intermediarios comerciales que habitualmente regatean las tarifas. Al contar con un estimador "
        "matemático que demuestra que un mantel complejo requiere más de 90 horas de dedicación exclusiva, la artesana adquiere "
        "un argumento técnico irrefutable para defender un precio justo y una retribución salarial digna para su hogar."
    )
    historia.append(Paragraph(d3, p_body))

    # ==========================================================================
    # PÁGINA 14-15: CONCLUSIONES Y TRABAJO FUTURO (Sección 3.1)
    # ==========================================================================
    historia.append(Paragraph("<b>Conclusiones y Trabajo Futuro</b>", p_h1))
    historia.append(Spacer(1, 12))

    c1 = (
        "El desarrollo del presente proyecto permitió validar con éxito el ciclo completo de la inteligencia artificial aplicada "
        "a una problemática real del municipio de Cartago, alcanzando los siguientes hallazgos concluyentes:"
    )
    historia.append(Paragraph(c1, p_body))

    c_items = [
        "1. Se demostró la viabilidad técnica de predecir cuantitativamente el tiempo de confección manual de bordados tradicionales, logrando mediante el algoritmo de regresión Ridge un coeficiente de determinación R² de 0.928 y un MAE de 3.58 horas, lo cual valida la hipótesis de que las dimensiones geométricas y el consumo de hilo son determinantes causales del esfuerzo productivo.",
        "2. El perceptrón construido desde cero con NumPy demostró que una sola neurona artificial con activación sigmoide es plenamente capaz de aprender una frontera lineal que separa piezas estándar de piezas de alta dedicación horaria (con exactitud del 100.0% respecto al umbral de la mediana de 29.0 horas), evidenciando la solidez matemática del descenso del gradiente.",
        "3. La adopción de Pipelines en Scikit-Learn garantizó una metodología experimental rigurosa libre de fuga de datos (data leakage), permitiendo comparar de forma justa algoritmos de clasificación y regresión, donde la regularización L2 demostró superioridad frente a modelos no paramétricos como árboles de decisión no acotados.",
        "4. La serialización de los modelos mediante Joblib y su despliegue en un contenedor Docker modular viabilizan la transferencia tecnológica hacia talleres artesanales, facilitando una cotización en tiempo real en menos de 100 milisegundos."
    ]
    for ci in c_items:
        historia.append(Paragraph(ci, p_body))

    historia.append(Paragraph("<b>Trabajo Futuro</b>", p_h2))
    tf = (
        "Como líneas prioritarias de trabajo futuro se proyecta: (a) ampliar el banco de datos hasta alcanzar un mínimo de 100 "
        "pedidos representativos incorporando talleres de los municipios aledaños de Ansermanuevo y Obando; (b) integrar módulos "
        "de Visión por Computador (Computer Vision) mediante redes neuronales convolucionales (CNN) que analicen directamente una "
        "fotografía del trazo del diseño para estimar automáticamente el área y la densidad de puntadas; y (c) desarrollar una "
        "aplicación móvil accesible o un bot de mensajería instantánea que acerque la herramienta a artesanas no digitalizadas."
    )
    historia.append(Paragraph(tf, p_body))

    # ==========================================================================
    # PÁGINAS 15-16: REFERENCIAS (APA 7 - Mínimo 6 referencias, sangría francesa)
    # ==========================================================================
    historia.append(PageBreak())
    historia.append(Paragraph("<b>Referencias</b>", p_h1))
    historia.append(Spacer(1, 12))

    referencias_lista = [
        "Géron, A. (2022). <i>Hands-on machine learning with Scikit-Learn, Keras, and TensorFlow</i> (3.ª ed.). O'Reilly Media.",
        "Goodfellow, I., Bengio, Y., & Courville, A. (2016). <i>Deep learning</i>. MIT Press.",
        "Minsky, M., & Papert, S. (1969). <i>Perceptrons: An introduction to computational geometry</i>. MIT Press.",
        "Müller, A. C., & Guido, S. (2016). <i>Introduction to machine learning with Python: A guide for data scientists</i>. O'Reilly Media.",
        "OpenAI. (2026). <i>ChatGPT (versión del 22 de noviembre)</i> [Modelo de lenguaje de gran tamaño]. https://chat.openai.com",
        "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. <i>Journal of Machine Learning Research</i>, 12, 2825–2830.",
        "Python Software Foundation. (2024). <i>Python (Versión 3.12)</i> [Software]. https://www.python.org",
        "Rosenblatt, F. (1958). The perceptron: A probabilistic model for information storage and organization in the brain. <i>Psychological Review</i>, 65(6), 386–408. https://doi.org/10.1037/h0042519",
        "Russell, S., & Norvig, P. (2020). <i>Artificial intelligence: A modern approach</i> (4.ª ed.). Pearson."
    ]

    for ref in referencias_lista:
        historia.append(Paragraph(ref, p_ref))
        historia.append(Spacer(1, 12))

    # ==========================================================================
    # PÁGINA 16-17: APÉNDICES (Sección 3.1 y 3.5)
    # ==========================================================================
    historia.append(PageBreak())
    historia.append(Paragraph("<b>Apéndice A</b>", p_h1))
    historia.append(Paragraph("<i>Enlace al Repositorio de GitHub y Estructura del Código Fuente</i>", p_table_title))
    historia.append(Spacer(1, 12))

    ap_a = (
        "El código fuente íntegro, datasets, scripts de entrenamiento, modelos serializados (.joblib) e imágenes de soporte "
        "se encuentran alojados de forma pública y reproducible en el siguiente repositorio de GitHub:<br/>"
        "<b>Enlace Oficial:</b> https://github.com/Cruz1905/curso-inteligencia-artificial<br/><br/>"
        "<b>Estructura de Carpetas del Proyecto:</b><br/>"
        "• proyecto/data/: Contiene los datasets pedidos_bordados.csv, pedidos_bordados_limpio.csv y pedidos_bordados_preparados_ml.csv.<br/>"
        "• proyecto/src/eda_proyecto.py: Script para análisis exploratorio de datos mediante NumPy puro.<br/>"
        "• proyecto/src/preparacion_datos_proyecto.py: Script para limpieza, ingeniería de variables y One-Hot Encoding con Pandas.<br/>"
        "• proyecto/src/perceptron_proyecto.py: Implementación de la neurona artificial monocapa con descenso del gradiente (Avance 2).<br/>"
        "• proyecto/src/modelo_proyecto.py: Implementación con Scikit-Learn de Pipelines, clasificación y regresión Ridge.<br/>"
        "• proyecto/src/usar_modelo.py: Script de inferencia en tiempo real para cotizaciones instantáneas.<br/>"
        "• Dockerfile y docker-compose.yml: Configuración de contenedorización con Python 3.12-slim."
    )
    historia.append(Paragraph(ap_a, p_body_no_indent))

    historia.append(Spacer(1, 24))
    historia.append(Paragraph("<b>Apéndice B</b>", p_h1))
    historia.append(Paragraph("<i>Declaración Formal de Uso de Inteligencia Artificial (Sección 3.5)</i>", p_table_title))
    historia.append(Spacer(1, 12))

    ap_b = (
        "En estricto cumplimiento de la Sección 3.5 de los lineamientos oficiales del curso de Inteligencia Artificial "
        "(COTECNOVA 2026-02), los integrantes del Grupo 02 declaran el uso responsable y ético de herramientas de "
        "inteligencia artificial generativa como soporte técnico durante la elaboración de este proyecto:<br/><br/>"
        "1. <b>Herramienta utilizada:</b> Antigravity AI Assistant / ChatGPT (OpenAI, 2026).<br/>"
        "2. <b>Tareas en las que se empleó la herramienta:</b><br/>"
        "   a) Asistencia en la depuración sintáctica y vectorización de código en Python con NumPy y Scikit-Learn.<br/>"
        "   b) Optimización de estilos visuales en gráficos estadísticos con Matplotlib y Seaborn.<br/>"
        "   c) Revisión ortotipográfica y verificación de la estructura editorial bajo directrices de Normas APA 7.ª edición.<br/>"
        "3. <b>Mecanismo de verificación y validación:</b> Todo el código fuente generado fue ejecutado, testeado y verificado "
        "línea por línea por los estudiantes dentro del contenedor Docker local. Las métricas numéricas, coeficientes y "
        "conclusiones teóricas fueron confrontadas directamente con las salidas de consola y el marco analítico del docente. "
        "El equipo asume la total autoría y responsabilidad sobre la veracidad de los datos, código y conclusiones expuestas."
    )
    historia.append(Paragraph(ap_b, p_body_no_indent))

    # Construir PDF
    doc.build(historia, canvasmaker=APANumberedCanvas)
    
    # Copiar también a la ruta de docs/ y Documents/
    import shutil
    shutil.copy(ruta_salida, ruta_docs)
    
    ruta_ia = r"C:\Users\davis\OneDrive\Documentos\Davison\IA\Informe_Final_Grupo02_BordadosCartago.pdf"
    shutil.copy(ruta_salida, ruta_ia)

    print(f"Informe APA 7 generado exitosamente en: {ruta_salida}")
    print(f"Copia guardada en: {ruta_docs}")
    print(f"Copia guardada en: {ruta_ia}")

if __name__ == "__main__":
    construir_informe_apa()
