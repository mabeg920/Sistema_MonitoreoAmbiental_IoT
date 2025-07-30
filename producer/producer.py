from kafka import KafkaProducer
import time
import json
import os
from kafka.errors import NoBrokersAvailable
import random
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


MAX_RETRIES = 5       # Número máximo de intentos
RETRY_DELAY = 5       # Segundos entre intentos

producer = None
for attempt in range(1, MAX_RETRIES + 1):
    try:
        print(f"Intento {attempt} de conexión con el broker Kafka...",flush=True)
        
        admin_client = KafkaAdminClient(bootstrap_servers='kafka:9092')
        topic = NewTopic(name="iot-data", num_partitions=2, replication_factor=1)
        try:
            admin_client.create_topics([topic])
            print("Tópico 'iot-data' creado con 2 particiones.", flush=True)
        except TopicAlreadyExistsError:
            print("Tópico ya existe, no se necesita crear.", flush=True)
        finally:
            admin_client.close()
        
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            api_version=(2, 0, 2),
        )
        print("Conexión exitosa con el broker Kafka.",flush=True)
        break  # Salir del bucle si se conecta correctamente

    except NoBrokersAvailable as e:
        print(f"No se pudo conectar con el broker Kafka. Reintentando en {RETRY_DELAY} segundos...",flush=True)
        print("Detalle:", str(e),flush=True)
        time.sleep(RETRY_DELAY)

    except Exception as e:
        print("Error inesperado al crear el productor Kafka.",flush=True)
        print("Detalle:", str(e),flush=True)
        break
i = 0
topic = "iot-data"
while True:
    data =  {
        'temperature': round(random.uniform(20.0, 30.0), 2),
        'humidity': round(random.uniform(30.0, 60.0), 2)
    }
    print(f"Enviando: {data}",flush=True)
    producer.send(topic, value=data)
    time.sleep(2)
    i += 1
