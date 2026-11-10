# Clase 12: Scikit-Learn – Entrenar, Evaluar y Guardar Modelos
## Inteligencia Artificial · Facultad de Ingeniería de Sistemas · COTECNOVA 2026-02
* **Docente:** Jhon James Cano Sánchez  
* **Estudiante:** Davison Cruz López (Grupo 02 - Proyecto Bordados de Cartago)  

---

## 1. Visión General de la Clase

En las clases anteriores se construyó un perceptrón desde cero utilizando únicamente NumPy para comprender el funcionamiento interno del aprendizaje automático (suma ponderada $X \cdot \mathbf{w} + b$, función sigmoide, cálculo de la función de pérdida y optimización mediante descenso del gradiente).

En esta clase se hace la transición a **Scikit-Learn**, la librería estándar de la industria en Python para Machine Learning. Los objetivos cumplidos son:
1. Usar el flujo canónico de Scikit-Learn: **instanciar modelo $\rightarrow$ entrenar (`fit`) $\rightarrow$ predecir (`predict` / `predict_proba`)**.
2. Dividir rigurosamente el conjunto de datos en **entrenamiento (80%)** y **prueba (20%)** usando `train_test_split` con estratificación (`stratify=y`).
3. Encapsular el preprocesamiento y el estimador en un `Pipeline` con `StandardScaler` para prevenir fuga de datos (*data leakage*).
4. Entrenar y comparar múltiples clasificadores (**Regresión Logística**, **K-Nearest Neighbors (KNN)** y **Árbol de Decisión**) mediante métricas integrales: Exactitud, Precisión, Recall, F1-Score y Validación Cruzada con 5 pliegues ($k=5$).
5. Implementar un modelo de **Regresión Lineal** para predecir una variable cuantitativa continua (rendimiento agrícola en kg/ha), evaluando con **MAE**, **RMSE** y **$R^2$**.
6. Demostrar la superación de la limitación del perceptrón monocapa en problemas no linealmente separables (**Compuerta XOR**) empleando un perceptrón multicapa (**`MLPClassifier`**).
7. Identificar experimentalmente el fenómeno de **sobreajuste (*overfitting*)** al variar la profundidad de un árbol de decisión (`max_depth` de 1 a 12).
8. Persistir y serializar el modelo entrenado en disco (`joblib.dump`) para su posterior consumo en inferencia (`joblib.load`) sin necesidad de reentrenamiento.

---

## 2. Estructura de la Carpeta `clase12/`

```text
clase12/
├── Dockerfile                  # Entorno Docker basado en Python 3.12-slim
├── docker-compose.yml          # Orquestación con container_name: ia_python
├── requirements.txt            # Dependencias: scikit-learn, joblib, pandas, seaborn, etc.
├── README.md                   # Documentación técnica completa y preguntas de reflexión
├── notebooks/                  # Directorio para experimentación interactiva
├── data/
│   ├── cultivos_cartago.csv    # Dataset de clasificación (120 lotes: precipitación, temperatura, éxito)
│   └── rendimiento_cartago.csv # Dataset de regresión simulado (150 lotes: insumos y rendimiento en kg/ha)
└── src/
    ├── clasificar_cultivos.py  # Paso 1: Comparación de modelos, métricas y guardado de modelo
    ├── usar_modelo.py          # Paso 2: Carga del modelo serializado y predicción sobre lotes nuevos
    ├── regresion_rendimiento.py# Paso 3: Regresión lineal múltiple para rendimiento agrícola
    ├── red_xor.py              # Paso 4: Solución de la compuerta XOR mediante MLPClassifier
    ├── profundidad_arbol.py    # Paso 5: Demostración empírica de sobreajuste
    ├── modelo_cultivos.joblib  # Modelo final exportado con Pipeline y escalador
    ├── matriz_confusion.png    # Heatmap de la matriz de confusión del mejor clasificador
    ├── real_vs_predicho.png    # Gráfico de dispersión real vs predicho en regresión lineal
    └── sobreajuste_arbol.png   # Gráfica de curvas de exactitud en entrenamiento vs prueba
```

---

## 3. Desarrollo de los Pasos Prácticos

### Paso 1: Comparación de Modelos de Clasificación (`clasificar_cultivos.py`)
Se evaluaron tres arquitecturas sobre los 24 lotes de prueba no vistos:

| Modelo | Exactitud | Precisión | Recall | F1-Score | Val. Cruzada ($k=5$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Regresión Logística** | **1.000** | **1.000** | **1.000** | **1.000** | **0.967** |
| **KNN (5 vecinos)** | 0.958 | 1.000 | 0.923 | 0.960 | 0.967 |
| **Árbol de Decisión ($d=3$)** | 0.958 | 1.000 | 0.923 | 0.960 | 0.908 |

* **Mejor modelo seleccionado:** **Regresión Logística** (mayor F1 y consistencia en validación cruzada).
* **Pesos aprendidos:** $w_1 = 2.80$ (precipitación), $w_2 = -2.27$ (temperatura), $b = 0.18$.
  * Coincide exactamente con el análisis del perceptrón: **la precipitación favorece la cosecha ($w_1 > 0$) y la temperatura excesiva la perjudica ($w_2 < 0$)**.
* **Matriz de Confusión:**
  $$\begin{pmatrix} 11 & 0 \\ 0 & 13 \end{pmatrix}$$
  * Aciertos clase 0 (verdaderos negativos): 11
  * Aciertos clase 1 (verdaderos positivos): 13
  * Falsos positivos: 0
  * Falsos negativos: 0

---

### Paso 2: Uso del Modelo Guardado (`usar_modelo.py`)
Sin reentrenar el modelo, se cargó el archivo `modelo_cultivos.joblib` (el cual incluye internamente el transformador `StandardScaler` y el clasificador `LogisticRegression`):

```text
Predicciones con el modelo guardado:
 precipitacion_mm  temperatura_c  probabilidad_exito_%  resultado
            220.0           23.5                  99.8    Exitosa
             60.0           30.0                   0.1 No exitosa
            150.0           26.0                  63.6    Exitosa
```
* **Lote 1 (Alta precipitación y clima fresco):** 99.8% de probabilidad de éxito $\rightarrow$ **Exitosa**.
* **Lote 2 (Baja precipitación y calor intenso):** 0.1% de probabilidad de éxito $\rightarrow$ **No exitosa**.
* **Lote 3 (Condiciones intermedias cercanas a la frontera):** 63.6% de probabilidad $\rightarrow$ **Exitosa** (con menor certeza).

---

### Paso 3: Predicción Cuantitativa - Regresión Lineal (`regresion_rendimiento.py`)
Para estimar el rendimiento de los cultivos en kg/ha a partir de tres variables explicativas:

* **Métricas en datos de prueba:**
  * **$\text{MAE} = 122.3\text{ kg/ha}$**: En promedio, la predicción se desvía en apenas $122.3\text{ kg/ha}$ frente a un rendimiento medio de $3405\text{ kg/ha}$ (un error relativo de solo $3.6\%$).
  * **$\text{RMSE} = 157.2\text{ kg/ha}$**: Penaliza desviaciones grandes y confirma la estabilidad del estimador.
  * **$R^2 = 0.901$**: El modelo lineal explica más del **$90\%$ de la varianza total** del rendimiento agrícola.
* **Efecto de cada variable (por desviación estándar):**
  * `precipitacion_mm`: $+389.2\text{ kg/ha}$ (es el factor más determinante y positivo).
  * `fertilizante_kg_ha`: $+200.5\text{ kg/ha}$ (segundo aporte positivo relevante).
  * `temperatura_c`: $-250.0\text{ kg/ha}$ (impacto negativo sobre el rendimiento).

---

### Paso 4: Solución de la Compuerta XOR (`red_xor.py`)
Se confrontó una sola neurona lineal frente a una red neuronal multicapa (`MLPClassifier` con 4 neuronas ocultas y activación `tanh`):

```text
 x1  x2  Esperado  Una neurona  Red neuronal
  0   0         0            0             0
  0   1         1            0             1
  1   0         1            0             1
  1   1         0            0             0

Exactitud de una neurona: 50%
Exactitud de la red neuronal: 100%
```
* **Conclusión teórica:** Una sola neurona solo puede generar un hiperplano lineal, fallando en el XOR. La capa oculta del MLP introduce transformaciones no lineales que curvan el espacio de decisión, logrando una clasificación perfecta del 100%.

---

### Paso 5: Análisis Experimental de Sobreajuste (`profundidad_arbol.py`)
Se entrenaron árboles de decisión variando la profundidad máxima (`max_depth`) entre 1 y 12:

* A profundidad baja ($d = 1, 2$), el modelo subajusta ligeramente.
* A profundidad media ($d = 3$), el modelo equilibra entrenamiento ($95.8\%$) y prueba ($95.8\%$).
* A profundidades altas ($d \ge 5$), el árbol alcanza **$100\%$ de exactitud en entrenamiento**, memorizando ruido muestral sin aportar mejoras en el conjunto de prueba. Esto justifica la restricción de hiperparámetros como `max_depth` en árboles de producción.

---

## 4. Respuestas a las Preguntas de Reflexión (Guía Docente)

### 1. ¿Por qué la validación cruzada (0.883 / 0.967) es más confiable que la exactitud con solo 24 lotes de prueba (0.958 / 1.000)?
**Respuesta:**  
Porque al evaluar sobre un conjunto de prueba pequeño (como $N=24$), cada muestra individual tiene un peso porcentual desproporcionado ($\approx 4.17\%$). Si por azar de la partición el subconjunto de prueba contiene observaciones sencillas, la exactitud resultará optimista; si contiene un caso atípico, la métrica caerá drásticamente.  
La **validación cruzada en 5 pliegues ($k=5$)** divide la totalidad de los datos en 5 bloques disyuntos y evalúa 5 veces, rotando el bloque de prueba. Al promediar los 5 resultados, se reduce sustancialmente la varianza debida a la partición aleatoria, ofreciendo una estimación del rendimiento generalizable mucho más robusta y estadísticamente representativa.

### 2. En su proyecto, ¿qué error es más grave: una falsa alarma (falso positivo) o un caso que se escapa (falso negativo)? ¿Qué métrica conviene usar?
**Respuesta (Contexto del Proyecto de Bordados de Cartago):**  
En el proyecto de estimación para los talleres de bordados de Cartago, el objetivo de clasificación es detectar **pedidos de Alta Dedicación / Complejidad Crítica ($y=1$)**:
* Un **Falso Positivo** significa etiquetar un bordado estándar como si fuera de alta dedicación, lo que llevaría a cotizar un plazo de entrega excesivamente largo o un precio más alto, con el riesgo comercial de perder al cliente.
* Un **Falso Negativo** significa clasificar un bordado muy complejo y exigente como si fuera estándar ($0$), asignando tiempos insuficientes a las artesanas y cobrando una tarifa por debajo del costo real de confección. Esto provoca retrasos en la entrega, sobrecostos operativos y pérdida directa de rentabilidad para el taller.
* **Métrica más conveniente:** En este contexto, el Falso Negativo es el más perjudicial financieramente. Por tanto, la métrica prioritaria es el **Recall (Sensibilidad)**, buscando capturar todos los pedidos de alta dedicación reales. Sin embargo, para no descuidar la competitividad de las cotizaciones, se emplea el **F1-Score** como métrica balanceada de selección final.

### 3. ¿Qué pasaría si los datos de prueba se escalaran con su propia media? ¿Cómo lo evita el Pipeline?
**Respuesta:**  
Si los datos de prueba se escalan con su propia media y desviación estándar, se incurre en una violación metodológica conocida como **fuga de información (*data leakage*)**: el modelo estaría evaluando inferencias condicionadas a información global de un conjunto que, en teoría, representa el futuro o datos nunca antes vistos. Además, en producción real (cuando llega una sola muestra para predecir), es imposible calcular una media o desviación sobre un único registro.  
El **`Pipeline` de Scikit-Learn** previene este error de diseño de forma automática: durante `pipeline.fit()`, ajusta (`fit_transform`) el `StandardScaler` calculando la media $\mu_{\text{train}}$ y la desviación $\sigma_{\text{train}}$ **exclusivamente con los datos de entrenamiento**. Posteriormente, al ejecutar `pipeline.predict()`, aplica únicamente la transformación (`transform`) usando esa misma media y desviación previamente fijadas.

### 4. ¿Por qué el árbol de profundidad 12 acierta el 100% en entrenamiento y menos en prueba?
**Respuesta:**  
Porque un árbol con profundidad 12 dispone de hasta $2^{12} = 4096$ hojas posibles, permitiéndole crear bifurcaciones extremadamente específicas para aislar cada una de las 96 muestras de entrenamiento en sus propias hojas terminales. El árbol no está aprendiendo el patrón subyacente de la relación lluvia-temperatura, sino que está **memorizando literalmente el ruido, irregularidades y peculiaridades de los datos observados**. Al recibir datos de prueba con pequeñas variaciones normales, las reglas hiper-específicas del árbol fallan en generalizar.

### 5. ¿Qué tienen en común el perceptrón hecho a mano, `LogisticRegression` y cada neurona de `MLPClassifier`?
**Respuesta:**  
Los tres comparten la misma **unidad computacional fundamental (la neurona artificial)**:
1. **Combinación lineal ponderada:** Reciben un vector de entradas $\mathbf{x}$, lo multiplican por un vector de pesos $\mathbf{w}$ y le suman un término independiente o sesgo $b$: $z = \mathbf{w}^T \mathbf{x} + b$.
2. **Función de activación no lineal:** Pasan dicha suma por una función de activación (la función sigmoide en el perceptrón y en `LogisticRegression`, o funciones como sigmoide, tanh o ReLU en las neuronas del `MLPClassifier`) para mapear el valor real continuo a un espacio acotado.
3. **Optimización guiada por gradientes:** Ajustan sus pesos minimizando una función de pérdida (entropía cruzada logarítmica) calculando derivadas parciales y actualizando parámetros en dirección contraria al gradiente.

---

## 5. Instrucciones para Ejecución en Docker o Entorno Local

### Ejecución con Docker Compose
```bash
cd clase12
docker-compose up -d --build
docker exec -it ia_python bash

# Dentro del contenedor (/app/src)
cd src
python clasificar_cultivos.py
python usar_modelo.py
python regresion_rendimiento.py
python red_xor.py
python profundidad_arbol.py
exit
```

### Ejecución Directa en Python
```bash
cd clase12/src
python clasificar_cultivos.py
python usar_modelo.py
python regresion_rendimiento.py
python red_xor.py
python profundidad_arbol.py
```
