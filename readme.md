## REAL-TIME FRAUD ANALYTICS SYSTEM

## WORKFLOW AND ARCHITECTURE


![Screenshot 2024-05-22 190000](https://github.com/Noble-mungu/RTFS/assets/64100418/4a7d9277-d6c9-4e64-9762-053005911d20)


## Simulate Data

-Generate 100 customers' information and save it to customer.csv.
-Generate over 10,000 transaction records and save them to transaction_training.csv.

Data Import

-Use a Spark SQL job to retrieve data from CSV files and import them into a Mongo database.

## Model Training

## Run a Spark ML job to read data from Mongo
-Train models (Preprocessing and Random Forest) to classify transactions as fraud or non-fraud.
-Save the trained models to the file system.
Real-Time Processing

## Start a Spark Streaming job to:
-Load ML models.</br>
-Consume credit card transactions from Kafka.</br>
-Create a Kafka topic and produce transaction records from transaction_testing.csv.</br>
-Predict transaction fraud status.</br>
-Save transactions into fraud_transaction and non_fraud_transaction tables in Mongo based on classification.</br>
-Display Results</br>
-Use Spring Boot to create a dashboard displaying fraud and non-fraud transactions in real-time.</br>

## Flask to create REST APIs to:
Retrieve customer information.</br>
Create transaction statements for each customer.</br>

## Implementation Details
## Customers & Transactions dataset
Stimulate 100 customers using [Mockaroo](https://www.mockaroo.com/). For each record, it includes following columns (information):</br>

-cc_num: credit card number which uniquely identify each card / customer</br>
-first: customer's first name</br>
-last: customer's last name</br>
-gender: customer's gender</br>
-street</br>
-city</br>
-state</br>
-zip: zip code for the address above</br>
-lat: latitude for the address above</br>
-long: longitude for the address above</br>
-job: customer's vocation</br>
-dob: the date of birth for the customer</br>
Also generate over 10K transaction records for these customers using the same way. For each record, it includes following columns (information):</br>

-cc_num: credit card number which uniquely identify each card / customer</br>
-first: customer's first name</br>
-last: customer's last name</br>
-trans_num: transaction number</br>
-trans_date: transaction date</br>
-trans_time: transaction time</br>
-unix_time: transaction time in unix timestamp format</br>
-category: category for the purchased item</br>
-amt: transaction amount</br>
-merchant: the place that the transaction happened</br>
-merch_lat: latitude for the merchant</br>
-merch_long: longitude for the merchant</br>
-is_fraud: boolean to indicate the transaction is fraud or not</br>


## Kafka producer
Create a Kafka topic named as creditcardTransaction with 3 partitions.
```
kafka-topics --zookeeper localhost:2181 --create --topic 
```
creditcardTransaction  --replication-factor 1 --partitions 3
The Kafka producer job would randomly select transactions from the transaction training dataset as messages and save the current timestamp into the messages as the transaction time. Later, these messages would be fed into the Spark Streaming job.
## Spark ML job
## Data Preprocessing and Storage

* Spark SQL retrieves customer and transaction data.</br>
* Data is imported into Cassandra database.</br>
* During import, calculates additional features:</br>
* Age (based on customer's date of birth)</br>
* Distance (Euclidean distance between customer and merchant)</br>
* Training data is split and stored in separate tables:</br>
* Fraud transactions</br>
* Non-fraud transactions</br>

## Model Training

* Spark ML loads data from fraud and non-fraud tables.</br>
* Data undergoes transformations:</br>
* StringIndexer - Converts categorical data to numerical values.</br>
* OneHotEncoder - Normalizes numerical data.</br>
* VectorAssembler - Combines all features into a single vector.</br>
* Data balancing: Reduces non-fraud transactions (K-means) to address imbalance.</br>
* Balanced data is used to train a Random Forest classification model.</br>
* Trained model is saved to the filesystem.</br>





## Front-end dashboard
The front-end dashboard class is designed with Spring Bot framework that would select fraud and non-fraud transactions from Cassandra tables and display it on the dashboard in real-time. This method will call a select query to retrieve the latest fraud and non-fraud transactions that occurred in the last 5 seconds and display it on the dashboard. To display the record only once, the method maintains the max timestamp of previously displayed fraud/non-fraud transactions. And in the current trigger, it would only select those transactions whose timestamp is greater than the previous max timestamp.

## REST API for customers and transaction statements
I also design two REST APIs with the Flask framework to easily retrieve the customer information and create transaction statements for customers. They are all implemented by calling SQL queries to select records from the Cassandra non-fraud table.

For customer information, the endpoint is: /api/customer/<cc_num> which would return basic information for the credit card <cc_num> owner.
For creating a transaction statement for the specific customer, the endpoint is: api/statement/<cc_num> which would return all the transaction records for the credit card <cc_num> and order them by transaction time.


## Elasticsearch.
Create an index for global blacklist data.
-Index Blacklist Data
-Index customer or transaction data that are marked as blacklisted.


