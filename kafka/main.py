from confluent_kafka import Producer
import json
import time
import random

# Kafka broker configuration
conf = {'bootstrap.servers': "localhost:9092"}

# Create Kafka producer
producer = Producer(conf)

# Function to generate random transaction messages
def generate_transaction():
    transaction = {
        "cc_num": random.randint(1000, 9999),
        "amount": round(random.uniform(10.0, 1000.0), 2),
        "timestamp": int(time.time())  # Current timestamp
    }
    return json.dumps(transaction)

# Produce messages to Kafka topic
topic = "creditcardTransaction"
for _ in range(10):  # Produce 10 random messages
    message = generate_transaction()
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()

print("Messages sent to Kafka topic")

# Close the producer
producer.flush()
producer.close()
