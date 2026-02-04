# Usamos una imagen ligera de Python
FROM python:3.9-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos los requerimientos y los instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la app
COPY app.py .

# Copiamos también el script sensor
COPY sensor.py .

# Comando por defecto: permite elegir modo con la variable de entorno MODE
# Si MODE==sensor se ejecuta el sensor; en otro caso se ejecuta la app web
CMD ["sh", "-c", "if [ \"$MODE\" = \"sensor\" ]; then python sensor.py; else python app.py; fi"]
