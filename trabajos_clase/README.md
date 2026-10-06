# Trabajos y Talleres en Clase 📚

Repositorio organizado para las actividades prácticas, talleres y laboratorios del curso de Inteligencia Artificial (COTECNOVA).

---

## 📑 Índice de Clases

### 🔹 [Clase 01 - Introducción y Fundamentos](./clase_01/)
- **Archivo:** `analisis_datos.py`
- **Temas:** Variables, tipos de datos y condicionales `if-else` en Python aplicados al contexto de Cartago.

### 🔹 [Clase 03 - Manejo de Archivos y Estructuras de Datos](./clase_03/)
- **Archivos:**
  - `cultivos.csv`: Dataset con información de producción y hectáreas.
  - `analizar_cultivos.py`: Script con `csv.DictReader` y funciones para calcular estadísticas.
  - `informe_cultivos.md`: Informe autogenerado en formato Markdown con los resultados del análisis.
- **Temas:** Lectura/escritura de archivos CSV, listas de diccionarios y generación automatizada de informes.

### 🔹 [Clase 04 - Introducción a NumPy y EDA Básico](./clase_04/)
- **Archivos:**
  - `cultivos_detalle.csv`: Dataset extendido con región y tipo de suelo.
  - `eda_cultivos.py`: Script con NumPy y Matplotlib para Análisis Exploratorio de Datos (EDA).
  - `estadisticas.txt`: Exportación de métricas descriptivas en JSON/texto plano.
  - `hectareas_por_cultivo.png`: Gráfico de barras.
  - `hectareas_vs_produccion.png`: Gráfico de dispersión.
  - `distribucion_produccion.png`: Histograma de frecuencias de producción.
- **Temas:** Arrays de NumPy, operaciones vectorizadas, estadísticas descriptivas (media, mediana, desviación estándar, min/max) y visualizaciones con Matplotlib.

### 🔹 [Clase 07 - Pandas, Seaborn y Preparación de Datos para ML](./clase_07/)
- **Archivos:**
  - `ventas_tienda.csv`: Dataset de ventas con valores nulos intencionales.
  - `preparacion_datos.py`: Script con Pandas (imputación de nulos con mediana, columna derivada `total_venta`), Seaborn (gráficos estadísticos) y One-Hot Encoding con `pd.get_dummies()`.
  - `ventas_preparadas_ml.csv`: Dataset limpio y codificado listo para Machine Learning.
  - `distribucion_ventas.png`: Histograma con estimación de densidad KDE.
  - `ventas_por_categoria.png`: Gráfico de barras con acumulado de ventas.
  - `edad_vs_venta.png`: Gráfico de dispersión multivariable (edad vs venta con categoría y método de pago).
  - `interpretacion_resultados.md`: Respuestas detalladas a las preguntas de análisis del profesor.
- **Temas:** Manipulación de DataFrames y Series, imputación de datos faltantes, visualización estadística avanzada con Seaborn y preparación de matrices para modelos de ML.

### 🔹 [Clase 08 - ¿Cómo Aprende una IA? Pesos, Neuronas y Error](./clase_08/)
- **Archivos:**
  - `neurona_and.py`: Implementación desde cero en Python puro de un Perceptrón simple para aprender la compuerta AND, con registro del error por época y gráfica.
  - `evolucion_error_and.png`: Curva de descenso del error total a lo largo de las épocas de entrenamiento para la compuerta AND.
  - `neuronas_logicas.py`: Implementación del perceptrón para compuertas OR y NOT (1 entrada) con convergencia y visualización.
  - `evolucion_error_or_not.png`: Gráficas comparativas de evolución del error para OR y NOT.
  - `reflexion_aprendizaje_ia.md`: Análisis teórico riguroso sobre tasa de aprendizaje, necesidad del bias y demostración matemática/geométrica de la no separabilidad lineal de la compuerta XOR (Minsky & Papert, 1969).
- **Temas:** Fundamentos de redes neuronales, suma ponderada, función de activación escalón, regla de aprendizaje de Rosenblatt, épocas, ajuste de pesos y bias, y separabilidad lineal.
