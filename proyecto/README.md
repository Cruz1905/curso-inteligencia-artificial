# Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago 🧵🤖

**Asignatura:** Inteligencia Artificial – COTECNOVA 2026  
**Docente:** Jhon James Cano Sánchez  
**Integrantes:** Davison Cruz & Juan Diego Zapata  
**Fecha de Avance (Corte 1):** 21 de septiembre de 2026  
**Actualización (Clase 8 - Preparación ML):** 28 de septiembre de 2026  

---

## 1. Definición del Proyecto

### 📌 Problemática
En el municipio de Cartago, Valle del Cauca (*Capital Mundial del Bordado*), los talleres artesanales y modistas tradicionales calculan el costo y tiempo de entrega de sus pedidos de forma meramente empírica ("al ojo"). Al no contar con herramientas estandarizadas para tasar piezas complejas (con técnicas como *calado*, *punto de sombra* o *rococó*), las artesanas suelen subvalorar sus horas de trabajo manual, sufriendo pérdidas económicas continuas o retrasos imprevistos en las entregas.

### 🎯 Objetivo
Desarrollar un sistema basado en Inteligencia Artificial (Machine Learning - Regresión) capaz de estimar con precisión matemática:
1. Las **horas de trabajo manual requeridas** para la confección artesanal.
2. El **precio justo sugerido de venta al público (COP)**, asegurando una retribución digna y competitiva.

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

## 2. Preparación de Datos con Pandas y Seaborn (Clase 8)

En cumplimiento de la actividad complementaria de la **Clase 8**:
- **Exploración con Pandas:** Carga del dataset mediante `pd.read_csv()`, verificación de tipos con `df.info()`, estadísticas descriptivas con `df.describe()` y comprobación de nulos con `df.isnull().sum()` (0 valores nulos detectados).
- **Columnas Derivadas Creadas:**
  - `costo_por_cm2 = precio_cop / area_cm2`: Mide el valor en pesos por centímetro cuadrado bordado.
  - `productividad_cm2_hora = area_cm2 / horas_trabajo`: Cuantifica el avance de la artesana por hora según la técnica.
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

## 4. Hallazgos Clave

1. **Impacto de la técnica sobre el tiempo:** La técnica artesanal influye más en las horas requeridas que el tamaño bruto de la prenda. Un calado fino de $400\text{ cm}^2$ toma el triple de tiempo que un bordado de cruz de igual tamaño, justificando un modelo predictivo multifactorial.
2. **Asimetría en la fijación de precios tradicionales:** La desviación estándar de precios (\$181.490 COP) refleja la inconsistencia del cobro al tanteo en Cartago, ratificando la necesidad de un sistema objetivo de cotización.

---

## 5. Próximos Pasos (Segundo Corte)
- División de datos en conjuntos de entrenamiento y prueba (`train_test_split`).
- Entrenamiento de modelos de Machine Learning supervisado con `scikit-learn` (`LinearRegression`, `DecisionTreeRegressor`, `RandomForestRegressor`).
- Comparación de métricas de precisión y error ($R^2$, MAE, RMSE).
