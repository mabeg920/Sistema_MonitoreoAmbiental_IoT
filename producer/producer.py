# Importaciones de dependencias para el productor de Kafka
from kafka import KafkaProducer # Clase principal para enviar mensajes a Kafka
import time # Librería para manejar pausas y delays
import json # Librería para serializar datos a formato JSON
from kafka.errors import NoBrokersAvailable # Excepción cuando no hay brokers disponibles
import random  # Librería para generar números aleatorios
from kafka.admin import KafkaAdminClient, NewTopic # Clases para administrar tópicos de Kafka
from kafka.errors import TopicAlreadyExistsError   # Excepción cuando el tópico ya existe


MAX_RETRIES = 5 # Número máximo de intentos
RETRY_DELAY = 5 # Segundos entre intentos

# Inicializa variable del productor como None
producer = None

# Bucle para intentar conectar con Kafka hasta MAX_RETRIES veces
for attempt in range(1, MAX_RETRIES + 1):
    try:
        print(f"Intento {attempt} de conexión con el broker Kafka...",flush=True)
        
        # Crea el cliente administrador para gestionar tópicos
        admin_client = KafkaAdminClient(bootstrap_servers='kafka:9092')
        
        # Define configuración del nuevo tópico
        topic = NewTopic(name="iot-data", # Nombre del tópico 
                         num_partitions=2, # Número de particiones para paralelismo 
                         replication_factor=1 # Factor de replicación (copias del tópico)
                         )
        try:
            # Intenta crear el tópico con la configuración definida
            admin_client.create_topics([topic])
            print("Tópico 'iot-data' creado con 2 particiones.", flush=True)
        except TopicAlreadyExistsError:
            # Si el tópico ya existe, muestra el mensaje informativo
            print("Tópico ya existe, no se necesita crear.", flush=True)
        finally:
            # Cierra el cliente administrador para liberar recursos
            admin_client.close()

        # Crear instancia del productor de Kafka
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'], # Lista de servidores Kafka
            value_serializer=lambda v: json.dumps(v).encode('utf-8'), # Serializar valores a JSON y luego a bytes
            api_version=(2, 0, 2), # Versión de la API de Kafka a usar
        )
        print("Conexión exitosa con el broker Kafka.",flush=True)
        break  # Salir del bucle si se conecta correctamente

    except NoBrokersAvailable as e:
        # Captura la excepción cuando no hay brokers disponibles
        print(f"No se pudo conectar con el broker Kafka. Reintentando en {RETRY_DELAY} segundos...",flush=True)
        print("Detalle:", str(e),flush=True)
        # Espera segundos antes del siguiente intento
        time.sleep(RETRY_DELAY)

    except Exception as e:
        print("Error inesperado al crear el productor Kafka.",flush=True)
        print("Detalle:", str(e),flush=True)
        break

# Inicializa contador de mensajes
i = 0
# Define el nombre del tópico donde se enviarán los mensajes
topic = "iot-data"

# Bucle infinito para enviar datos continuamente
while True:
    # Crea el diccionario con datos simulados de sensores IoT
    data =  {
        'temperature': round(random.uniform(20.0, 30.0), 2),  # Temperatura aleatoria entre 20-30°C con 2 decimales
        'humidity': round(random.uniform(30.0, 60.0), 2)  # Humedad aleatoria entre 30-60% con 2 decimales
    }

    print(f"Enviando: {data}",flush=True)
    # Enviar el mensaje al tópico de Kafka
    producer.send(topic, value=data)
    # Esperar 2 segundos antes de enviar el siguiente mensaje
    time.sleep(2)
    # Incrementar contador de mensajes enviados
    i += 1
