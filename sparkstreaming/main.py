from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.ml import PipelineModel

# Create SparkSession
spark = SparkSession.builder \
    .appName("CreditCardFraudDetection") \
    .getOrCreate()

# Read from Kafka
transactions = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "creditcardTransaction") \
    .load()

# Extract message value and timestamp
transaction_df = transactions.selectExpr("CAST(value AS STRING)", "timestamp") \
    .withColumn("transaction", from_json("value", "struct<cc_num:integer,amount:double,timestamp:integer>")) \
    .select("transaction.*", "timestamp")

# Compute features
customer_data = spark.read.format("mongo").load()  # Read customer data from MongoDB
transaction_df = transaction_df.join(customer_data, transaction_df.cc_num == customer_data.cc_num, "left") \
    .withColumn("age", year(current_date()) - year(customer_data.dob)) \
    .withColumn("distance", sqrt(pow(transaction_df.lat - customer_data.lat, 2) + pow(transaction_df.long - customer_data.long, 2)))

# Load machine learning models
preprocessing_model = PipelineModel.load("preprocessing_model")
rf_model = PipelineModel.load("rf_model")

# Apply models for prediction
prediction_df = preprocessing_model.transform(transaction_df) \
    .transform(rf_model)

# Save results to Mongodb
fraud_df = prediction_df.filter(prediction_df.prediction == 1) \
    .select("cc_num", "amount", "timestamp", "prediction") \
    .write.format("org.apache.spark.sql.cassandra") \
    .options(table="fraud", keyspace="fraud_detection") \
    .save()

non_fraud_df = prediction_df.filter(prediction_df.prediction == 0) \
    .select("cc_num", "amount", "timestamp", "prediction") \
    .write.format("org.apache.spark.sql.cassandra") \
    .options(table="non_fraud", keyspace="fraud_detection") \
    .save()

# Offset management
query = transaction_df.writeStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("topic", "fraud_detection") \
    .option("checkpointLocation", "checkpoint") \
    .start()

query.awaitTermination()
