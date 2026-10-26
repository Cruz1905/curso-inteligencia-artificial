# Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago 🧵🤖

**Asignatura:** Inteligencia Artificial – COTECNOVA 2026-02  
**Docente:** Jhon James Cano Sánchez  
**Integrantes:** Davison Cruz & Juan Diego Zapata  
**Fecha de Avance (Corte 1):** 21 de septiembre de 2026  
**Fecha de Avance (Corte 2):** 25 de octubre de 2026  

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

## 4. Avance 2: Primer Modelo de IA – Perceptrón con Sigmoide desde Cero (Clases 8 y 9)

Como hito fundamental del Segundo Corte, se implementó en `src/perceptron_proyecto.py` una neurona artificial simple unicapa entrenada mediante **descenso del gradiente en lote** sin librerías de alto nivel (utilizando exclusivamente **NumPy puro**).

### Formulación Matemática del Modelo:
1. **Variable Objetivo ($y \in \{0, 1\}$):** Clasificación binaria de dedicación horaria (`alta_dedicacion`), donde $y = 1$ si las horas de confección son mayores o iguales a la mediana ($29.0\text{ h}$), y $y = 0$ si son menores. Esta elección garantiza un balance perfecto de clases (10 pedidos en cada clase). Ni `horas_trabajo` ni `precio_cop` se usan como entradas para evitar fuga de información (*data leakage*).
2. **Variables de Entrada Escaladas ($X_{\text{std}}$):** Superficie del bordado (`area_cm2`) y consumo de hilo (`madejas_hilo`), transformadas mediante estandarización $Z$-score ($z = \frac{x - \mu}{\sigma}$).
3. **Función de Activación:** Sigmoide $\sigma(z) = \frac{1}{1 + e^{-z}}$.
4. **Función de Pérdida:** Pérdida Logarítmica (*Binary Cross-Entropy*):
   $$L = -\frac{1}{N} \sum_{i=1}^N \left[ y^{(i)} \log(\hat{y}^{(i)}) + (1 - y^{(i)}) \log(1 - \hat{y}^{(i)}) \right]$$
5. **Gradientes Analíticos:**
   $$\frac{\partial L}{\partial w_j} = \frac{1}{N} \sum_{i=1}^N (\hat{y}^{(i)} - y^{(i)}) x_j^{(i)}, \quad \frac{\partial L}{\partial b} = \frac{1}{N} \sum_{i=1}^N (\hat{y}^{(i)} - y^{(i)})$$

### Resultados Cuantitativos del Entrenamiento:
- **Pérdida inicial:** $0.6931$ (azar teórico con clases balanceadas $-\ln(0.5)$).
- **Pérdida final:** $0.1361$ (reducción progresiva de $0.5571$).
- **Exactitud final (Accuracy):** **$100.0\%$** ($20/20$ aciertos en la clasificación de la mediana).
- **Parámetros finales aprendidos:**
  - $w_1 (\text{Área}) = +3.5566$
  - $w_2 (\text{Madejas}) = +3.4419$
  - $b (\text{Sesgo}) = +1.7104$

### Interpretación en el Contexto del Proyecto:
- **Signo de los pesos ($w_1 > 0, w_2 > 0$):** Demuestra que tanto el incremento de área bordada como la cantidad de madejas aumentan monotónicamente la probabilidad de que una prenda exija alta dedicación temporal ($\ge 29$ horas).
- **Frontera de decisión y separabilidad lineal:** El gráfico `frontera_decision_perceptron.png` muestra una clara línea divisoria $w_1 x_1 + w_2 x_2 + b = 0$ que separa los encargos ligeros/medianos de las piezas de alta dedicación.
- **Gráficos generados:** `curva_aprendizaje_perceptron.png` y `frontera_decision_perceptron.png`.

---

## 5. Instrucciones de Ejecución con Docker 🐳

Todo el entorno de ejecución está completamente contenerizado para garantizar reproducibilidad en cualquier sistema operativo.

### Paso 1: Iniciar el contenedor de desarrollo
Desde la raíz del repositorio, levantar el servicio con Docker Compose:
```bash
docker compose up -d
```

### Paso 2: Acceder a la terminal del contenedor
Ingresar a la sesión interactiva de Bash:
```bash
docker exec -it ia_python bash
```
El prompt de la terminal mostrará la ruta de trabajo:
```text
root@...:/app#
```

### Paso 3: Ejecutar los scripts del proyecto
Navegar a la carpeta de código fuente del proyecto y ejecutar los programas:
```bash
cd /app/proyecto/src

# 1. Ejecutar análisis exploratorio (EDA):
python eda_proyecto.py

# 2. Ejecutar limpieza y preparación de datos:
python preparacion_datos_proyecto.py

# 3. Ejecutar el modelo perceptrón desde cero:
python perceptron_proyecto.py
```

---

## 6. Plan hacia el Proyecto Final (Tercer Corte)

- **Tipo de problema final:** **REGRESIÓN** multivariable (estimación precisa y continua de `horas_trabajo` y `precio_cop` en pesos colombianos).
- **Modelos de Scikit-Learn a comparar (Clase 12 - 9 de noviembre):**
  1. *Regresión Lineal Múltiple* (Línea base).
  2. *Árboles de Decisión para Regresión* (`DecisionTreeRegressor`).
  3. *Bosques Aleatorios* (`RandomForestRegressor`).
  4. *Gradient Boosting* (`GradientBoostingRegressor`).
- **Métricas de Selección:**
  - $R^2$ (*Coeficiente de determinación*): Proporción de la varianza explicada (se buscará $R^2 > 0.85$).
  - $\text{MAE}$ (*Mean Absolute Error*): Error absoluto medio expresado directamente en horas y en pesos COP para fácil interpretación comercial por las bordadoras.
  - $\text{RMSE}$ (*Root Mean Squared Error*): Penalización de errores grandes en piezas de alto costo.
- **Demostración Final:** Módulo interactivo de inferencia que reciba un pedido nuevo (ej. Guayabera de 450 cm² en lino con calado fino) y retorne la cotización y calendario sugerido.
- **Cronograma de Trabajo:**
  - *26 de octubre - 8 de noviembre:* Implementación y ajuste de modelos con Scikit-Learn.
  - *9 de noviembre (Clase 12):* Validación cruzada y comparación sistemática de algoritmos.
  - *10 de noviembre - 22 de noviembre:* Desarrollo de la interfaz demostrativa e informe final en normas APA.
  - *23 / 30 de noviembre:* Sustentación final del proyecto.
