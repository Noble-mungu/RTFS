#!/bin/bash

# Start the first producer in the background
python kafka_producer_random.py &

# Start the second producer in the background
python kafka_producer_random_2.py &

# Wait for all background processes to finish
wait