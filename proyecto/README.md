# Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago 🧵🤖

**Asignatura:** Inteligencia Artificial – COTECNOVA 2026-02  
**Docente:** Jhon James Cano Sánchez  
**Integrantes:** Davison Cruz & Juan Diego Zapata  
**Fecha de Avance (Corte 1):** 21 de septiembre de 2026  
**Fecha de Avance (Corte 2):** 25 de octubre de 2026  
**Fecha de Entrega Técnica (Clase 12 / Corte 3):** 22 de noviembre de 2026  

---

## 1. Definición del Proyecto

### 📌 Problemática
En el municipio de Cartago, Valle del Cauca (*Capital Mundial del Bordado*), los talleres artesanales y modistas tradicionales calculan el costo y tiempo de entrega de sus pedidos de forma meramente empírica ("al ojo"). Al no contar con herramientas estandarizadas para tasar piezas complejas (con técnicas como *calado*, *punto de sombra* o *rococó*), las artesanas suelen subvalorar sus horas de trabajo manual, sufriendo pérdidas económicas continuas o retrasos imprevistos en las entregas.

### 🎯 Objetivo
Desarrollar un sistema basado en Inteligencia Artificial (Machine Learning) capaz de estimar con precisión matemática:
1. Las **horas de trabajo manual requeridas** para la confección artesanal mediante **Regresión**.
2. La **clasificación de complejidad y dedicación** (Estándar vs Alta Dedicación) para planificación de talleres.
3. El **precio justo sugerido de venta al público (COP)**, asegurando una retribución digna y competitiva.

### 📊 Datos y Fuente
Se construyó y estructuró el dataset `pedidos_bordados.csv` a partir del muestreo de piezas representativas de talleres locales de Cartago, considerando 20 registros con 9 atributos técnicos:
- `id_pedido`: Identificador del encargo.
- `prenda`: Tipo de artículo (Guayabera, Blusa, Mantel, Vestido, etc.).
- `tecnica`: Técnica artesanal principal (Calado Fino, Punto de Sombra, Rococó, Punto de Cruz, Pata de Cabra).
- `tela`: Tipo de textil base (Lino, Algodón, Seda).
- `area_cm2`: Superficie neta del bordado en centímetros cuadrados.
- `complejidad`: Nivel de detalle (Baja, Media, Alta, Muy Alta).
- `madejas_hilo`: Cantidad de madejas consumidas.
- `horas_trabajo`: Tiempo invertido de confección manual.
- `precio_cop`: Valor final de venta cobrado.

---

## 2. Preparación de Datos con Pandas y Seaborn (Clases 7 y 8)

En cumplimiento de los requisitos de preparación y visualización:
- **Exploración con Pandas:** Carga del dataset mediante `pd.read_csv()`, verificación de tipos con `df.info()`, estadísticas descriptivas y comprobación de nulos con `df.isnull().sum()` (0 valores nulos, 0 duplicados, rangos lógicos coherentes).
- **Columnas Derivadas Creadas:**
  - `costo_por_cm2 = precio_cop / area_cm2`: Mide el valor en pesos por centímetro cuadrado bordado.
  - `productividad_cm2_hora = area_cm2 / horas_trabajo`: Cuantifica el avance de la artesana por hora según la técnica.
- **Tabla "Antes / Después" de la Limpieza:**

| Métrica | Antes (Crudo) | Después (Limpio) | Para ML (One-Hot) |
| :--- | :---: | :---: | :---: |
| **Número de Filas** | 20 | 20 | 20 |
| **Número de Columnas** | 9 | 11 | 18 |
| **Valores Nulos Totales** | 0 | 0 | 0 |
| **Filas Duplicadas** | 0 | 0 | 0 |
| **Variables Categóricas** | 3 (texto) | 3 (texto) | 0 (codificadas 1/0) |

- **Visualizaciones con Seaborn:**
  1. `densidad_precios_seaborn.png`: Histograma con curva KDE que muestra la distribución bimodal de precios según si son prendas personales o manteles de gran formato.
  2. `boxplot_horas_por_tecnica.png`: Diagrama de caja y bigotes que evidencia la alta dispersión y exigencia temporal del *Calado Fino* respecto a las demás técnicas.
  3. `regresion_area_vs_horas.png`: Gráfico de dispersión con ajuste de regresión lineal directa que confirma la correlación positiva entre superficie y horas de labor.
- **Codificación para Machine Learning:** Aplicación de **One-Hot Encoding** (`pd.get_dummies()`) sobre las variables `tecnica`, `tela` y `complejidad`, exportando el dataset final listo para modelado en `data/pedidos_bordados_preparados_ml.csv` (20 filas x 18 columnas numéricas).

---

## 3. Análisis Exploratorio de Datos (EDA) con NumPy

Mediante funciones vectorizadas de NumPy (`np.mean`, `np.median`, `np.std`, `np.min`, `np.max`), se obtuvieron las siguientes métricas descriptivas:

| Variable Analizada | Promedio (Media) | Mediana | Desv. Estándar | Mínimo | Máximo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Horas de Trabajo (h)** | 37.30 h | 29.00 h | 24.43 h | 9.50 h | 115.00 h |
| **Precio Sugerido (COP)** | $287,500 COP | $230,000 COP | $181,490 COP | $85,000 COP | $850,000 COP |

---

## 4. Avance 2: Perceptrón con Sigmoide desde Cero (Clases 8 y 9)

Como hito fundamental del Segundo Corte, se implementó en `src/perceptron_proyecto.py` una neurona artificial simple unicapa entrenada mediante **descenso del gradiente en lote** sin librerías de alto nivel (utilizando exclusivamente **NumPy puro**).

* **Pérdida inicial:** $0.6931$ $\rightarrow$ **Pérdida final:** $0.1361$.
* **Exactitud de entrenamiento:** $100.0\%$ ($20/20$ aciertos).
* **Pesos finales aprendidos:** $w_1 (\text{Área}) = +3.5566$, $w_2 (\text{Madejas}) = +3.4419$, $b = +1.7104$.
* **Limitación identificada en Avance 2:** Se evaluó con los mismos datos de entrenamiento (riesgo de memorización) y solo resolvía una clasificación binaria (0/1), sin predecir el número exacto continuo de horas ni el precio final en COP.

---

## 5. Clase 12: Modelos Finales con Scikit-Learn, Pipelines y Persistencia (.joblib)

Siguiendo la metodología de la **Clase 12**, se implementó el pipeline industrial completo de Machine Learning en [`src/modelo_proyecto.py`](./src/modelo_proyecto.py) y el módulo de inferencia en tiempo real en [`src/usar_modelo.py`](./src/usar_modelo.py).

### 5.1. División Rigurosa Entrenamiento / Prueba y Pipelines
* Se separó el conjunto de datos en **80% Entrenamiento ($N=16$)** y **20% Prueba ($N=4$)** con `stratify=y` en clasificación y `random_state=42`.
* Cada modelo se encapsuló dentro de un `Pipeline([('escalado', StandardScaler()), ('modelo', ...)])` para evitar fuga de información (*data leakage*).

### 5.2. Comparación de Modelos de Clasificación (Alta Dedicación: Horas $\ge 29$)

| Modelo | Exactitud | Precisión | Recall | F1-Score | Val. Cruzada ($k=5$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Regresión Logística** | **1.000** | **1.000** | **1.000** | **1.000** | **0.900** |
| **KNN (3 vecinos)** | 1.000 | 1.000 | 1.000 | 1.000 | 0.950 |
| **Árbol de Decisión ($d=3$)** | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| **Red Neuronal (MLP)** | 1.000 | 1.000 | 1.000 | 1.000 | 0.900 |

* **Matriz de Confusión en Prueba:**
  $$\begin{pmatrix} 2 & 0 \\ 0 & 2 \end{pmatrix}$$
  * Aciertos clase Estándar (0): 2
  * Aciertos clase Alta Dedicación (1): 2
  * Falsos positivos: 0 \| Falsos negativos: 0
* **Gráfico generado:** [`matriz_confusion_proyecto.png`](matriz_confusion_proyecto.png).
* **Modelo guardado:** [`src/modelo_clasificacion_bordados.joblib`](src/modelo_clasificacion_bordados.joblib).

### 5.3. Comparación de Modelos de Regresión (Estimación Continua de Horas de Trabajo)

| Modelo | MAE (horas) | RMSE (horas) | $R^2$ Score |
| :--- | :---: | :---: | :---: |
| **Regresión Lineal** | 4.386 h | 5.370 h | 0.914 |
| **Ridge Regression ($\alpha=1.0$)** | **3.584 h** | **4.919 h** | **0.928** |
| **KNN Regressor ($k=3$)** | 5.667 h | 7.528 h | 0.831 |
| **Árbol de Regresión ($d=3$)** | 7.500 h | 8.712 h | 0.773 |

* **Mejor Modelo de Regresión:** **Ridge Regression** con $R^2 = 0.928$ (explica el $92.8\%$ de la variabilidad real de las horas de confección) y un error absoluto medio de solo $3.58$ horas.
* **Gráfico generado:** [`real_vs_predicho_proyecto.png`](real_vs_predicho_proyecto.png).
* **Modelo guardado:** [`src/modelo_regresion_bordados.joblib`](src/modelo_regresion_bordados.joblib).

### 5.4. Demostración en Tiempo Real para la Sustentación (`src/usar_modelo.py`)
El script carga los modelos serializados sin volver a entrenar y realiza predicciones instantáneas sobre piezas nuevas:

```text
--- RESULTADOS DE INFERENCIA EN TIEMPO REAL ---
                               descripcion  area_cm2  madejas_hilo  Prob_Alta_%   Clasificacion  Horas_Estimadas Precio_Sugerido_COP
    Guayabera de Gala (Lino + Calado Fino)     400.0           5.0         65.8 Alta Dedicación             37.9            $342,000
Pañuelo Delicado (Algodón + Pata de Cabra)     100.0           1.0          2.6        Estándar              7.1             $97,000
  Mantel Imperial (Lino + Rococó Complejo)    1050.0          12.0        100.0 Alta Dedicación             93.7            $785,000
```

### 5.5. Comparación Crítica: Avance 2 (Perceptrón a Mano) vs Clase 12 (Scikit-Learn)
1. **Confiabilidad de Métricas:** En el Avance 2 la exactitud se medía sobre los mismos 20 datos de aprendizaje (posible memorización). En la Clase 12 se garantiza evaluación con datos de prueba no vistos y validación cruzada.
2. **Capacidad del Modelo:** El perceptrón a mano solo resolvía si una prenda era o no de alta dedicación ($0/1$). El pipeline de Scikit-Learn predice la probabilidad exacta, clasifica la prenda, y mediante **Ridge Regression** estima las horas exactas continuas y el precio sugerido en COP.
3. **Persistencia y Demostración:** El modelo se encuentra serializado con `joblib`, permitiendo que en la sustentación presencial se cargue en milisegundos y cotice cualquier pedido en vivo.

---

## 6. Instrucciones de Ejecución 🐳

### Opción A: Ejecución Directa en Python
```bash
# 1. Ejecutar el entrenamiento y guardado de los modelos:
python proyecto/src/modelo_proyecto.py

# 2. Ejecutar la demostración de inferencia con casos nuevos:
python proyecto/src/usar_modelo.py
```

### Opción B: Ejecución en Contenedor Docker
```bash
docker compose up -d
docker exec -it ia_python bash
cd /app/proyecto/src
python modelo_proyecto.py
python usar_modelo.py
exit
```

---

## 7. Entregables Finales y Documentación Oficial (Tercer Corte) 📄🎓

En estricto cumplimiento de los lineamientos del Proyecto Final de la asignatura:

1. **Informe Final en Normas APA 7ma Edición (PDF):**
   - [`Informe_Final_Grupo02_BordadosCartago.pdf`](Informe_Final_Grupo02_BordadosCartago.pdf) (y copia en [`docs/Informe_Final_Grupo02_BordadosCartago.pdf`](docs/Informe_Final_Grupo02_BordadosCartago.pdf)).
   - **Formato:** Times New Roman 12 pt, interlineado doble (2.0), márgenes de 2.54 cm, sangría de 1.27 cm, numeración superior derecha, tablas y figuras bajo normativa APA 7, 8 referencias académicas rigurosas y Apéndice de declaración de uso de IA generativa (Sección 3.5).
   - **Extensión:** 22 páginas en total (17 páginas de contenido neto de investigación, entre el rango exigido de 12 a 20 páginas).

2. **Presentación para Sustentación Presencial (PPTX y PDF):**
   - [`Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pdf`](Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pdf)
   - [`Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pptx`](Presentacion_Proyecto_Final_Grupo02_BordadosCartago.pptx)
   - **Estructura cronometrada (6 minutos de exposición + 2 minutos de preguntas):**
     - Diapositiva 1: Portada institucional COTECNOVA e integrantes del Grupo 02.
     - Diapositiva 2: Momento 1 · Planteamiento del problema en Cartago, beneficiarios y objetivo (1 min).
     - Diapositiva 3: Momento 2 · Ingeniería de datos, calidad, imputación y división anti-fuga (1 min).
     - Diapositiva 4: Momento 3 · Modelo por dentro: Perceptrón desde cero en NumPy y frontera de decisión (1.5 min).
     - Diapositiva 5: Momento 4 · Modelos Scikit-Learn (Random Forest, Ridge Regression) y métricas F1/MAE (1 min).
     - Diapositiva 6: Momento 5 · Demostración en vivo (`usar_modelo.py`) y **Plan B obligatorio** con captura de terminal integrada (1 min).
     - Diapositiva 7: Momento 6 · Cierre, limitaciones del alcance y trabajo futuro (0.5 min).
     - Diapositiva 8: Ronda de preguntas y enlace al repositorio de GitHub.

3. **Demostración y Plan B:**
   - Evidencia gráfica de respaldo: [`captura_plan_b_terminal.png`](captura_plan_b_terminal.png).
   - Inferencia en milisegundos con modelos serializados (`.joblib`) listos para ejecutarse en vivo desde el contenedor Docker.
