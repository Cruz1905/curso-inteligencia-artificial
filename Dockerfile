FROM python:3.12-slim
WORKDIR /app

# 1. Crear el entorno virtual en una ruta limpia
RUN python -m venv /opt/venv

# 2. Activar el entorno virtual agregandolo al PATH
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# 3. Este comando ya usara el pip del venv de forma automatica
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
CMD ["python", "src/main.py"]
