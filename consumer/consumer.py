from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable, KafkaError
import json
import time

TOPIC_NAME = 'iot-data'
BOOTSTRAP_SERVERS = 'kafka:9092'  
GROUP_ID = 'iot-group'

def esperar_kafka():
    """Intenta conectarse a Kafka hasta que esté disponible."""
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC_NAME,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id=GROUP_ID,
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )
            print("Conectado a Kafka.")
            return consumer
        except NoBrokersAvailable:
            print("Esperando que Kafka esté disponible...")
            time.sleep(5)

def consumir_datos(consumer):
    """Lee datos del tópico y maneja errores de conexión."""
    print(f"Esperando datos del tópico '{TOPIC_NAME}'...")
    while True:
        try:
            for msg in consumer:
                print(f"Recibido: {msg.value}")
        except KafkaError as e:
            print(f"Error de Kafka: {e}. Reintentando en 5 segundos...")
            time.sleep(5)
            consumer.close()
            consumer = esperar_kafka()

if __name__ == "__main__":
    consumer = esperar_kafka()
    consumir_datos(consumer)
