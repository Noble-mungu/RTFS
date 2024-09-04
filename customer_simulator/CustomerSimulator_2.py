from kafka import KafkaConsumer
import time
import psycopg2
import numpy as np
import os


def main():
    # Get the file path from an environment variable, with a default fallback
    data_file_path = os.environ.get('DATA_FILE_PATH', '/app/balanced_data.csv')

    # Load the Customer_2fraud map
    with open(data_file_path, "r") as f:
        index2fraud = {}

        # Skip the header line
        header = f.readline().rstrip('\n')

        for line in f:
            line = line.rstrip('\n').split(",")

            # The first column is the index, and the last column is the fraud indicator
            index = int(float(line[0]))  # Convert to float first, then to int
            fraud = int(float(line[-1].strip().replace('"', '')))  # Handle scientific notation
            index2fraud[index] = fraud  # 0 -> not fraud, 1 -> fraud

    print("How many indexes: " + str(len(index2fraud)))


    # Kafka consumer configuration
    consumer = KafkaConsumer("transactions-backward", group_id="CustomerSimulator", bootstrap_servers = ['kafka-1:9092','kafka-2:9092','kafka-3:9092'])
    # PostgreSQL connection
    connection = psycopg2.connect(
        dbname='frauddetection',
        user='postgres',
        password='azbycx567',
        host='postgreshost',
        port='5433'
    )
    cursor = connection.cursor()
    print(connection.get_dsn_parameters(), "\n")

    postgres_insert_query = """INSERT INTO transactions (key,index,phonenumber,time,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18,v19,v20,v21,v22,v23,v24,v25,v26,v27,v28,amount,timeproduced,timeprocessed,latency,prediction,reply) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    max_waiting_time = 5000  # 10000 ms, 10s
    
    for message in consumer:
        transaction = message.value.decode('utf-8').split(",")
        index = int(transaction[1])  # Assuming this is the correct index
        time_produced = int(transaction[33])
        time_now = int(time.time() * 1000)
        waiting_time = np.random.poisson(5000)
        
        if waiting_time <= max_waiting_time:
            time_processed = time_now + waiting_time
            latency = time_processed - time_produced
            transaction[34] = str(time_processed)
            transaction[35] = str(latency)
            transaction[37] = "yes" if index2fraud[index] == 1 else "no"
        else:
            time_processed = time_now + max_waiting_time
            latency = time_processed - time_produced
            transaction[34] = str(time_processed)
            transaction[35] = str(latency)
            transaction[37] = "noreply"
        
        try:
            record_to_insert = tuple(transaction)
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into transactions table")
        
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into transactions table", error)
    
    # Closing database connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

    # StopIteration if no message after 1 sec
    KafkaConsumer(consumer_timeout_ms=100000)

if __name__ == '__main__':
    main()
