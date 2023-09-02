# Define the PostgreSQL connection properties
postgres_url = "jdbc:postgresql://localhost:5432/your_database"
properties = {
    "user": "your_user0",
    "password": "your_password",
    "driver": "org.postgresql.Driver"
}

# Write the processed data to PostgreSQL
query = transaction_stream.writeStream.foreachBatch(lambda batch_df, batch_id: batch_df.write \
    .jdbc(url=postgres_url, table="credit_card_transactions", mode="append", properties=properties)) \
    .outputMode("append").start()

# Await termination (Ctrl+C to stop)
query.awaitTermination()
