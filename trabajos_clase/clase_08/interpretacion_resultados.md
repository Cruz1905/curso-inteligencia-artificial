# Interpretación de Resultados - Clase 8: Pandas y Seaborn 📊

**Asignatura:** Inteligencia Artificial – COTECNOVA 2026  
**Estudiante:** Davison Cruz  
**Archivo Analizado:** `ventas_tienda.csv`  

---

## 1. Exploración de Datos
- **Dimensiones:** El dataset original contiene **12 filas** (transacciones) y **9 columnas**.
- **Tipos de datos identificados:**
  - Numéricos enteros (`int64`): `id_venta`, `cantidad`.
  - Numéricos flotantes (`float64`): `precio_unitario`, `cliente_edad`.
  - Categóricos / Texto (`object`): `fecha`, `producto`, `categoria`, `ciudad`, `metodo_pago`.
- **Valores nulos:** Se identificaron **2 valores nulos** en la columna `cliente_edad` (filas 6 y 12).

---

## 2. Limpieza y Tratamiento de Nulos
- **Tratamiento:** Los valores nulos en `cliente_edad` se imputaron utilizando la **mediana** (36.0 años).
- **¿Por qué la mediana y no la media?** La mediana es una medida de tendencia central robusta ante valores extremos o atípicos (*outliers*). En muestras pequeñas como esta, un cliente de edad muy avanzada o muy joven distorsiona el promedio, mientras que la mediana refleja el punto central exacto de la distribución de clientes.

---

## 3. Visualización con Seaborn
- **Categoría con mayor venta:** La categoría de **Alimentos** lidera el total de ventas acumuladas (con productos como Arroz y Café), seguida por Lácteos y Aseo.
- **Relación Edad vs Total Venta:** En el gráfico de dispersión (`edad_vs_venta.png`) se observa que clientes de mayor edad (40 a 55 años) tienden a realizar compras con montos superiores, especialmente en Alimentos y Lácteos, utilizando preferentemente pago en efectivo.

---

## 4. Preparación para Machine Learning
- **Codificación:** Se aplicó **One-Hot Encoding** (`pd.get_dummies()`) sobre las variables categóricas nominales `categoria` (Alimentos, Aseo, Lácteos) y `metodo_pago` (Efectivo, Tarjeta), convirtiéndolas en columnas binarias (0 y 1 / True y False).
- **Eliminación de columnas:**
  - `id_venta`: Es un identificador arbitrario que no aporta información predictiva y causa sobreajuste (*overfitting*).
  - `fecha`: Al no estar descompuesta en estacionalidad o mes, como texto simple añade ruido.
  - `producto`: Presenta alta cardinalidad y su efecto ya queda capturado por la `categoria` y el `precio_unitario`.
  - `ciudad`: Para un modelo general de compra de productos básicos, la ciudad en esta muestra añade dimensionalidad sin correlación suficiente.

---

## 5. Propuesta de Optimización del Código
- **Pipeline de Scikit-Learn:** En lugar de hacer la limpieza e imputación manual en pasos aislados, se puede implementar un `ColumnTransformer` con `SimpleImputer` y `OneHotEncoder`, lo cual previene la fuga de datos (*data leakage*) al dividir en conjuntos de entrenamiento y prueba (*train/test split*).
