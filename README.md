# Curso de Inteligencia Artificial 🤖
## Facultad de Ingeniería de Sistemas · COTECNOVA (2026-02)
* **Docente:** Jhon James Cano Sánchez
* **Estudiante:** Davison Cruz López

Repositorio integral con las actividades prácticas de clase, talleres, exámenes parciales y el proyecto de aula en Inteligencia Artificial.

---

## 📁 Estructura del Repositorio

- **[`proyecto/`](./proyecto/)**: **Sistema Inteligente de Tasación y Estimación de Tiempos para Bordados Tradicionales de Cartago**. Incluye EDA, preparación de datos, perceptrón desde cero con NumPy (Avance 2) y los modelos finales de clasificación y regresión implementados con Scikit-Learn, Pipelines y serialización `joblib` (Clase 12 / Entrega Final).
- **[`clase12/`](./clase12/)**: **Scikit-Learn: Entrenar, Evaluar y Guardar Modelos**. Comparación de modelos con Pipelines, métricas de clasificación y regresión, solución de la compuerta XOR con `MLPClassifier`, análisis empírico de sobreajuste y persistencia con `joblib`.
- **[`parcial2/`](./parcial2/)**: **Segundo Parcial**. Limpieza y depuración con Pandas, visualizaciones con Seaborn, perceptrón desde cero con NumPy y reporte técnico del sector hotelero de Cartago.
- **[`trabajos_clase/`](./trabajos_clase/)**: Talleres y laboratorios de clases anteriores (Clases 1 a 8: EDA con NumPy/Pandas, visualización con Seaborn y neuronas lógicas AND/OR/NOT).

---

## 🛠️ Requisitos e Instalación

- **Python 3.12+**
- Librerías principales: `numpy`, `pandas`, `matplotlib`, `seaborn`, `scikit-learn`, `joblib`

### Entorno Local / Virtual
```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual en Windows PowerShell
.venv\Scripts\Activate.ps1
# O en bash/WSL: source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Entorno Docker
Cada carpeta de entrega (`clase12`, `parcial2`) cuenta con su propio `Dockerfile` y `docker-compose.yml` para ejecución desacoplada y reproducible.
