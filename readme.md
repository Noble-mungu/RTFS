## REAL-TIME FRAUD ANALYTICS SYSTEM

## WORKFLOW AND ARCHITECTURE

![alt text](file:///C:/Users/HomePC/Downloads/Screenshot%202024-05-22%20190000.png)



## Simulate Data

Generate 100 customers' information and save it to customer.csv.
Generate over 10,000 transaction records and save them to transaction_training.csv.
Data Import

Use a Spark SQL job to retrieve data from CSV files and import them into a Mongo/Cassandra database.

## Model Training

## Run a Spark ML job to read data from Mongo/Cassandra
Train models (Preprocessing and Random Forest) to classify transactions as fraud or non-fraud.
Save the trained models to the file system.
Real-Time Processing

## Start a Spark Streaming job to:
Load ML models.
Consume credit card transactions from Kafka.
Create a Kafka topic and produce transaction records from transaction_testing.csv.
Predict transaction fraud status.
Save transactions into fraud_transaction and non_fraud_transaction tables in Mongo/Cassandra based on classification.
Display Results

Use Spring Boot to create a dashboard displaying fraud and non-fraud transactions in real-time.

## Flask to create REST APIs to:
Retrieve customer information.
Create transaction statements for each customer.

## Implementation Details
## Customers & Transactions dataset
Stimulate 100 customers using [Mockaroo](https://www.mockaroo.com/). For each record, it includes following columns (information):

cc_num: credit card number which uniquely identify each card / customer
first: customer's first name
last: customer's last name
gender: customer's gender
street
city
state
zip: zip code for the address above
lat: latitude for the address above
long: longitude for the address above
job: customer's vocation
dob: the date of birth for the customer
Also generate over 10K transaction records for these customers using the same way. For each record, it includes following columns (information):

cc_num: credit card number which uniquely identify each card / customer
first: customer's first name
last: customer's last name
trans_num: transaction number
trans_date: transaction date
trans_time: transaction time
unix_time: transaction time in unix timestamp format
category: category for the purchased item
amt: transaction amount
merchant: the place that the transaction happened
merch_lat: latitude for the merchant
merch_long: longitude for the merchant
is_fraud: boolean to indicate the transaction is fraud or not


## Kafka producer
Create a Kafka topic named as creditcardTransaction with 3 partitions.

kafka-topics --zookeeper localhost:2181 --create --topic 

creditcardTransaction  --replication-factor 1 --partitions 3
The Kafka producer job would randomly select transactions from the transaction training dataset as messages and save the current timestamp into the messages as the transaction time. Later, these messages would be fed into the Spark Streaming job.
## Spark ML job
## Data Preprocessing and Storage

Spark SQL retrieves customer and transaction data.
Data is imported into Cassandra database.
During import, calculates additional features:
Age (based on customer's date of birth)
Distance (Euclidean distance between customer and merchant)
Training data is split and stored in separate tables:
Fraud transactions
Non-fraud transactions

## Model Training

Spark ML loads data from fraud and non-fraud tables.
Data undergoes transformations:
StringIndexer - Converts categorical data to numerical values.
OneHotEncoder - Normalizes numerical data.
VectorAssembler - Combines all features into a single vector.
Data balancing: Reduces non-fraud transactions (K-means) to address imbalance.
Balanced data is used to train a Random Forest classification model.
Trained model is saved to the filesystem.





## Front-end dashboard
The front-end dashboard class is designed with Spring Bot framework that would select fraud and non-fraud transactions from Cassandra tables and display it on the dashboard in real-time. This method will call a select query to retrieve the latest fraud and non-fraud transactions that occurred in the last 5 seconds and display it on the dashboard. To display the record only once, the method maintains the max timestamp of previously displayed fraud/non-fraud transactions. And in the current trigger, it would only select those transactions whose timestamp is greater than the previous max timestamp.

## REST API for customers and transaction statements
I also design two REST APIs with the Flask framework to easily retrieve the customer information and create transaction statements for customers. They are all implemented by calling SQL queries to select records from the Cassandra non-fraud table.

For customer information, the endpoint is: /api/customer/<cc_num> which would return basic information for the credit card <cc_num> owner.
For creating a transaction statement for the specific customer, the endpoint is: api/statement/<cc_num> which would return all the transaction records for the credit card <cc_num> and order them by transaction time.


## Implementation in Java/Scala and Apache Maven
https://github.com/Noble-mungu/RTFS-A