from confluent_kafka import Producer
import time
import random

# Kafka producer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Replace with your Kafka broker address
    'client.id': 'credit-card-producer'
}

# Create a Kafka producer instance
producer = Producer(conf)

# Simulate sending 10 records every second (you can replace this with your data retrieval logic)
while True:
    for _ in range(10):
        # Replace this with code to fetch data from the credit card transactions table
        transaction_data = {
            "transaction_id": random.randint(1, 1000),
            "amount": random.uniform(1.0, 1000.0),
            "card_number": "************" + str(random.randint(1000, 9999))
        }

        # Send the data to the Kafka topic
        producer.produce('credit_card_transactions', key=str(transaction_data["transaction_id"]), value=str(transaction_data))

    # Flush the producer to ensure data is sent
    producer.flush()
    time.sleep(1)  # Send data every second
