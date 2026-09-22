# Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago 🧵🤖

**Asignatura:** Inteligencia Artificial – COTECNOVA 2026  
**Docente:** Jhon James Cano Sánchez  
**Integrantes:** Davison Cruz & Juan Diego Zapata  
**Fecha de Avance (Corte 1):** 21 de septiembre de 2026  

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

## 2. Estructura de Datos y Código en Python

El script principal se encuentra en [`src/eda_proyecto.py`](./src/eda_proyecto.py).
- **Carga de datos:** Uso de `csv.DictReader` para mapear los registros a listas de diccionarios tipados.
- **Función propia implementada:** `calcular_rendimiento(area, horas)`, la cual calcula la tasa de $cm^2$ bordados por cada hora efectiva de labor manual.
- **Matriz NumPy:** Conversión de las columnas numéricas (`area_cm2`, `madejas_hilo`, `horas_trabajo`, `precio_cop`) para cómputo vectorial de alta velocidad.

---

## 3. Análisis Exploratorio de Datos (EDA) con NumPy

Mediante funciones vectorizadas de NumPy (`np.mean`, `np.median`, `np.std`, `np.min`, `np.max`), se obtuvieron las siguientes métricas descriptivas:

| Variable Analizada | Promedio (Media) | Mediana | Desv. Estándar | Mínimo | Máximo |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Horas de Trabajo (h)** | 37.30 h | 29.00 h | 24.43 h | 9.50 h | 115.00 h |
| **Precio Sugerido (COP)** | $287,500 COP | $230,000 COP | $181,490 COP | $85,000 COP | $850,000 COP |

---

## 4. Visualizaciones con Matplotlib

1. **Dispersión Área ($cm^2$) vs Horas de Trabajo:** Muestra una clara tendencia ascendente donde a mayor superficie bordada se incrementan las horas, pero con dispersión notable provocada por la técnica artesanal.
2. **Barras de Horas por Técnica:** Evidencia la disparidad de esfuerzo: el *Calado Fino* lidera con más de 50 horas promedio por pieza, contrastando con el *Punto de Cruz* y la *Pata de Cabra*.
3. **Distribución de Precios (Histograma):** La mayor concentración de pedidos oscila entre los $120.000 y $350.000 COP.

---

## 5. Hallazgos Clave

1. **Impacto de la técnica sobre el tiempo:** La técnica artesanal influye más en las horas requeridas que el tamaño bruto de la prenda. Un calado fino de $400\text{ cm}^2$ toma el triple de tiempo que un bordado de cruz de igual tamaño, justificando un modelo predictivo multifactorial.
2. **Asimetría en la fijación de precios tradicionales:** La desviación estándar de precios (\$181.490 COP) refleja la inconsistencia del cobro al tanteo en Cartago, ratificando la necesidad de un sistema objetivo de cotización.

---

## 6. Próximos Pasos (Segundo Corte)
- Normalización y codificación de variables categóricas (`OneHotEncoder`).
- Entrenamiento de modelos de Machine Learning supervisado con `scikit-learn` (`LinearRegression`, `DecisionTreeRegressor`, `RandomForestRegressor`).
- Comparación de métricas de precisión y error ($R^2$, MAE, RMSE).
