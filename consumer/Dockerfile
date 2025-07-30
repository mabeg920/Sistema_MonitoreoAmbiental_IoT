# Indica la imagen base de Python 3.11 en versión ligera (sin herramientas innecesarias)
FROM python:3.11-slim

# Establece /app como directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos del directorio actual (host) al directorio /app del contenedor
COPY . .

# Instala la librería kafka-python necesaria para conectar con Apache Kafka
RUN pip install kafka-python

# Comando que se ejecutará por defecto cuando el contenedor inicie
CMD ["python", "consumer.py"]