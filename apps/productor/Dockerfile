# Usamos una imagen ligera de Python
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la app
COPY app.py .
COPY sensor.py .

CMD ["sh", "-c", "if [ \"$MODE\" = \"sensor\" ]; then python sensor.py; else python app.py; fi"]
