from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Create a SparkSession
spark = SparkSession.builder.appName("KafkaConsumer").getOrCreate()

# Define the schema for the Kafka message
schema = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("amount", DoubleType(), True),
    StructField("card_number", StringType(), True)
])

# Read data from Kafka topic
raw_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "credit_card_transactions") \
    .load()

# Deserialize the Kafka message
transaction_stream = raw_stream.selectExpr("CAST(value AS STRING)").select(from_json("value", schema).alias("data")).select("data.*")

# Perform processing or analysis on the transaction_stream
# ...

# Start the Spark Streaming query
query = transaction_stream.writeStream.outputMode("append").format("console").start()

# Await termination (Ctrl+C to stop)
query.awaitTermination()
