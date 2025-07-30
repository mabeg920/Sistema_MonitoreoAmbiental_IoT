# Importaciones de dependencias para el consumidor de Kafka
from kafka import KafkaConsumer # Clase principal para consumir mensajes de Kafka
from kafka.errors import NoBrokersAvailable, KafkaError  # Excepciones (Errores) específicas de Kafka
import json # Librería para manejar datos en formato JSON
import time # Librería para manejar pausas y delays

# Configuración del tópico de Kafka
TOPIC_NAME = 'iot-data' # Nombre del tópico del cual se van a consumir mensajes
BOOTSTRAP_SERVERS = 'kafka:9092' # Servidor de Kafka y puerto para conexión
GROUP_ID = 'iot-group' # ID del grupo de consumidores
                                        
# Intenta conectarse a Kafka hasta que esté disponible.
def esperar_kafka():
    # Bucle infinito para reintentar conexión
    while True:
        try:
            # Crear instancia del consumidor de Kafka
            consumer = KafkaConsumer(
                TOPIC_NAME, # Topic del cual se va a consumir el mensaje 
                bootstrap_servers=BOOTSTRAP_SERVERS, # Servidor de Kafka para conectarse
                value_deserializer=lambda m: json.loads(m.decode('utf-8')), # Función para deserializar mensajes JSON
                group_id=GROUP_ID,  # ID del grupo de consumidores
                auto_offset_reset='earliest', # Leer desde el mensaje más antiguo si no hay offset guardado
                enable_auto_commit=True,  # Confirmar automáticamente los mensajes procesados
            )
            print("Conectado a Kafka.",flush=True)
            # Retornar el consumidor configurado
            return consumer
        except NoBrokersAvailable:
            # Capturar excepción cuando Kafka no está disponible
            print("Esperando que Kafka esté disponible...",flush=True)
            # Esperar 5 segundos antes del siguiente intento
            time.sleep(5)

# Lee datos del tópico y maneja errores de conexión.
def consumir_datos(consumer):
    print(f"Esperando datos del tópico '{TOPIC_NAME}'...",flush=True)
    # Bucle infinito para procesar mensajes continuamente
    while True:
        try:
            # Iterar sobre los mensajes recibidos del tópico
            for msg in consumer:
                print(f"Recibido: {msg.value}",flush=True)
                # Pausa de 2 segundos entre procesamiento de mensajes
                time.sleep(2)
        except KafkaError as e:
            print(f"Error de Kafka: {e}. Reintentando en 5 segundos...",flush=True)
            # Esperar 5 segundos antes de reintentar
            time.sleep(5)
            # Cerrar el consumidor actual para liberar recursos
            consumer.close()
            # Crear nuevo consumidor y reconectar
            consumer = esperar_kafka()

if __name__ == "__main__":
     # Establecer conexión inicial con Kafka
    consumer = esperar_kafka()
    # Iniciar el proceso de consumo de datos
    consumir_datos(consumer)
