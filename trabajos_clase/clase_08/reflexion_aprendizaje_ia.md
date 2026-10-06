# Taller y Reflexión Teórica: Pesos, Neuronas y Error (Clase 08)

**Asignatura:** Inteligencia Artificial  
**Institución:** Corporación de Estudios Tecnológicos del Norte del Valle (COTECNOVA)  
**Docente:** Jhon James Cano Sánchez  
**Estudiante:** Davison Cruz  
**Fecha:** Octubre 2026  

---

## 1. Introducción y Fundamentos del Perceptrón Simple

En esta sesión implementamos desde cero en Python puro el modelo fundacional del aprendizaje supervisado: la **neurona artificial (Perceptrón simple)** formulada por Frank Rosenblatt (1958).

El modelo computacional de la neurona se rige por:
1. **Combinación Lineal (Suma Ponderada):**
   $$z = \sum_{i=1}^{n} w_i x_i + b = w_1 x_1 + w_2 x_2 + \dots + w_n x_n + b$$
2. **Función de Activación (Escalón de Heaviside):**
   $$\hat{y} = f(z) = \begin{cases} 1 & \text{si } z \ge 0 \\ 0 & \text{si } z < 0 \end{cases}$$
3. **Cálculo del Error:**
   $$e = y - \hat{y}$$
4. **Regla de Actualización de Parámetros (Perceptron Learning Rule):**
   $$w_i \leftarrow w_i + \alpha \cdot e \cdot x_i$$
   $$b \leftarrow b + \alpha \cdot e$$
   donde $\alpha \in (0, 1]$ representa la tasa de aprendizaje (*learning rate*).

---

## 2. Respuestas a las Preguntas de Reflexión (Sección 6.6)

### 1. ¿Qué pasa si se inicializa $w_1 = 0$, $w_2 = 0$, $b = 0$? ¿La neurona aprende? ¿Por qué?
**Sí, la neurona sí aprende.**  
A diferencia de las redes neuronales multicapa con funciones sigmoides o tangentes hiperbólicas donde la inicialización simétrica en cero puede provocar que todas las neuronas ocultas calculen el mismo gradiente, en un perceptrón simple para compuertas booleanas con regla de corrección de error:
- En la primera muestra $(x_1, x_2)$, si produce un error ($e \neq 0$), la regla $w_i \leftarrow w_i + \alpha \cdot e \cdot x_i$ rompe inmediatamente el valor cero para aquellas entradas donde $x_i = 1$.
- De igual forma, el sesgo $b$ se actualiza como $b \leftarrow b + \alpha \cdot e$.
- Dado que los datos son linealmente separables, el **Teorema de Convergencia del Perceptrón** garantiza que los pesos encontrarán un hiperplano separador en un número finito de pasos sin importar si iniciaron en cero o en valores pequeños.

### 2. ¿Qué pasa si la tasa de aprendizaje es muy alta? (ej. $\alpha = 1.0$) ¿La neurona aprende o se "desestabiliza"?
Para el problema específico de compuertas booleanas con entradas discretas $\{0, 1\}$ y función escalón:
- Con $\alpha = 1.0$, el perceptrón sigue convergiendo rápidamente porque las magnitudes de los pasos son múltiplos enteros de las entradas y los datos son pocos y fijos.
- Sin embargo, en problemas continuos o funciones de pérdida suaves (descenso del gradiente con MSE), una tasa $\alpha$ excesivamente grande genera **oscilaciones violentas** y sobrepasos (*overshooting*), haciendo que el modelo salte por encima del mínimo óptimo e impidiendo la convergencia.

### 3. ¿Qué pasa si la tasa de aprendizaje es muy baja? (ej. $\alpha = 0.001$) ¿Cuántas épocas necesita?
- **Convergencia extremadamente lenta:** Con $\alpha = 0.001$, cada error genera una corrección diminuta en los pesos ($\Delta w \approx 0.001$).
- Para mover el hiperplano desde $b = 0.0$ hasta el umbral negativo requerido por la compuerta AND (por ejemplo, $b \approx -0.3$), la neurona requerirá decenas o cientos de épocas acumulando pequeños ajustes.
- Aunque el modelo terminará convergiendo (dada la separabilidad lineal), el costo computacional se multiplica drásticamente de forma innecesaria.

### 4. ¿Por qué el *bias* (sesgo) es necesario? ¿Qué pasaría si $b = 0$ siempre?
El sesgo $b$ actúa como un término independiente que permite desplazar la frontera de decisión en el espacio:
- La ecuación de la frontera de decisión es:
  $$w_1 x_1 + w_2 x_2 + b = 0 \implies x_2 = -\frac{w_1}{w_2} x_1 - \frac{b}{w_2}$$
- **Si $b = 0$ siempre:** La recta separadora está forzada a pasar estrictamente por el origen de coordenadas $(0, 0)$.
- **Consecuencia crítica en la compuerta AND:** Para $(0, 0)$, $z = w_1(0) + w_2(0) + 0 = 0$. Dado que $\text{escalon}(0) = 1$, la neurona predeciría $1$ en $(0, 0)$, lo cual es un error garrafal para AND (donde $0 \text{ AND } 0 = 0$). Sin un sesgo negativo ($b < 0$), es algebraicamente imposible que la recta clasifique a $(0, 0)$ como clase $0$ y al mismo tiempo pase por el origen. Por ende, **el bias es imprescindible para desplazar el hiperplano fuera del origen**.

### 5. ¿Cómo cambiaría el código si se quisiera aprender la compuerta OR en lugar de AND?
Solo es necesario modificar el conjunto de datos de entrenamiento (`datos`), asignando como etiquetas esperadas:
$$(0, 0) \to 0, \quad (0, 1) \to 1, \quad (1, 0) \to 1, \quad (1, 1) \to 1$$
La estructura de la neurona, la función de activación y la fórmula de actualización de pesos permanecen idénticas, demostrando el principio general de la IA: el algoritmo aprende las reglas a partir de los datos sin reprogramar la lógica de inferencia.

---

## 3. Resultados de la Actividad Independiente (Sección 7)

### 3.1. Resumen de Convergencia por Compuerta

| Compuerta Lógica | Entradas | Parámetros Iniciales | Épocas para Converger | Parámetros Finales Aprendidos | Archivo de Gráfica |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **AND** | 2 | $w_1=0.1, w_2=0.1, b=0.0$ | **3 épocas** | $w_1=0.200, w_2=0.100, b=-0.200$ | `evolucion_error_and.png` |
| **OR** | 2 | $w_1=0.0, w_2=0.0, b=0.0$ | **4 épocas** | $w_1=0.100, w_2=0.100, b=-0.100$ | `evolucion_error_or_not.png` |
| **NOT** | 1 | $w=0.0, b=0.0$ | **3 épocas** | $w=-0.100, b=0.000$ | `evolucion_error_or_not.png` |

---

## 4. Análisis y Respuestas a la Actividad Independiente

### 1. ¿Cuántas épocas necesitó cada compuerta para aprender?
- **Compuerta AND:** Con $\alpha = 0.1$ y pesos iniciales de $0.1$, convergió en **3 épocas**.
- **Compuerta OR:** Con $\alpha = 0.1$ e inicialización en ceros, convergió en **4 épocas**.
- **Compuerta NOT:** Con 1 sola entrada, convergió en **3 épocas**.

### 2. ¿Fue necesario ajustar la tasa de aprendizaje? ¿Por qué?
No fue necesario modificar $\alpha = 0.1$. Con este valor, las compuertas convergen de manera estable en menos de 5 épocas, lo que permite apreciar la disminución progresiva del error acumulado sin oscilaciones ni demoras excesivas.

### 3. ¿Qué diferencias encontró entre la compuerta AND y la OR?
- **Frontera de decisión:** 
  - En la compuerta **AND**, solo un punto pertenece a la clase $1$ (el punto $(1, 1)$), mientras que los otros 3 pertenecen a la clase $0$. Por ello, el hiperplano debe aislar estrictamente la esquina superior derecha, exigiendo un sesgo negativo mayor para compensar la suma de pesos ($b \le -w_1$ y $b \le -w_2$, con $w_1 + w_2 + b \ge 0$).
  - En la compuerta **OR**, tres puntos pertenecen a la clase $1$ y únicamente el origen $(0, 0)$ pertenece a la clase $0$. Por lo tanto, cualquier peso individual positivo basta para activar la neurona, y la recta separadora pasa muy cerca del origen.

### 4. ¿Por qué la compuerta XOR no puede ser aprendida por una sola neurona?
Este es el célebre **Problema de Separabilidad Lineal**, expuesto por Marvin Minsky y Seymour Papert en 1969 en su influyente libro *Perceptrons*.

#### Justificación Geométrica:
En el plano cartesiano bidimensional $(x_1, x_2)$, los cuatro estados de la tabla de verdad de la compuerta XOR se distribuyen de la siguiente manera:
- $(0, 0) \to 0$ (Clase A)
- $(1, 1) \to 0$ (Clase A)
- $(0, 1) \to 1$ (Clase B)
- $(1, 0) \to 1$ (Clase B)

Las clases están situadas en vértices diagonalmente opuestos del cuadrado unitario:
- Los puntos de clase $1$ están en $(0,1)$ y $(1,0)$.
- Los puntos de clase $0$ están en $(0,0)$ y $(1,1)$.

Una sola neurona artificial representa una función lineal $w_1 x_1 + w_2 x_2 + b = 0$, que geométricamente es una **línea recta única**. Es físicamente imposible trazar una sola línea recta continua que separe simultáneamente los puntos $(0,1)$ y $(1,0)$ de los puntos $(0,0)$ y $(1,1)$. Se requerirían al menos **dos rectas** (dos hiperplanos de decisión).

#### Justificación Matemática:
Para que un perceptrón clasifique correctamente XOR, debe satisfacer simultáneamente el siguiente sistema de inecuaciones:
1. Para $(0, 0) \to 0$:  
   $$w_1(0) + w_2(0) + b < 0 \implies b < 0$$
2. Para $(0, 1) \to 1$:  
   $$w_1(0) + w_2(1) + b \ge 0 \implies w_2 + b \ge 0 \implies w_2 \ge -b$$
3. Para $(1, 0) \to 1$:  
   $$w_1(1) + w_2(0) + b \ge 0 \implies w_1 + b \ge 0 \implies w_1 \ge -b$$
4. Para $(1, 1) \to 0$:  
   $$w_1(1) + w_2(1) + b < 0 \implies w_1 + w_2 + b < 0 \implies w_1 + w_2 < -b$$

Sumando las inecuaciones (2) y (3):
$$w_1 + w_2 \ge -2b$$
Sustituyendo esto en la inecuación (4):
$$-2b \le w_1 + w_2 < -b \implies -2b < -b \implies -b < 0 \implies b > 0$$

Sin embargo, la inecuación (1) exige de forma obligatoria que $b < 0$.  
Llegamos a una **contradicción matemática insoluble** ($b < 0$ y $b > 0$ al mismo tiempo).

#### Conclusión:
Un perceptrón simple unicapa no puede resolver problemas que no sean linealmente separables. Para resolver la compuerta XOR es indispensable contar con una **red neuronal multicapa (MLP - Multilayer Perceptron)** con al menos una capa oculta, o introducir transformaciones no lineales en las entradas.
