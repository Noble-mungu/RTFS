from kafka import KafkaProducer
from json import dumps
import random
import time

def main():
    """Load the whole file to a dictionary and send messages to Kafka."""
    # customer_id, phone number, features.
    with open("balanced_data.csv", "r") as f:
        index2line = {}
        header = True  # To skip the header
        index = 0
        
        for line in f:
            line = line.rstrip('\n')
            if header:
                header = False
                continue
            
            index2line[index] = line
            index += 1
    
    # Initialize Kafka Producer with the specified bootstrap servers, API version, and serializer
    producer = KafkaProducer(
        bootstrap_servers=['kafka-1:9092', 'kafka-2:9092', 'kafka-3:9092'],
        api_version=(0, 11, 5),
        value_serializer=lambda x: dumps(x).encode('utf-8')
    )
    
    index_max = len(index2line) - 1
    print("Total number of records:", index_max + 1)
    
    key = 0  # The serial key of the current message
    index = random.randint(0, index_max)  # Start at a random index
    while key < 600000:   
        line = index2line[index] 
        time_produced = int(1000 * time.time())  # Timestamp in milliseconds
        msg = f"{key},{line},{time_produced}"  # Construct message
        producer.send('transactions-forward', value=msg)
        producer.flush()  # Ensure the message is sent
        
        key += 1
        index = index + 1 if index < index_max else 0  # Circular indexing

if __name__ == '__main__':
    main()
